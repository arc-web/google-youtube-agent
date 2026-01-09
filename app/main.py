#!/usr/bin/env python3
"""
YouTube Content Management Agent - Main Application

FastAPI-based YouTube management platform with MCP integration.
"""

import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Dict, Any, Optional
import logging

# Import agent components
from .core.youtube_agent import YouTubeAgent
from .core.mcp_client import MCPYouTubeClient
from .models.video import Video, VideoAnalytics
from .models.channel import Channel, ChannelAnalytics
from .services.analytics_service import AnalyticsService
from .services.content_service import ContentService
from .services.optimization_service import OptimizationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global agent instance
youtube_agent: Optional[YouTubeAgent] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global youtube_agent

    # Startup
    logger.info("Starting YouTube Content Management Agent...")

    try:
        # Initialize MCP client
        mcp_client = MCPYouTubeClient()

        # Initialize services
        analytics_service = AnalyticsService(mcp_client)
        content_service = ContentService(mcp_client)
        optimization_service = OptimizationService(mcp_client)

        # Initialize main agent
        youtube_agent = YouTubeAgent(
            mcp_client=mcp_client,
            analytics_service=analytics_service,
            content_service=content_service,
            optimization_service=optimization_service
        )

        logger.info("YouTube Agent initialized successfully")

        yield

    except Exception as e:
        logger.error(f"Failed to initialize YouTube Agent: {e}")
        raise

    finally:
        # Shutdown
        logger.info("Shutting down YouTube Agent...")

# Create FastAPI app
app = FastAPI(
    title="YouTube Content Management Agent",
    description="AI-powered YouTube channel management platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "YouTube Content Management Agent",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        auth_status = await youtube_agent.check_auth_status()
        return {
            "status": "healthy",
            "agent_status": "operational",
            "mcp_connection": auth_status.get("authenticated", False),
            "services": ["analytics", "content", "optimization"]
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

# Channel Management Endpoints
@app.get("/api/channel/info")
async def get_channel_info():
    """Get channel information"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    try:
        channel_info = await youtube_agent.get_channel_info()
        return channel_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get channel info: {str(e)}")

@app.get("/api/channel/analytics")
async def get_channel_analytics():
    """Get channel analytics"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    try:
        analytics = await youtube_agent.get_channel_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get channel analytics: {str(e)}")

# Video Management Endpoints
@app.get("/api/videos")
async def get_videos(limit: int = 50, offset: int = 0):
    """Get channel videos"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    try:
        videos = await youtube_agent.get_channel_videos(limit=limit, offset=offset)
        return {"videos": videos, "count": len(videos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get videos: {str(e)}")

@app.get("/api/videos/{video_id}")
async def get_video_details(video_id: str):
    """Get specific video details"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    try:
        video_details = await youtube_agent.get_video_details(video_id)
        return video_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get video details: {str(e)}")

@app.post("/api/videos/{video_id}/optimize")
async def optimize_video(video_id: str, background_tasks: BackgroundTasks):
    """Optimize video metadata"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    try:
        # Start optimization in background
        background_tasks.add_task(youtube_agent.optimize_video, video_id)
        return {"status": "optimization_started", "video_id": video_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start optimization: {str(e)}")

# Content Analysis Endpoints
@app.get("/api/analytics/performance")
async def get_performance_analytics(days: int = 30):
    """Get performance analytics"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    try:
        analytics = await youtube_agent.get_performance_analytics(days=days)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

@app.get("/api/analytics/trends")
async def get_content_trends():
    """Get content trend analysis"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    try:
        trends = await youtube_agent.analyze_content_trends()
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze trends: {str(e)}")

# AI-Powered Endpoints
@app.post("/api/ai/optimize-title")
async def optimize_title(data: Dict[str, Any]):
    """AI-powered title optimization"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    try:
        current_title = data.get("title", "")
        video_topic = data.get("topic", "")
        target_audience = data.get("audience", "")

        optimized_title = await youtube_agent.optimize_title(
            current_title, video_topic, target_audience
        )
        return {"original_title": current_title, "optimized_title": optimized_title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to optimize title: {str(e)}")

@app.post("/api/ai/generate-description")
async def generate_description(data: Dict[str, Any]):
    """AI-powered description generation"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    try:
        video_topic = data.get("topic", "")
        key_points = data.get("key_points", [])
        target_keywords = data.get("keywords", [])

        description = await youtube_agent.generate_description(
            video_topic, key_points, target_keywords
        )
        return {"description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate description: {str(e)}")

@app.post("/api/ai/suggest-content")
async def suggest_content(data: Dict[str, Any]):
    """AI-powered content suggestions"""
    if not youtube_agent:
        raise HTTPException(status_code=503, detail="Agent not available")

    try:
        channel_niche = data.get("niche", "")
        recent_performance = data.get("performance", {})
        trending_topics = data.get("trends", [])

        suggestions = await youtube_agent.suggest_content_ideas(
            channel_niche, recent_performance, trending_topics
        )
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to suggest content: {str(e)}")

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
