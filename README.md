# 🎬 YouTube Content Management Agent

An AI-powered YouTube management platform that integrates with the YouTube Data API v3 through MCP (Model Context Protocol) to provide comprehensive content management, analytics, and optimization capabilities.

## 🎯 Overview

**Purpose**: Complete YouTube channel management and content optimization  
**Scope**: Video management, analytics, audience engagement, and content strategy  
**Authority Level**: Platform-specific - reports to Marketing/Development Orchestrators  
**Integration**: MCP-powered YouTube Data API v3 integration

## ✨ Key Features

### 🎥 Content Management
- **Video Upload & Management**: Automated video publishing with metadata optimization
- **Playlist Organization**: Intelligent playlist creation and content categorization
- **Thumbnail & Metadata**: AI-generated thumbnails and SEO-optimized descriptions
- **Bulk Operations**: Batch video updates, scheduling, and management

### 📊 Analytics & Insights
- **Performance Tracking**: Real-time video analytics and engagement metrics
- **Audience Analysis**: Demographics, watch time, and retention analytics
- **Trend Analysis**: Content performance trends and optimization recommendations
- **Revenue Insights**: Monetization performance and optimization suggestions

### 🤖 AI-Powered Optimization
- **Content Strategy**: AI-driven content recommendations and topic suggestions
- **SEO Optimization**: Title, description, and tag optimization for discoverability
- **Engagement Boosting**: Automated engagement strategies and community management
- **A/B Testing**: Video thumbnail and title testing for optimal performance

### 🔄 Automated Workflows
- **Upload Automation**: Scheduled content publishing and cross-platform distribution
- **Engagement Automation**: Automated responses to comments and community management
- **Performance Monitoring**: Real-time alerts for video performance and issues
- **Content Lifecycle**: Automated content archiving and cleanup

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   API Gateway   │    │   AI Engine     │
│   (Streamlit)   │◄──►│   (FastAPI)     │◄──►│   (LangChain)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP YouTube   │    │   Content       │    │   Analytics     │
│   Integration   │◄──►│   Management    │◄──►│   Engine        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- YouTube Data API v3 access enabled
- Google Cloud Project with OAuth 2.0 credentials
- MCP YouTube server configured

### Installation

1. **Navigate to agent directory**
   ```bash
   cd 4_agents/platform_agents/google_agents/google_youtube_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r ../../../shared/dependencies/google_youtube_agent.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your YouTube API credentials
   ```

4. **Set up MCP integration**
   ```bash
   # Ensure YouTube MCP is configured in Claude Desktop
   # See MCP setup instructions below
   ```

5. **Run the agent**
   ```bash
   # Start the web interface
   streamlit run app/interface/streamlit_app.py

   # Or start the API server
   python -m uvicorn app.main:app --reload
   ```

## 🔧 MCP Integration Setup

### 1. YouTube MCP Configuration

The YouTube agent integrates with the YouTube Data API v3 MCP server:

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

### 2. OAuth Setup

```bash
# Navigate to YouTube MCP directory
cd 7_tools/mcp_tools/servers/youtube_mcp

# Run OAuth setup
npm run setup:oauth

# Store credentials
npm run setup:credentials

# Build and test
npm run build && npm test
```

### 3. Available MCP Tools

The agent leverages these YouTube MCP tools:

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `search_videos` | Find videos by query | Search for trending content |
| `get_video_details` | Get video metadata | Analyze competitor videos |
| `get_channel_info` | Channel analytics | Monitor channel performance |
| `get_playlist_videos` | Playlist content | Analyze series performance |
| `get_video_comments` | Engagement data | Community sentiment analysis |
| `update_video_metadata` | Content optimization | A/B test titles/descriptions |
| `get_auth_status` | Connection verification | Health checks |

## 📖 Usage Examples

### Natural Language Commands

```python
# Content Analysis
"Analyze my top performing videos this month"
"Find videos similar to my most successful content"
"Show me engagement trends across my channel"

# Content Optimization
"Optimize titles for my latest video series"
"Generate thumbnail ideas for tech review videos"
"Suggest tags for my cooking tutorial"

# Audience Insights
"Who is watching my content and when?"
"What topics are my viewers most interested in?"
"Show me subscriber demographics"

# Automated Workflows
"Schedule my video series for the next month"
"Respond to comments on my latest video"
"Archive videos older than 2 years"
```

### API Integration Examples

```python
from youtube_agent import YouTubeAgent

agent = YouTubeAgent()

# Get channel analytics
analytics = await agent.get_channel_analytics()
print(f"Subscriber count: {analytics.subscriber_count}")
print(f"Total views: {analytics.total_views}")

# Analyze video performance
videos = await agent.get_top_videos(limit=10)
for video in videos:
    print(f"{video.title}: {video.view_count} views")

# Optimize content
optimization = await agent.optimize_video_title("My Video Title")
print(f"Suggested title: {optimization.title}")
print(f"SEO score: {optimization.seo_score}")
```

## 🔧 Configuration

### Environment Variables

```bash
# YouTube API Configuration
YOUTUBE_CREDENTIALS_PATH=/path/to/youtube/credentials.json
YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxxxx

# AI/ML Configuration
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/google_youtube_agent

# MCP Configuration
MCP_YOUTUBE_SERVER_URL=http://localhost:3000
```

### Agent Configuration

```yaml
# google_youtube_agent_config.yaml
google_youtube_agent:
  channel_id: "UCxxxxxxxxxxxxxxxxxxxx"
  default_privacy: "public"
  auto_tagging: true
  seo_optimization: true
  comment_moderation: "ai_assisted"

  analytics:
    retention_tracking: true
    demographic_analysis: true
    competitor_monitoring: true

  automation:
    scheduled_publishing: true
    comment_responses: true
    thumbnail_generation: true
    content_archiving: true
```

## 🎯 Key Capabilities

### Content Strategy & Planning
- **Trend Analysis**: Identify trending topics and content formats
- **Competitor Research**: Analyze competitor content strategies
- **Audience Insights**: Understand viewer preferences and behaviors
- **Content Calendar**: Automated content planning and scheduling

### Performance Optimization
- **A/B Testing**: Test different thumbnails, titles, and descriptions
- **SEO Optimization**: Optimize metadata for better discoverability
- **Engagement Boosting**: Automated strategies to increase engagement
- **Monetization Optimization**: Maximize revenue through content optimization

### Community Management
- **Comment Analysis**: Sentiment analysis and response suggestions
- **Community Building**: Automated community engagement strategies
- **Spam Detection**: AI-powered comment moderation
- **Fan Engagement**: Personalized responses and community building

### Analytics & Reporting
- **Performance Dashboards**: Real-time channel and video analytics
- **ROI Analysis**: Content performance vs. time/effort invested
- **Growth Tracking**: Subscriber growth and audience expansion metrics
- **Content Performance**: Video-level analytics and insights

## 🔄 Integration with Other Google Agents

### Marketing Orchestrator Integration
```python
# Coordinate with Google Ads Agent
ads_performance = await google_ads_agent.get_youtube_campaign_performance()
youtube_insights = await youtube_agent.optimize_for_ads_targeting(ads_performance)

# Unified marketing analytics
marketing_report = {
    "youtube_performance": youtube_agent.get_channel_metrics(),
    "ads_performance": google_ads_agent.get_campaign_metrics(),
    "cross_platform_insights": analytics_agent.get_cross_platform_attribution()
}
```

### Cross-Platform Content Distribution
```python
# Automated multi-platform publishing
content = await youtube_agent.create_video("My Content")
platforms = ["youtube", "tiktok", "instagram"]

for platform in platforms:
    await content_distribution_agent.publish_to_platform(content, platform)
```

## 📊 Monitoring & Analytics

### Real-time Metrics
- **Video Performance**: Views, watch time, engagement rates
- **Channel Growth**: Subscriber growth, audience retention
- **Revenue Tracking**: Monetization performance and trends
- **SEO Performance**: Search ranking and discoverability metrics

### AI-Powered Insights
- **Content Recommendations**: What content to create next
- **Optimization Suggestions**: How to improve existing content
- **Audience Predictions**: What your audience wants to see
- **Trend Forecasting**: Upcoming content trends and opportunities

## 🛡️ Security & Compliance

### Authentication & Authorization
- **OAuth 2.0**: Secure authentication with Google
- **Scoped Permissions**: Minimal required permissions only
- **Token Management**: Automated token refresh and rotation
- **Audit Logging**: Complete audit trail of all operations

### Data Protection
- **Privacy Compliance**: GDPR, CCPA compliance
- **Data Encryption**: All data encrypted in transit and at rest
- **Access Controls**: Role-based access to sensitive operations
- **Content Moderation**: Automated content appropriateness checking

## 🚀 Advanced Features

### AI Content Creation
- **Script Generation**: AI-generated video scripts and outlines
- **Thumbnail Creation**: AI-generated custom thumbnails
- **Title Optimization**: AI-optimized titles for maximum engagement
- **Description Enhancement**: SEO-optimized descriptions

### Automated Workflows
- **Content Pipeline**: End-to-end content creation and publishing
- **Quality Assurance**: Automated content quality checks
- **Distribution Automation**: Multi-platform content distribution
- **Performance Monitoring**: Automated performance alerts and actions

### Predictive Analytics
- **Content Forecasting**: Predict which content will perform well
- **Audience Growth**: Forecast subscriber growth and engagement
- **Trend Prediction**: Identify upcoming content trends
- **Optimization Recommendations**: AI-driven content improvement suggestions

## 📈 Performance Optimization

### Content Strategy Optimization
- **Algorithm Analysis**: Understand YouTube's recommendation algorithm
- **Timing Optimization**: Optimal publishing times for maximum reach
- **Format Testing**: Test different video formats and lengths
- **Series Optimization**: Optimize content series for binge-watching

### Technical Optimization
- **Video Encoding**: Optimal video encoding for quality and file size
- **CDN Distribution**: Ensure fast global content delivery
- **SEO Optimization**: Technical SEO for better discoverability
- **Mobile Optimization**: Optimize for mobile viewing experience

## 🔧 Development & Testing

### Testing Strategy
```bash
# Unit tests
python -m pytest tests/unit/ -v

# Integration tests
python -m pytest tests/integration/ -v

# MCP integration tests
python -m pytest tests/mcp_integration/ -v

# End-to-end tests
python -m pytest tests/e2e/ -v
```

### Development Workflow
```bash
# Set up development environment
pip install -r requirements-dev.txt

# Run with hot reload
python -m uvicorn app.main:app --reload --host 0.0.0.0

# Run tests
make test

# Lint and format
make lint
make format
```

## 📚 Documentation & Support

### Documentation Structure
- **User Guide**: Complete usage instructions and examples
- **API Reference**: Detailed API documentation
- **Integration Guide**: How to integrate with other systems
- **Troubleshooting**: Common issues and solutions

### Support Resources
- **GitHub Issues**: Bug reports and feature requests
- **Documentation Wiki**: Comprehensive guides and tutorials
- **Community Forum**: User community and discussions
- **Professional Support**: Enterprise support options

## 🔮 Future Enhancements

### Planned Features
- **Live Streaming Management**: Live stream planning and management
- **Shorts Optimization**: YouTube Shorts creation and optimization
- **Multi-channel Management**: Manage multiple YouTube channels
- **Advanced Analytics**: Deep learning-powered content insights

### Integration Roadmap
- **TikTok Integration**: Cross-platform content optimization
- **Instagram Integration**: Reels and Stories optimization
- **Twitter/X Integration**: Video content distribution
- **LinkedIn Integration**: B2B content optimization

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for comprehensive YouTube channel management**
