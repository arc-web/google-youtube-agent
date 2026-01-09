# 🎬 YouTube MCP Integration Guide

Complete guide for integrating and using the YouTube Data API v3 MCP server with the YouTube Content Management Agent.

## 📋 Table of Contents

- [Overview](#overview)
- [MCP Server Setup](#mcp-server-setup)
- [Agent Integration](#agent-integration)
- [Available MCP Tools](#available-mcp-tools)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)

## 🎯 Overview

The YouTube Content Management Agent integrates with the YouTube Data API v3 through a Model Context Protocol (MCP) server. This architecture provides:

- **Secure API Access**: OAuth 2.0 authenticated access to YouTube API
- **Tool-Based Interface**: Standardized tool calls for different YouTube operations
- **Error Handling**: Robust error handling and retry logic
- **Rate Limiting**: Built-in rate limiting and quota management
- **Caching**: Intelligent caching of API responses

## 🔧 MCP Server Setup

### Prerequisites

- Node.js 18+
- Google Cloud Project with YouTube Data API v3 enabled
- OAuth 2.0 credentials configured

### 1. Install YouTube MCP Server

```bash
# Navigate to MCP tools directory
cd 7_tools/mcp_tools/servers/youtube_mcp

# Install dependencies
npm install

# Build the server
npm run build
```

### 2. Configure OAuth Credentials

```bash
# Run OAuth setup automation
npm run setup:oauth

# Follow the browser prompts to:
# 1. Create/select Google Cloud Project
# 2. Enable YouTube Data API v3
# 3. Configure OAuth consent screen
# 4. Create OAuth 2.0 credentials
# 5. Download credentials.json
```

### 3. Store Credentials Securely

```bash
# Store credentials in Supabase (recommended)
npm run setup:credentials

# Or manually place credentials.json in config directory
cp ~/Downloads/credentials.json config/credentials.json
```

### 4. Test MCP Server

```bash
# Test basic connectivity
npm run test:connection

# Test individual tools
npm run test:tools

# Run full smoke test
npm run test:smoke
```

### 5. Configure Claude Desktop

Add the YouTube MCP server to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "youtube": {
      "command": "node",
      "args": ["/Users/home/aimacpro/7_tools/mcp_tools/servers/youtube_mcp/dist/server.js"],
      "env": {
        "YOUTUBE_CREDENTIALS_PATH": "/Users/home/aimacpro/7_tools/mcp_tools/servers/youtube_mcp/config/credentials.json"
      }
    }
  }
}
```

## 🤖 Agent Integration

### Basic Integration

```python
from app.core.youtube_agent import YouTubeAgent
from app.core.mcp_client import MCPYouTubeClient
from app.services.analytics_service import AnalyticsService
from app.services.content_service import ContentService
from app.services.optimization_service import OptimizationService

# Initialize MCP client
mcp_client = MCPYouTubeClient()

# Initialize services
analytics = AnalyticsService(mcp_client)
content = ContentService(mcp_client)
optimization = OptimizationService(mcp_client)

# Initialize main agent
agent = YouTubeAgent(mcp_client, analytics, content, optimization)

# Initialize and verify connection
await agent.initialize()
```

### FastAPI Integration

```python
from fastapi import FastAPI
from app.core.youtube_agent import YouTubeAgent

app = FastAPI()
agent = None

@app.on_event("startup")
async def startup_event():
    global agent
    # Initialize agent (see above)
    agent = YouTubeAgent(...)
    await agent.initialize()

@app.get("/api/channel/info")
async def get_channel_info():
    channel_info = await agent.get_channel_info()
    return channel_info
```

### Streamlit Integration

```python
import streamlit as st
from app.core.youtube_agent import YouTubeAgent

if 'agent' not in st.session_state:
    # Initialize agent
    st.session_state.agent = YouTubeAgent(...)

agent = st.session_state.agent

# Use agent methods
if st.button("Load Channel Info"):
    with st.spinner("Loading..."):
        info = await agent.get_channel_info()
        st.write(info)
```

## 🔨 Available MCP Tools

The YouTube MCP server provides 9 core tools:

### 1. `search_videos`
Search for YouTube videos by query.

**Parameters:**
- `query` (string, required): Search query
- `maxResults` (number, optional): Maximum results (default: 10)
- `order` (string, optional): Sort order (relevance, date, rating, title, videoCount, viewCount)
- `channelId` (string, optional): Channel ID to search within

**Example:**
```python
results = await mcp_client.call_tool("search_videos", {
    "query": "Python tutorials",
    "maxResults": 25,
    "order": "viewCount"
})
```

### 2. `get_video_details`
Get detailed information about specific videos.

**Parameters:**
- `videoIds` (array, required): Array of video IDs
- `parts` (array, optional): Data parts to retrieve (snippet, statistics, contentDetails, status)

**Example:**
```python
details = await mcp_client.call_tool("get_video_details", {
    "videoIds": ["VIDEO_ID_1", "VIDEO_ID_2"],
    "parts": ["snippet", "statistics", "contentDetails"]
})
```

### 3. `get_channel_info`
Get information about a YouTube channel.

**Parameters:**
- `channelId` (string, optional): Channel ID
- `username` (string, optional): Channel username
- `mine` (boolean, optional): Get authenticated user's channel

**Example:**
```python
channel = await mcp_client.call_tool("get_channel_info", {
    "mine": true  # Get authenticated user's channel
})
```

### 4. `get_playlist_videos`
Get videos from a YouTube playlist.

**Parameters:**
- `playlistId` (string, required): Playlist ID
- `maxResults` (number, optional): Maximum results (default: 50)

**Example:**
```python
videos = await mcp_client.call_tool("get_playlist_videos", {
    "playlistId": "PLAYLIST_ID",
    "maxResults": 100
})
```

### 5. `get_channel_playlists`
Get playlists for a channel.

**Parameters:**
- `channelId` (string, required): Channel ID
- `maxResults` (number, optional): Maximum results (default: 50)

**Example:**
```python
playlists = await mcp_client.call_tool("get_channel_playlists", {
    "channelId": "CHANNEL_ID",
    "maxResults": 25
})
```

### 6. `get_video_comments`
Get comments for a video.

**Parameters:**
- `videoId` (string, required): Video ID
- `maxResults` (number, optional): Maximum results (default: 20)
- `order` (string, optional): Sort order (relevance, time)

**Example:**
```python
comments = await mcp_client.call_tool("get_video_comments", {
    "videoId": "VIDEO_ID",
    "maxResults": 50,
    "order": "relevance"
})
```

### 7. `update_video_metadata`
Update video metadata (requires ownership).

**Parameters:**
- `videoId` (string, required): Video ID to update
- `title` (string, optional): New title
- `description` (string, optional): New description
- `tags` (array, optional): New tags
- `privacyStatus` (string, optional): Privacy status (public, private, unlisted)

**Example:**
```python
result = await mcp_client.call_tool("update_video_metadata", {
    "videoId": "VIDEO_ID",
    "title": "New Optimized Title",
    "description": "New SEO description",
    "tags": ["tag1", "tag2", "tag3"],
    "privacyStatus": "public"
})
```

### 8. `delete_video`
Delete a video (requires ownership).

**Parameters:**
- `videoId` (string, required): Video ID to delete

**Example:**
```python
result = await mcp_client.call_tool("delete_video", {
    "videoId": "VIDEO_ID"
})
```

### 9. `get_auth_status`
Check YouTube API authentication status.

**Parameters:** None

**Example:**
```python
status = await mcp_client.call_tool("get_auth_status", {})
```

## 💡 Usage Examples

### Channel Analytics Dashboard

```python
async def create_channel_dashboard():
    # Get channel info
    channel = await mcp_client.get_channel_info(mine=True)

    # Get recent videos
    videos = await mcp_client.search_videos("", {
        "channelId": channel["id"],
        "maxResults": 50,
        "order": "date"
    })

    # Calculate metrics
    total_views = sum(int(v.get("statistics", {}).get("viewCount", 0)) for v in videos)
    total_likes = sum(int(v.get("statistics", {}).get("likeCount", 0)) for v in videos)

    print(f"Channel: {channel['snippet']['title']}")
    print(f"Total Views: {total_views:,}")
    print(f"Total Likes: {total_likes:,}")
    print(f"Videos Analyzed: {len(videos)}")
```

### Content Optimization Workflow

```python
async def optimize_video_content(video_id: str):
    # Get current video details
    video_details = (await mcp_client.get_video_details([video_id]))[0]

    # Get comments for sentiment analysis
    comments = await mcp_client.get_video_comments(video_id, max_results=100)

    # Analyze performance
    views = int(video_details.get("statistics", {}).get("viewCount", 0))
    likes = int(video_details.get("statistics", {}).get("likeCount", 0))

    engagement_rate = likes / views if views > 0 else 0

    # Generate optimization suggestions
    suggestions = []

    if engagement_rate < 0.02:
        suggestions.append("Consider improving thumbnail and title for better engagement")

    current_title = video_details.get("snippet", {}).get("title", "")
    if len(current_title) < 30:
        suggestions.append("Title might be too short for SEO")

    # Apply optimizations
    if suggestions:
        optimized_title = f"{current_title} - Complete Guide"
        await mcp_client.update_video_metadata(video_id, {
            "title": optimized_title,
            "tags": ["tutorial", "guide", "how-to"]  # Add relevant tags
        })

    return {
        "video_id": video_id,
        "current_engagement": engagement_rate,
        "suggestions": suggestions
    }
```

### Competitor Analysis

```python
async def analyze_competitor_channel(competitor_channel_id: str):
    # Get competitor channel info
    competitor = await mcp_client.get_channel_info(channel_id=competitor_channel_id)

    # Get their top videos
    top_videos = await mcp_client.search_videos("", {
        "channelId": competitor_channel_id,
        "maxResults": 20,
        "order": "viewCount"
    })

    # Analyze content patterns
    titles = [v.get("snippet", {}).get("title", "") for v in top_videos]

    # Simple pattern analysis
    question_titles = sum(1 for title in titles if "?" in title)
    numbered_titles = sum(1 for title in titles if any(char.isdigit() for char in title))

    return {
        "channel": competitor["snippet"]["title"],
        "question_titles_percent": (question_titles / len(titles)) * 100,
        "numbered_titles_percent": (numbered_titles / len(titles)) * 100,
        "top_video_views": int(top_videos[0].get("statistics", {}).get("viewCount", 0)) if top_videos else 0
    }
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Authentication Errors

**Error:** `"Authentication failed"`
```json
{
  "success": false,
  "error": "Authentication failed"
}
```

**Solutions:**
- Verify credentials.json file exists and is valid
- Check OAuth token hasn't expired
- Re-run OAuth setup: `npm run setup:oauth`
- Ensure YouTube Data API v3 is enabled in Google Cloud Console

#### 2. Quota Exceeded

**Error:** `"Quota exceeded"`
```json
{
  "success": false,
  "error": "YouTube API quota exceeded"
}
```

**Solutions:**
- Check Google Cloud Console for quota usage
- Implement request batching to reduce API calls
- Use caching to avoid repeated requests
- Consider upgrading to higher quota limits

#### 3. Invalid Video ID

**Error:** `"Video not found"`
```json
{
  "success": false,
  "error": "Video VIDEO_ID not found"
}
```

**Solutions:**
- Verify video ID is correct and public
- Check if video is private or deleted
- Ensure video exists and is accessible

#### 4. Network Connectivity

**Error:** `"Connection failed"`
```json
{
  "success": false,
  "error": "Failed to connect to MCP server"
}
```

**Solutions:**
- Verify MCP server is running: `npm test`
- Check server URL in configuration
- Ensure firewall allows connections
- Try restarting MCP server

### Debug Mode

Enable debug logging for detailed error information:

```bash
# Set environment variable
export DEBUG=youtube_mcp

# Run with debug logging
node dist/server.js
```

### Health Checks

```python
# Check MCP server health
async def check_mcp_health():
    try:
        status = await mcp_client.check_auth_status()
        return status.get("authenticated", False)
    except Exception as e:
        print(f"MCP health check failed: {e}")
        return False
```

## ⚙️ Advanced Configuration

### Custom MCP Server Configuration

```json
{
  "mcpServers": {
    "youtube": {
      "command": "node",
      "args": ["/path/to/youtube_mcp/dist/server.js"],
      "env": {
        "YOUTUBE_CREDENTIALS_PATH": "/path/to/credentials.json",
        "YOUTUBE_API_KEY": "your-api-key",
        "DEBUG": "youtube_mcp",
        "LOG_LEVEL": "debug"
      }
    }
  }
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `YOUTUBE_CREDENTIALS_PATH` | Path to OAuth credentials | `~/.youtube-mcp/credentials.json` |
| `MCP_YOUTUBE_SERVER_URL` | MCP server URL | `http://localhost:3000` |
| `DEBUG` | Enable debug logging | `false` |
| `LOG_LEVEL` | Logging level | `info` |
| `YOUTUBE_API_KEY` | API key for public requests | None |

### Rate Limiting Configuration

```yaml
# config/settings.yaml
google_youtube_agent:
  rate_limiting:
    requests_per_minute: 60
    burst_limit: 10
    backoff_factor: 2
    max_retries: 3
```

### Caching Configuration

```yaml
# config/settings.yaml
google_youtube_agent:
  caching:
    enabled: true
    ttl_seconds: 3600  # 1 hour
    max_size_mb: 100
    redis_url: "redis://localhost:6379"  # Optional
```

### Monitoring and Metrics

```python
# Enable metrics collection
import time
from functools import wraps

def track_api_call(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            # Log metrics
            print(f"API call {func.__name__}: {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            print(f"API call {func.__name__} failed: {duration:.2f}s - {e}")
            raise
    return wrapper
```

## 📊 Performance Optimization

### Batch Operations

```python
# Batch video details retrieval
video_ids = ["id1", "id2", "id3", "id4", "id5"]
batch_size = 50

all_details = []
for i in range(0, len(video_ids), batch_size):
    batch = video_ids[i:i + batch_size]
    details = await mcp_client.get_video_details(batch)
    all_details.extend(details)

    # Rate limiting delay
    await asyncio.sleep(0.1)
```

### Intelligent Caching

```python
from cachetools import TTLCache
import asyncio

class YouTubeCache:
    def __init__(self, ttl_seconds=3600):
        self.cache = TTLCache(maxsize=1000, ttl=ttl_seconds)

    async def get_or_fetch(self, key, fetch_func):
        if key in self.cache:
            return self.cache[key]

        result = await fetch_func()
        self.cache[key] = result
        return result

# Usage
cache = YouTubeCache()

video_details = await cache.get_or_fetch(
    f"video_{video_id}",
    lambda: mcp_client.get_video_details([video_id])
)
```

## 🔐 Security Best Practices

### Credential Management

- Store credentials securely (avoid committing to version control)
- Use environment variables for sensitive data
- Rotate OAuth tokens regularly
- Implement proper access controls

### API Usage

- Monitor quota usage regularly
- Implement exponential backoff for retries
- Use batch operations when possible
- Cache responses to reduce API calls

### Error Handling

```python
async def safe_api_call(tool_name, params, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await mcp_client.call_tool(tool_name, params)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            wait_time = 2 ** attempt  # Exponential backoff
            await asyncio.sleep(wait_time)
```

This comprehensive guide covers all aspects of YouTube MCP integration. For additional support, check the troubleshooting section or create an issue in the project repository.
