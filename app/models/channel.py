#!/usr/bin/env python3
"""
YouTube Channel Models

Data models for YouTube channel data and analytics.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChannelSnippet:
    """YouTube channel snippet data"""
    title: str
    description: str
    published_at: datetime
    custom_url: Optional[str]
    country: Optional[str]
    default_language: Optional[str]

@dataclass
class ChannelStatistics:
    """YouTube channel statistics"""
    view_count: int
    subscriber_count: Optional[int]  # Hidden if channel doesn't show count
    video_count: int
    hidden_subscriber_count: bool

@dataclass
class ChannelBranding:
    """YouTube channel branding settings"""
    channel_title: str
    channel_description: str
    keywords: str
    default_tab: Optional[str]
    tracking_analytics_account_id: Optional[str]
    moderate_comments: bool
    show_related_channels: bool
    show_browse_view: bool
    featured_channels_title: Optional[str]
    featured_channels_urls: List[str]
    unsubscribed_trailer: Optional[str]
    profile_color: str
    default_language: Optional[str]

@dataclass
class ChannelStatus:
    """YouTube channel status"""
    privacy_status: str
    is_linked: bool
    long_uploads_status: str
    made_for_kids: bool
    self_declared_made_for_kids: bool

@dataclass
class Channel:
    """Complete YouTube channel data model"""
    id: str
    snippet: ChannelSnippet
    statistics: ChannelStatistics
    branding_settings: Optional[ChannelBranding] = None
    status: Optional[ChannelStatus] = None

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> 'Channel':
        """Create Channel instance from YouTube API response"""
        snippet_data = api_data.get("snippet", {})
        stats_data = api_data.get("statistics", {})
        branding_data = api_data.get("brandingSettings", {})
        status_data = api_data.get("status", {})

        # Parse published date
        published_at = datetime.fromisoformat(
            snippet_data.get("publishedAt", "").replace('Z', '+00:00')
        )

        snippet = ChannelSnippet(
            title=snippet_data.get("title", ""),
            description=snippet_data.get("description", ""),
            published_at=published_at,
            custom_url=snippet_data.get("customUrl"),
            country=snippet_data.get("country"),
            default_language=snippet_data.get("defaultLanguage")
        )

        statistics = ChannelStatistics(
            view_count=int(stats_data.get("viewCount", 0)),
            subscriber_count=int(stats_data.get("subscriberCount", 0)) if stats_data.get("subscriberCount") else None,
            video_count=int(stats_data.get("videoCount", 0)),
            hidden_subscriber_count=stats_data.get("hiddenSubscriberCount", False)
        )

        branding_settings = None
        if branding_data:
            branding_settings = ChannelBranding(
                channel_title=branding_data.get("channel", {}).get("title", ""),
                channel_description=branding_data.get("channel", {}).get("description", ""),
                keywords=branding_data.get("channel", {}).get("keywords", ""),
                default_tab=branding_data.get("channel", {}).get("defaultTab"),
                tracking_analytics_account_id=branding_data.get("channel", {}).get("trackingAnalyticsAccountId"),
                moderate_comments=branding_data.get("channel", {}).get("moderateComments", False),
                show_related_channels=branding_data.get("channel", {}).get("showRelatedChannels", True),
                show_browse_view=branding_data.get("channel", {}).get("showBrowseView", True),
                featured_channels_title=branding_data.get("channel", {}).get("featuredChannelsTitle"),
                featured_channels_urls=branding_data.get("channel", {}).get("featuredChannelsUrls", []),
                unsubscribed_trailer=branding_data.get("channel", {}).get("unsubscribedTrailer"),
                profile_color=branding_data.get("channel", {}).get("profileColor", "#000000"),
                default_language=branding_data.get("channel", {}).get("defaultLanguage")
            )

        status = None
        if status_data:
            status = ChannelStatus(
                privacy_status=status_data.get("privacyStatus", ""),
                is_linked=status_data.get("isLinked", False),
                long_uploads_status=status_data.get("longUploadsStatus", ""),
                made_for_kids=status_data.get("madeForKids", False),
                self_declared_made_for_kids=status_data.get("selfDeclaredMadeForKids", False)
            )

        return cls(
            id=api_data.get("id", ""),
            snippet=snippet,
            statistics=statistics,
            branding_settings=branding_settings,
            status=status
        )

    @property
    def subscriber_milestone(self) -> str:
        """Get subscriber milestone category"""
        if not self.statistics.subscriber_count:
            return "Hidden"

        subs = self.statistics.subscriber_count
        if subs >= 1000000:
            return "1M+"
        elif subs >= 100000:
            return "100K+"
        elif subs >= 10000:
            return "10K+"
        elif subs >= 1000:
            return "1K+"
        else:
            return "< 1K"

    @property
    def avg_views_per_video(self) -> Optional[float]:
        """Calculate average views per video"""
        if self.statistics.video_count > 0:
            return self.statistics.view_count / self.statistics.video_count
        return None

@dataclass
class ChannelAnalytics:
    """Channel performance analytics"""
    channel_id: str
    period_days: int
    total_views: int
    total_subscribers_gained: int
    total_subscribers_lost: int
    top_videos: List[Dict[str, Any]]
    views_by_day: List[Dict[str, int]]
    subscribers_by_day: List[Dict[str, int]]
    traffic_sources: Dict[str, int]
    audience_retention_avg: float
    top_countries: List[Dict[str, Any]]
    device_types: Dict[str, int]
    age_demographics: Dict[str, int]
    gender_demographics: Dict[str, int]
    watch_time_hours: float
    average_view_duration: float

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> 'ChannelAnalytics':
        """Create ChannelAnalytics from API response (placeholder)"""
        # This would parse actual YouTube Analytics API data
        return cls(
            channel_id=api_data.get("channel_id", ""),
            period_days=api_data.get("period_days", 30),
            total_views=api_data.get("total_views", 0),
            total_subscribers_gained=api_data.get("subscribers_gained", 0),
            total_subscribers_lost=api_data.get("subscribers_lost", 0),
            top_videos=api_data.get("top_videos", []),
            views_by_day=api_data.get("views_by_day", []),
            subscribers_by_day=api_data.get("subscribers_by_day", []),
            traffic_sources=api_data.get("traffic_sources", {}),
            audience_retention_avg=api_data.get("audience_retention", 0.0),
            top_countries=api_data.get("top_countries", []),
            device_types=api_data.get("device_types", {}),
            age_demographics=api_data.get("age_demographics", {}),
            gender_demographics=api_data.get("gender_demographics", {}),
            watch_time_hours=api_data.get("watch_time_hours", 0.0),
            average_view_duration=api_data.get("average_view_duration", 0.0)
        )

    @property
    def net_subscriber_growth(self) -> int:
        """Calculate net subscriber growth"""
        return self.total_subscribers_gained - self.total_subscribers_lost

    @property
    def subscriber_growth_rate(self) -> float:
        """Calculate subscriber growth rate (placeholder - needs baseline)"""
        # This would need historical data to calculate properly
        return 0.0

@dataclass
class Playlist:
    """YouTube playlist data model"""
    id: str
    title: str
    description: str
    published_at: datetime
    channel_id: str
    channel_title: str
    item_count: int
    privacy_status: str
    tags: List[str]

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> 'Playlist':
        """Create Playlist instance from YouTube API response"""
        snippet_data = api_data.get("snippet", {})
        status_data = api_data.get("status", {})
        content_details = api_data.get("contentDetails", {})

        # Parse published date
        published_at = datetime.fromisoformat(
            snippet_data.get("publishedAt", "").replace('Z', '+00:00')
        )

        return cls(
            id=api_data.get("id", ""),
            title=snippet_data.get("title", ""),
            description=snippet_data.get("description", ""),
            published_at=published_at,
            channel_id=snippet_data.get("channelId", ""),
            channel_title=snippet_data.get("channelTitle", ""),
            item_count=int(content_details.get("itemCount", 0)),
            privacy_status=status_data.get("privacyStatus", "public"),
            tags=snippet_data.get("tags", [])
        )

@dataclass
class Comment:
    """YouTube comment data model"""
    id: str
    text_display: str
    text_original: str
    author_display_name: str
    author_profile_image_url: str
    author_channel_url: str
    author_channel_id: str
    like_count: int
    published_at: datetime
    updated_at: Optional[datetime]
    total_reply_count: int
    is_public: bool

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> 'Comment':
        """Create Comment instance from YouTube API response"""
        snippet_data = api_data.get("snippet", {})
        top_level_comment = snippet_data.get("topLevelComment", {}).get("snippet", {})

        # Parse dates
        published_at = datetime.fromisoformat(
            top_level_comment.get("publishedAt", "").replace('Z', '+00:00')
        )

        updated_at = None
        if top_level_comment.get("updatedAt"):
            updated_at = datetime.fromisoformat(
                top_level_comment.get("updatedAt", "").replace('Z', '+00:00')
            )

        return cls(
            id=api_data.get("id", ""),
            text_display=top_level_comment.get("textDisplay", ""),
            text_original=top_level_comment.get("textOriginal", ""),
            author_display_name=top_level_comment.get("authorDisplayName", ""),
            author_profile_image_url=top_level_comment.get("authorProfileImageUrl", ""),
            author_channel_url=top_level_comment.get("authorChannelUrl", ""),
            author_channel_id=top_level_comment.get("authorChannelId", {}).get("value", ""),
            like_count=int(top_level_comment.get("likeCount", 0)),
            published_at=published_at,
            updated_at=updated_at,
            total_reply_count=int(api_data.get("totalReplyCount", 0)),
            is_public=top_level_comment.get("isPublic", True)
        )
