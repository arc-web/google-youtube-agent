#!/usr/bin/env python3
"""
YouTube Video Models

Data models for YouTube video data and analytics.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VideoSnippet:
    """YouTube video snippet data"""
    title: str
    description: str
    published_at: datetime
    channel_id: str
    channel_title: str
    tags: List[str]
    category_id: str
    default_audio_language: Optional[str] = None
    default_language: Optional[str] = None

@dataclass
class VideoStatistics:
    """YouTube video statistics"""
    view_count: int
    like_count: Optional[int]
    dislike_count: Optional[int]  # Deprecated but kept for compatibility
    favorite_count: int
    comment_count: Optional[int]

@dataclass
class VideoContentDetails:
    """YouTube video content details"""
    duration: str  # ISO 8601 duration
    dimension: str
    definition: str  # hd or sd
    caption: str  # true or false
    licensed_content: bool
    projection: str

@dataclass
class VideoStatus:
    """YouTube video status"""
    upload_status: str
    privacy_status: str
    license: str
    embeddable: bool
    public_stats_viewable: bool
    made_for_kids: bool

@dataclass
class Video:
    """Complete YouTube video data model"""
    id: str
    snippet: VideoSnippet
    statistics: VideoStatistics
    content_details: Optional[VideoContentDetails] = None
    status: Optional[VideoStatus] = None

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> 'Video':
        """Create Video instance from YouTube API response"""
        snippet_data = api_data.get("snippet", {})
        stats_data = api_data.get("statistics", {})
        content_data = api_data.get("contentDetails", {})
        status_data = api_data.get("status", {})

        # Parse published date
        published_at = datetime.fromisoformat(
            snippet_data.get("publishedAt", "").replace('Z', '+00:00')
        )

        snippet = VideoSnippet(
            title=snippet_data.get("title", ""),
            description=snippet_data.get("description", ""),
            published_at=published_at,
            channel_id=snippet_data.get("channelId", ""),
            channel_title=snippet_data.get("channelTitle", ""),
            tags=snippet_data.get("tags", []),
            category_id=snippet_data.get("categoryId", ""),
            default_audio_language=snippet_data.get("defaultAudioLanguage"),
            default_language=snippet_data.get("defaultLanguage")
        )

        statistics = VideoStatistics(
            view_count=int(stats_data.get("viewCount", 0)),
            like_count=int(stats_data.get("likeCount", 0)) if stats_data.get("likeCount") else None,
            dislike_count=int(stats_data.get("dislikeCount", 0)) if stats_data.get("dislikeCount") else None,
            favorite_count=int(stats_data.get("favoriteCount", 0)),
            comment_count=int(stats_data.get("commentCount", 0)) if stats_data.get("commentCount") else None
        )

        content_details = None
        if content_data:
            content_details = VideoContentDetails(
                duration=content_data.get("duration", ""),
                dimension=content_data.get("dimension", ""),
                definition=content_data.get("definition", ""),
                caption=content_data.get("caption", ""),
                licensed_content=content_data.get("licensedContent", False),
                projection=content_data.get("projection", "")
            )

        status = None
        if status_data:
            status = VideoStatus(
                upload_status=status_data.get("uploadStatus", ""),
                privacy_status=status_data.get("privacyStatus", ""),
                license=status_data.get("license", ""),
                embeddable=status_data.get("embeddable", False),
                public_stats_viewable=status_data.get("publicStatsViewable", False),
                made_for_kids=status_data.get("madeForKids", False)
            )

        return cls(
            id=api_data.get("id", ""),
            snippet=snippet,
            statistics=statistics,
            content_details=content_details,
            status=status
        )

    @property
    def engagement_rate(self) -> Optional[float]:
        """Calculate engagement rate (likes + comments) / views"""
        if not self.statistics.like_count or not self.statistics.comment_count:
            return None

        total_engagement = self.statistics.like_count + self.statistics.comment_count
        if self.statistics.view_count > 0:
            return total_engagement / self.statistics.view_count
        return None

    @property
    def duration_seconds(self) -> Optional[int]:
        """Convert ISO 8601 duration to seconds"""
        if not self.content_details:
            return None

        import re
        duration = self.content_details.duration

        # Parse ISO 8601 duration (PT1H2M3S)
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration)

        if match:
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            seconds = int(match.group(3) or 0)

            return hours * 3600 + minutes * 60 + seconds

        return None

@dataclass
class VideoAnalytics:
    """Video performance analytics"""
    video_id: str
    views_trend: List[Dict[str, Any]]
    engagement_trend: List[Dict[str, Any]]
    traffic_sources: Dict[str, int]
    audience_retention: Dict[str, float]
    top_geographies: List[Dict[str, str]]
    device_types: Dict[str, int]
    age_demographics: Dict[str, int]
    gender_demographics: Dict[str, int]

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> 'VideoAnalytics':
        """Create VideoAnalytics from API response (placeholder)"""
        # This would parse actual YouTube Analytics API data
        return cls(
            video_id=api_data.get("video_id", ""),
            views_trend=[],
            engagement_trend=[],
            traffic_sources={},
            audience_retention={},
            top_geographies=[],
            device_types={},
            age_demographics={},
            gender_demographics={}
        )

@dataclass
class VideoOptimization:
    """Video optimization recommendations"""
    video_id: str
    title_score: int  # 0-100
    description_score: int
    tags_score: int
    thumbnail_score: int
    overall_score: int
    recommendations: List[str]
    optimized_title: Optional[str] = None
    optimized_description: Optional[str] = None
    optimized_tags: Optional[List[str]] = None
