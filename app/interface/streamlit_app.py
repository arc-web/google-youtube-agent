#!/usr/bin/env python3
"""
YouTube Content Management Agent - Streamlit Web Interface

Interactive web interface for YouTube channel management and analytics.
"""

import streamlit as st
import asyncio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any, Optional

# Import agent components
from ..core.youtube_agent import YouTubeAgent
from ..core.mcp_client import MCPYouTubeClient
from ..services.analytics_service import AnalyticsService
from ..services.content_service import ContentService
from ..services.optimization_service import OptimizationService

# Configure page
st.set_page_config(
    page_title="YouTube Content Management Agent",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'channel_info' not in st.session_state:
    st.session_state.channel_info = None
if 'analytics_data' not in st.session_state:
    st.session_state.analytics_data = None

def initialize_agent():
    """Initialize the YouTube agent"""
    try:
        # Initialize MCP client
        mcp_client = MCPYouTubeClient()

        # Initialize services
        analytics_service = AnalyticsService(mcp_client)
        content_service = ContentService(mcp_client)
        optimization_service = OptimizationService(mcp_client)

        # Initialize main agent
        agent = YouTubeAgent(
            mcp_client=mcp_client,
            analytics_service=analytics_service,
            content_service=content_service,
            optimization_service=optimization_service
        )

        st.session_state.agent = agent
        return True
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        return False

async def get_channel_info_async():
    """Async wrapper for getting channel info"""
    if st.session_state.agent:
        return await st.session_state.agent.get_channel_info()
    return None

async def get_analytics_async(days: int = 30):
    """Async wrapper for getting analytics"""
    if st.session_state.agent:
        return await st.session_state.agent.get_channel_analytics(days)
    return None

def main():
    """Main Streamlit application"""
    st.title("🎬 YouTube Content Management Agent")
    st.markdown("*AI-powered YouTube channel management and optimization*")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        if st.button("🔌 Initialize Agent", type="primary"):
            with st.spinner("Initializing YouTube Agent..."):
                if initialize_agent():
                    st.success("✅ Agent initialized successfully!")
                else:
                    st.error("❌ Failed to initialize agent")

        st.divider()

        # Channel info section
        if st.session_state.agent:
            st.subheader("📺 Channel Status")

            if st.button("📊 Load Channel Info"):
                with st.spinner("Loading channel information..."):
                    try:
                        # Run async function
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        channel_info = loop.run_until_complete(get_channel_info_async())

                        if channel_info:
                            st.session_state.channel_info = channel_info
                            st.success("✅ Channel info loaded!")
                        else:
                            st.error("❌ Could not load channel info")

                    except Exception as e:
                        st.error(f"Error loading channel info: {e}")

            if st.session_state.channel_info:
                info = st.session_state.channel_info
                st.metric("Channel", info.get("snippet", {}).get("title", "Unknown"))
                st.metric("Subscribers", info.get("statistics", {}).get("subscriberCount", "Hidden"))
                st.metric("Videos", info.get("statistics", {}).get("videoCount", "0"))

    # Main content area
    if not st.session_state.agent:
        st.info("👈 Please initialize the YouTube Agent from the sidebar to get started.")
        return

    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "🎥 Content Management",
        "🔍 Analytics",
        "⚡ Optimization",
        "🤖 AI Assistant"
    ])

    with tab1:
        show_dashboard()

    with tab2:
        show_content_management()

    with tab3:
        show_analytics()

    with tab4:
        show_optimization()

    with tab5:
        show_ai_assistant()

def show_dashboard():
    """Dashboard tab"""
    st.header("📊 Channel Dashboard")

    if not st.session_state.channel_info:
        st.info("Please load your channel information from the sidebar first.")
        return

    col1, col2, col3, col4 = st.columns(4)

    info = st.session_state.channel_info
    stats = info.get("statistics", {})

    with col1:
        st.metric("Total Views", f"{int(stats.get('viewCount', 0)):,}")

    with col2:
        subscriber_count = stats.get('subscriberCount', 'Hidden')
        if subscriber_count != 'Hidden':
            st.metric("Subscribers", f"{int(subscriber_count):,}")
        else:
            st.metric("Subscribers", "Hidden")

    with col3:
        st.metric("Total Videos", f"{int(stats.get('videoCount', 0)):,}")

    with col4:
        # Calculate average views per video
        video_count = int(stats.get('videoCount', 1))
        total_views = int(stats.get('viewCount', 0))
        avg_views = total_views / video_count if video_count > 0 else 0
        st.metric("Avg Views/Video", f"{avg_views:,.0f}")

    # Recent analytics
    st.subheader("📈 Recent Performance (30 days)")

    if st.button("🔄 Load Analytics"):
        with st.spinner("Loading analytics data..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                analytics = loop.run_until_complete(get_analytics_async(30))

                if analytics:
                    st.session_state.analytics_data = analytics

                    # Display key metrics
                    metrics = analytics.get("metrics", {})
                    st.metric("Recent Views", f"{metrics.get('total_views', 0):,}")
                    st.metric("Avg Engagement", f"{metrics.get('average_engagement_rate', 0):.1%}")

                    # Show top videos
                    top_videos = analytics.get("top_videos", [])
                    if top_videos:
                        st.subheader("🏆 Top Performing Videos")
                        for i, video in enumerate(top_videos[:5], 1):
                            st.write(f"{i}. **{video['title']}** - {video['views']:,} views")

                    # Show recommendations
                    recommendations = analytics.get("recommendations", [])
                    if recommendations:
                        st.subheader("💡 Recommendations")
                        for rec in recommendations:
                            st.info(rec)

                else:
                    st.error("Could not load analytics data")

            except Exception as e:
                st.error(f"Error loading analytics: {e}")

def show_content_management():
    """Content management tab"""
    st.header("🎥 Content Management")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📹 Video Search")
        search_query = st.text_input("Search YouTube videos:")
        if st.button("🔍 Search") and search_query:
            with st.spinner("Searching videos..."):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    results = loop.run_until_complete(
                        st.session_state.agent.search_videos(search_query, max_results=10)
                    )

                    if results:
                        for video in results:
                            snippet = video.get("snippet", {})
                            stats = video.get("statistics", {})

                            with st.expander(f"🎬 {snippet.get('title', 'Unknown')}"):
                                st.write(f"**Channel:** {snippet.get('channelTitle', 'Unknown')}")
                                st.write(f"**Views:** {int(stats.get('viewCount', 0)):,}")
                                st.write(f"**Published:** {snippet.get('publishedAt', 'Unknown')[:10]}")
                                if snippet.get('description'):
                                    st.write(f"**Description:** {snippet['description'][:200]}...")

                    else:
                        st.warning("No videos found")

                except Exception as e:
                    st.error(f"Search failed: {e}")

    with col2:
        st.subheader("🎯 Content Strategy")

        if st.button("💡 Generate Content Ideas"):
            with st.spinner("Generating content suggestions..."):
                try:
                    # Mock data for demonstration - would use real channel data
                    performance_data = {"top_videos": []}
                    trending_topics = ["AI tutorials", "content creation", "video editing"]

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    suggestions = loop.run_until_complete(
                        st.session_state.agent.content.generate_content_suggestions(
                            "Technology", performance_data, trending_topics
                        )
                    )

                    if suggestions:
                        for suggestion in suggestions:
                            with st.expander(f"💡 {suggestion['title']}"):
                                st.write(f"**Type:** {suggestion['type']}")
                                st.write(f"**Expected Performance:** {suggestion['expected_performance']}")
                                st.write(f"**Estimated Views:** {suggestion['estimated_views']:,}")
                                st.write(f"**Production Time:** {suggestion['production_time']}")
                                st.write(f"**Reasoning:** {suggestion['reasoning']}")

                    else:
                        st.warning("No suggestions generated")

                except Exception as e:
                    st.error(f"Content generation failed: {e}")

def show_analytics():
    """Analytics tab"""
    st.header("🔍 Advanced Analytics")

    if not st.session_state.analytics_data:
        st.info("Please load analytics data from the Dashboard first.")
        return

    analytics = st.session_state.analytics_data

    # Performance breakdown
    st.subheader("📈 Performance Breakdown")

    perf_breakdown = analytics.get("performance_breakdown", {})

    col1, col2 = st.columns(2)

    with col1:
        # Publishing patterns
        pub_patterns = analytics.get("publishing_patterns", {})
        st.metric("Best Publish Day", pub_patterns.get("best_publish_day", "Unknown"))
        st.metric("Best Publish Time", pub_patterns.get("best_publish_hour", "Unknown"))

    with col2:
        # Growth metrics
        growth = analytics.get("growth", {})
        growth_rate = growth.get("view_growth_rate", 0)
        st.metric("View Growth Rate", f"{growth_rate:.1f}%")
        st.metric("Growth Trend", growth.get("trend", "Unknown").title())

    # Trends
    st.subheader("📊 Trends Analysis")

    trends = analytics.get("trends", {})
    views_trend = trends.get("views", {})

    if views_trend:
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Recent Avg Views", f"{views_trend.get('recent_avg', 0):,.0f}")
            st.metric("Previous Avg Views", f"{views_trend.get('previous_avg', 0):,.0f}")

        with col2:
            change_pct = views_trend.get('change_percent', 0)
            st.metric("Change %", f"{change_pct:.1f}%")
            st.metric("Trend Direction", views_trend.get('trend', 'stable').title())

def show_optimization():
    """Optimization tab"""
    st.header("⚡ Content Optimization")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Title Optimization")

        current_title = st.text_input("Current video title:")
        target_topic = st.text_input("Video topic:")
        target_audience = st.text_input("Target audience:")

        if st.button("🔧 Optimize Title") and current_title:
            with st.spinner("Optimizing title..."):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    optimized = loop.run_until_complete(
                        st.session_state.agent.optimize_title(
                            current_title, target_topic, target_audience
                        )
                    )

                    st.success("✅ Title optimized!")
                    st.write(f"**Optimized Title:** {optimized}")
                    st.info("💡 This optimization is based on YouTube SEO best practices")

                except Exception as e:
                    st.error(f"Optimization failed: {e}")

    with col2:
        st.subheader("📄 Description Generator")

        video_topic = st.text_input("Video topic (for description):")
        key_points = st.text_area("Key points (one per line):")
        target_keywords = st.text_input("Target keywords (comma-separated):")

        if st.button("📝 Generate Description") and video_topic:
            with st.spinner("Generating description..."):
                try:
                    key_points_list = [point.strip() for point in key_points.split('\n') if point.strip()]
                    keywords_list = [kw.strip() for kw in target_keywords.split(',') if kw.strip()]

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    description = loop.run_until_complete(
                        st.session_state.agent.generate_description(
                            video_topic, key_points_list, keywords_list
                        )
                    )

                    st.success("✅ Description generated!")
                    st.text_area("Generated Description:", description, height=200)

                except Exception as e:
                    st.error(f"Description generation failed: {e}")

def show_ai_assistant():
    """AI Assistant tab"""
    st.header("🤖 AI Content Assistant")

    st.markdown("Get AI-powered recommendations and assistance for your YouTube channel.")

    # Natural language command input
    user_command = st.text_area(
        "What would you like to know or do?",
        placeholder="Example: 'Analyze my top performing videos' or 'Suggest content ideas for tech tutorials'",
        height=100
    )

    if st.button("🚀 Process Command", type="primary") and user_command:
        with st.spinner("Processing your request..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    st.session_state.agent.process_natural_language_command(user_command)
                )

                if result:
                    action = result.get("action", "unknown")
                    response_data = result.get("result", {})

                    if action == "get_analytics":
                        st.success("📊 Analytics Retrieved!")
                        if "metrics" in response_data:
                            metrics = response_data["metrics"]
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Total Views", f"{metrics.get('total_views', 0):,}")
                            col2.metric("Avg Engagement", f"{metrics.get('average_engagement_rate', 0):.1%}")
                            col3.metric("Videos Analyzed", metrics.get('total_videos_analyzed', 0))

                    elif action == "search_videos":
                        st.success("🔍 Search Results!")
                        videos = response_data
                        if videos:
                            for video in videos[:5]:
                                snippet = video.get("snippet", {})
                                st.write(f"🎬 **{snippet.get('title', 'Unknown')}**")
                                st.write(f"👤 {snippet.get('channelTitle', 'Unknown')} - 👀 {video.get('statistics', {}).get('viewCount', 0):,} views")
                                st.divider()
                        else:
                            st.info("No videos found matching your search.")

                    else:
                        st.info(f"Command processed: {action}")
                        st.json(response_data)

                else:
                    st.warning("Could not process your command. Please try rephrasing.")

            except Exception as e:
                st.error(f"Command processing failed: {e}")

    # Quick action buttons
    st.subheader("⚡ Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📈 Show Performance"):
            st.info("💡 Try: 'Show me my channel performance'")

    with col2:
        if st.button("💡 Content Ideas"):
            st.info("💡 Try: 'Suggest content ideas for my niche'")

    with col3:
        if st.button("🔍 Analyze Competitors"):
            st.info("💡 Try: 'Analyze competitor content strategies'")

if __name__ == "__main__":
    main()
