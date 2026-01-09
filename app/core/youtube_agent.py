#!/usr/bin/env python3
"""
YouTube Content Management Agent Core

Main agent class that orchestrates YouTube content management operations
through MCP integration and AI-powered services.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import json

from ..core.mcp_client import MCPYouTubeClient
from ..services.analytics_service import AnalyticsService
from ..services.content_service import ContentService
from ..services.optimization_service import OptimizationService
from ..models.video import Video, VideoAnalytics
from ..models.channel import Channel, ChannelAnalytics

logger = logging.getLogger(__name__)

class YouTubeAgent:
    """
    Main YouTube Content Management Agent

    Orchestrates all YouTube-related operations through MCP integration
    and provides AI-powered content management capabilities.
    """

    def __init__(
        self,
        mcp_client: MCPYouTubeClient,
        analytics_service: AnalyticsService,
        content_service: ContentService,
        optimization_service: OptimizationService
    ):
        self.mcp_client = mcp_client
        self.analytics = analytics_service
        self.content = content_service
        self.optimization = optimization_service

        # Agent state
        self.channel_id: Optional[str] = None
        self.is_initialized = False

        logger.info("YouTube Agent initialized")

    async def initialize(self) -> bool:
        """Initialize the agent and verify MCP connection"""
        try:
            # Check MCP connection
            auth_status = await self.check_auth_status()
            if not auth_status.get("authenticated"):
                logger.warning("MCP authentication not verified")
                return False

            # Get channel info to verify access
            channel_info = await self.get_channel_info()
            if channel_info:
                self.channel_id = channel_info.get("id")
                logger.info(f"Agent initialized for channel: {self.channel_id}")
                self.is_initialized = True
                return True
            else:
                logger.error("Could not retrieve channel information")
                return False

        except Exception as e:
            logger.error(f"Agent initialization failed: {e}")
            return False

    async def check_auth_status(self) -> Dict[str, Any]:
        """Check YouTube API authentication status"""
        try:
            result = await self.mcp_client.call_tool("get_auth_status", {})
            return result
        except Exception as e:
            logger.error(f"Auth check failed: {e}")
            return {"authenticated": False, "error": str(e)}

    # Channel Management Methods
    async def get_channel_info(self) -> Optional[Dict[str, Any]]:
        """Get comprehensive channel information"""
        try:
            # Try to get authenticated user's channel first
            result = await self.mcp_client.call_tool("get_channel_info", {"mine": True})

            if result.get("success") and result.get("data"):
                return result["data"]

            # Fallback: try to get by channel ID if configured
            if self.channel_id:
                result = await self.mcp_client.call_tool("get_channel_info", {
                    "channelId": self.channel_id
                })
                if result.get("success") and result.get("data"):
                    return result["data"]

            return None

        except Exception as e:
            logger.error(f"Failed to get channel info: {e}")
            return None

    async def get_channel_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive channel analytics"""
        try:
            # Get basic channel info
            channel_info = await self.get_channel_info()
            if not channel_info:
                return {"error": "Could not retrieve channel information"}

            # Get recent videos for analysis
            videos = await self.get_channel_videos(limit=50)

            # Calculate analytics
            analytics = await self.analytics.calculate_channel_metrics(
                channel_info, videos, days
            )

            return analytics

        except Exception as e:
            logger.error(f"Failed to get channel analytics: {e}")
            return {"error": str(e)}

    # Video Management Methods
    async def get_channel_videos(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get channel videos with pagination"""
        try:
            # Use search to find channel videos (since we don't have a direct "get my videos" tool)
            # This is a workaround - in production you'd want a dedicated tool
            videos = []

            # For now, return mock data or implement through search
            # In a real implementation, you'd have a dedicated MCP tool for this

            return videos

        except Exception as e:
            logger.error(f"Failed to get channel videos: {e}")
            return []

    async def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific video"""
        try:
            result = await self.mcp_client.call_tool("get_video_details", {
                "videoIds": [video_id],
                "parts": ["snippet", "statistics", "contentDetails", "status"]
            })

            if result.get("success") and result.get("data", {}).get("items"):
                return result["data"]["items"][0]

            return None

        except Exception as e:
            logger.error(f"Failed to get video details for {video_id}: {e}")
            return None

    async def search_videos(self, query: str, options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search for videos using YouTube Data API"""
        try:
            search_options = {
                "query": query,
                "maxResults": options.get("maxResults", 25) if options else 25,
                "order": options.get("order", "relevance") if options else "relevance"
            }

            if options:
                if options.get("channelId"):
                    search_options["channelId"] = options["channelId"]

            result = await self.mcp_client.call_tool("search_videos", search_options)

            if result.get("success") and result.get("data", {}).get("items"):
                return result["data"]["items"]

            return []

        except Exception as e:
            logger.error(f"Failed to search videos for query '{query}': {e}")
            return []

    # Content Optimization Methods
    async def optimize_video(self, video_id: str) -> Dict[str, Any]:
        """Optimize a video's metadata for better performance"""
        try:
            # Get current video details
            video_details = await self.get_video_details(video_id)
            if not video_details:
                return {"error": f"Could not retrieve video {video_id}"}

            # Use optimization service
            optimization_result = await self.optimization.optimize_video_metadata(
                video_details
            )

            # Apply optimizations if requested
            if optimization_result.get("apply_changes", False):
                await self._apply_video_optimizations(video_id, optimization_result)

            return optimization_result

        except Exception as e:
            logger.error(f"Failed to optimize video {video_id}: {e}")
            return {"error": str(e)}

    async def optimize_title(self, current_title: str, topic: str = "", audience: str = "") -> str:
        """AI-powered title optimization"""
        try:
            return await self.optimization.optimize_title(current_title, topic, audience)
        except Exception as e:
            logger.error(f"Failed to optimize title '{current_title}': {e}")
            return current_title

    async def generate_description(self, topic: str, key_points: List[str], keywords: List[str]) -> str:
        """AI-powered description generation"""
        try:
            return await self.optimization.generate_description(topic, key_points, keywords)
        except Exception as e:
            logger.error(f"Failed to generate description for topic '{topic}': {e}")
            return f"Learn about {topic} in this comprehensive video."

    # Analytics Methods
    async def get_performance_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive performance analytics"""
        try:
            # Get videos from the specified period
            videos = await self.get_channel_videos(limit=100)

            # Filter by date
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_videos = [
                v for v in videos
                if v.get("snippet", {}).get("publishedAt") and
                datetime.fromisoformat(v["snippet"]["publishedAt"].replace('Z', '+00:00')) > cutoff_date
            ]

            # Calculate analytics
            analytics = await self.analytics.analyze_performance(recent_videos, days)

            return analytics

        except Exception as e:
            logger.error(f"Failed to get performance analytics: {e}")
            return {"error": str(e)}

    async def analyze_content_trends(self) -> Dict[str, Any]:
        """Analyze content performance trends"""
        try:
            # Get historical video data
            videos = await self.get_channel_videos(limit=200)

            # Analyze trends
            trends = await self.analytics.analyze_trends(videos)

            return trends

        except Exception as e:
            logger.error(f"Failed to analyze content trends: {e}")
            return {"error": str(e)}

    # AI-Powered Content Methods
    async def suggest_content_ideas(self, niche: str, performance_data: Dict[str, Any],
                                  trending_topics: List[str]) -> List[Dict[str, Any]]:
        """AI-powered content idea generation"""
        try:
            return await self.content.generate_content_suggestions(
                niche, performance_data, trending_topics
            )
        except Exception as e:
            logger.error(f"Failed to generate content suggestions: {e}")
            return []

    async def analyze_competitor_content(self, competitor_channel_id: str) -> Dict[str, Any]:
        """Analyze competitor channel content strategy"""
        try:
            # Get competitor videos
            competitor_videos = await self.search_videos("", {
                "channelId": competitor_channel_id,
                "maxResults": 50,
                "order": "viewCount"
            })

            # Analyze content patterns
            analysis = await self.content.analyze_competitor_strategy(competitor_videos)

            return analysis

        except Exception as e:
            logger.error(f"Failed to analyze competitor {competitor_channel_id}: {e}")
            return {"error": str(e)}

    # Private helper methods
    async def _apply_video_optimizations(self, video_id: str, optimizations: Dict[str, Any]) -> bool:
        """Apply video optimizations via MCP"""
        try:
            update_data = {}

            if optimizations.get("title"):
                update_data["title"] = optimizations["title"]

            if optimizations.get("description"):
                update_data["description"] = optimizations["description"]

            if optimizations.get("tags"):
                update_data["tags"] = optimizations["tags"]

            if optimizations.get("privacyStatus"):
                update_data["privacyStatus"] = optimizations["privacyStatus"]

            if update_data:
                result = await self.mcp_client.call_tool("update_video_metadata", {
                    "videoId": video_id,
                    **update_data
                })

                return result.get("success", False)

            return True

        except Exception as e:
            logger.error(f"Failed to apply optimizations to video {video_id}: {e}")
            return False

    # Natural Language Processing Methods
    async def process_natural_language_command(self, command: str) -> Dict[str, Any]:
        """Process natural language commands for YouTube management"""
        try:
            # This would integrate with LangChain or similar NLP framework
            # For now, return a structured response

            command_lower = command.lower()

            if "analytics" in command_lower or "performance" in command_lower:
                return {
                    "action": "get_analytics",
                    "result": await self.get_performance_analytics()
                }

            elif "optimize" in command_lower and "video" in command_lower:
                # Extract video ID from command (simplified)
                return {
                    "action": "optimize_video",
                    "result": {"message": "Video optimization requires specific video ID"}
                }

            elif "search" in command_lower or "find" in command_lower:
                # Extract search query
                query = command.replace("search for", "").replace("find", "").strip()
                return {
                    "action": "search_videos",
                    "result": await self.search_videos(query)
                }

            else:
                return {
                    "action": "unknown",
                    "result": {"message": f"Could not understand command: {command}"}
                }

        except Exception as e:
            logger.error(f"Failed to process command '{command}': {e}")
            return {"error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "initialized": self.is_initialized,
            "channel_id": self.channel_id,
            "mcp_connected": self.mcp_client.is_connected if hasattr(self.mcp_client, 'is_connected') else False,
            "services": ["analytics", "content", "optimization"]
        }
