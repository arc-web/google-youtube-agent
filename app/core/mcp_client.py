#!/usr/bin/env python3
"""
MCP YouTube Client

Client for communicating with the YouTube Data API v3 MCP server.
Handles tool calls and response processing.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
import aiohttp
from aiohttp import ClientSession, ClientTimeout
import os

logger = logging.getLogger(__name__)

class MCPYouTubeClient:
    """
    MCP Client for YouTube Data API v3

    Communicates with the YouTube MCP server to execute tools and retrieve data.
    """

    def __init__(self, server_url: str = None):
        """
        Initialize MCP YouTube client

        Args:
            server_url: URL of the MCP server (optional, uses env var if not provided)
        """
        self.server_url = server_url or os.getenv(
            "MCP_YOUTUBE_SERVER_URL",
            "http://localhost:3000"  # Default MCP server URL
        )
        self.session: Optional[ClientSession] = None
        self.timeout = ClientTimeout(total=30)  # 30 second timeout
        self.connected = False

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()

    async def connect(self) -> bool:
        """Establish connection to MCP server"""
        try:
            if self.session:
                return True

            self.session = ClientSession(timeout=self.timeout)

            # Test connection by checking if server is responsive
            async with self.session.get(f"{self.server_url}/health") as response:
                if response.status == 200:
                    self.connected = True
                    logger.info(f"Connected to YouTube MCP server at {self.server_url}")
                    return True
                else:
                    logger.warning(f"MCP server health check failed with status {response.status}")
                    return False

        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            return False

    async def disconnect(self):
        """Close connection to MCP server"""
        if self.session:
            await self.session.close()
            self.session = None
            self.connected = False
            logger.info("Disconnected from YouTube MCP server")

    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a YouTube MCP tool

        Args:
            tool_name: Name of the tool to call
            parameters: Tool parameters

        Returns:
            Tool execution result
        """
        if not self.session:
            await self.connect()

        if not self.connected:
            raise ConnectionError("Not connected to MCP server")

        try:
            # Prepare MCP protocol request
            request_payload = {
                "jsonrpc": "2.0",
                "id": f"call_{tool_name}_{asyncio.get_event_loop().time()}",
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": parameters
                }
            }

            logger.debug(f"Calling MCP tool '{tool_name}' with params: {parameters}")

            # Make request to MCP server
            async with self.session.post(
                f"{self.server_url}/mcp",
                json=request_payload,
                headers={"Content-Type": "application/json"}
            ) as response:

                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"MCP server error {response.status}: {error_text}")

                response_data = await response.json()

                # Extract tool result from MCP response
                if "result" in response_data:
                    result = response_data["result"]
                    if "content" in result and len(result["content"]) > 0:
                        # Parse the text content (assuming JSON format)
                        content = result["content"][0]
                        if content.get("type") == "text":
                            try:
                                # Try to parse as JSON first
                                return json.loads(content["text"])
                            except json.JSONDecodeError:
                                # If not JSON, return as raw text
                                return {"raw_response": content["text"], "success": True}
                    return result
                elif "content" in response_data and len(response_data["content"]) > 0:
                    # Handle direct content response (our HTTP wrapper format)
                    content = response_data["content"][0]
                    if content.get("type") == "text":
                        try:
                            parsed = json.loads(content["text"])
                            return parsed
                        except json.JSONDecodeError:
                            return {"raw_response": content["text"], "success": True}
                # Handle the case where response_data itself is the content structure
                if "content" in response_data and len(response_data["content"]) > 0:
                    content = response_data["content"][0]
                    if content.get("type") == "text":
                        try:
                            parsed = json.loads(content["text"])
                            return parsed
                        except json.JSONDecodeError:
                            return {"raw_response": content["text"], "success": True}

                elif "error" in response_data:
                    raise Exception(f"MCP tool error: {response_data['error']}")

                else:
                    raise Exception(f"Unexpected MCP response format: {response_data}")

        except Exception as e:
            logger.error(f"Failed to call MCP tool '{tool_name}': {e}")
            raise

    # High-level convenience methods for common operations

    async def search_videos(self, query: str, max_results: int = 25,
                          order: str = "relevance") -> List[Dict[str, Any]]:
        """Search for videos"""
        result = await self.call_tool("search_videos", {
            "query": query,
            "maxResults": max_results,
            "order": order
        })

        if result.get("success") and result.get("data", {}).get("items"):
            return result["data"]["items"]
        return []

    async def get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """Get video details"""
        result = await self.call_tool("get_video_details", {
            "videoIds": video_ids,
            "parts": ["snippet", "statistics", "contentDetails"]
        })

        if result.get("success") and result.get("data", {}).get("items"):
            return result["data"]["items"]
        return []

    async def get_channel_info(self, channel_id: str = None, mine: bool = False) -> Optional[Dict[str, Any]]:
        """Get channel information"""
        params = {}
        if mine:
            params["mine"] = True
        elif channel_id:
            params["channelId"] = channel_id

        result = await self.call_tool("get_channel_info", params)

        if result.get("success") and result.get("data"):
            return result["data"]
        return None

    async def get_playlist_videos(self, playlist_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Get videos from a playlist"""
        result = await self.call_tool("get_playlist_videos", {
            "playlistId": playlist_id,
            "maxResults": max_results
        })

        if result.get("success") and result.get("data", {}).get("items"):
            return result["data"]["items"]
        return []

    async def get_channel_playlists(self, channel_id: str, max_results: int = 25) -> List[Dict[str, Any]]:
        """Get channel playlists"""
        result = await self.call_tool("get_channel_playlists", {
            "channelId": channel_id,
            "maxResults": max_results
        })

        if result.get("success") and result.get("data", {}).get("items"):
            return result["data"]["items"]
        return []

    async def get_video_comments(self, video_id: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Get video comments"""
        result = await self.call_tool("get_video_comments", {
            "videoId": video_id,
            "maxResults": max_results
        })

        if result.get("success") and result.get("data", {}).get("items"):
            return result["data"]["items"]
        return []

    async def update_video_metadata(self, video_id: str, updates: Dict[str, Any]) -> bool:
        """Update video metadata"""
        params = {"videoId": video_id, **updates}
        result = await self.call_tool("update_video_metadata", params)
        return result.get("success", False)

    async def check_auth_status(self) -> Dict[str, Any]:
        """Check authentication status"""
        return await self.call_tool("get_auth_status", {})

    # Utility methods

    def is_connected(self) -> bool:
        """Check if connected to MCP server"""
        return self.connected

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on MCP server"""
        try:
            if not self.session:
                return {"status": "disconnected"}

            async with self.session.get(f"{self.server_url}/health") as response:
                if response.status == 200:
                    health_data = await response.json()
                    return {"status": "healthy", **health_data}
                else:
                    return {"status": "unhealthy", "http_status": response.status}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools"""
        try:
            result = await self.call_tool("tools/list", {})
            if result.get("tools"):
                return result["tools"]
            return []
        except Exception as e:
            logger.error(f"Failed to get available tools: {e}")
            return []

    # Batch operations for efficiency

    async def batch_get_video_details(self, video_ids: List[str], batch_size: int = 50) -> List[Dict[str, Any]]:
        """Get video details in batches to handle large requests"""
        all_videos = []

        for i in range(0, len(video_ids), batch_size):
            batch = video_ids[i:i + batch_size]
            videos = await self.get_video_details(batch)
            all_videos.extend(videos)

            # Small delay to avoid rate limiting
            if i + batch_size < len(video_ids):
                await asyncio.sleep(0.1)

        return all_videos

    async def search_with_pagination(self, query: str, max_results: int = 100,
                                   order: str = "relevance") -> List[Dict[str, Any]]:
        """Search with pagination to get more results"""
        all_results = []
        page_size = 50  # YouTube API max per request

        while len(all_results) < max_results:
            remaining = max_results - len(all_results)
            current_batch = min(remaining, page_size)

            results = await self.search_videos(query, current_batch, order)
            all_results.extend(results)

            # Break if we got fewer results than requested (no more pages)
            if len(results) < current_batch:
                break

        return all_results[:max_results]
