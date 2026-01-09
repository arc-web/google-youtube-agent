#!/usr/bin/env python3
"""
YouTube Analytics Service

Provides comprehensive analytics and performance tracking for YouTube content.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import statistics

logger = logging.getLogger(__name__)

class AnalyticsService:
    """
    YouTube Analytics Service

    Calculates performance metrics, trends, and insights from YouTube data.
    """

    def __init__(self, mcp_client):
        self.mcp_client = mcp_client

    async def calculate_channel_metrics(self, channel_info: Dict[str, Any],
                                      videos: List[Dict[str, Any]],
                                      days: int = 30) -> Dict[str, Any]:
        """
        Calculate comprehensive channel metrics

        Args:
            channel_info: Channel basic information
            videos: List of channel videos
            days: Number of days to analyze

        Returns:
            Comprehensive channel analytics
        """
        try:
            # Filter videos by date
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_videos = self._filter_videos_by_date(videos, cutoff_date)

            # Basic metrics
            total_views = sum(self._extract_view_count(v) for v in recent_videos)
            total_likes = sum(self._extract_like_count(v) for v in recent_videos)
            total_comments = sum(self._extract_comment_count(v) for v in recent_videos)

            # Engagement metrics
            avg_engagement = self._calculate_average_engagement(recent_videos)

            # Growth metrics
            growth_rate = self._calculate_growth_rate(videos, days)

            # Content performance
            top_videos = self._get_top_performing_videos(recent_videos, limit=5)

            # Publishing patterns
            publish_patterns = self._analyze_publishing_patterns(recent_videos)

            return {
                "period_days": days,
                "total_videos_analyzed": len(recent_videos),
                "metrics": {
                    "total_views": total_views,
                    "total_likes": total_likes,
                    "total_comments": total_comments,
                    "average_engagement_rate": avg_engagement,
                    "subscriber_count": channel_info.get("statistics", {}).get("subscriberCount", 0),
                    "video_count": channel_info.get("statistics", {}).get("videoCount", 0)
                },
                "growth": growth_rate,
                "top_videos": top_videos,
                "publishing_patterns": publish_patterns,
                "recommendations": self._generate_recommendations(recent_videos)
            }

        except Exception as e:
            logger.error(f"Failed to calculate channel metrics: {e}")
            return {"error": str(e)}

    async def analyze_performance(self, videos: List[Dict[str, Any]], days: int = 30) -> Dict[str, Any]:
        """
        Analyze video performance metrics

        Args:
            videos: List of videos to analyze
            days: Analysis period in days

        Returns:
            Performance analysis results
        """
        try:
            # Filter recent videos
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_videos = self._filter_videos_by_date(videos, cutoff_date)

            # Performance by category
            performance_by_duration = self._analyze_performance_by_duration(recent_videos)
            performance_by_day = self._analyze_performance_by_publish_day(recent_videos)
            performance_by_hour = self._analyze_performance_by_publish_hour(recent_videos)

            # Trend analysis
            view_trends = self._calculate_view_trends(recent_videos)
            engagement_trends = self._calculate_engagement_trends(recent_videos)

            return {
                "period_days": days,
                "videos_analyzed": len(recent_videos),
                "performance_breakdown": {
                    "by_duration": performance_by_duration,
                    "by_publish_day": performance_by_day,
                    "by_publish_hour": performance_by_hour
                },
                "trends": {
                    "views": view_trends,
                    "engagement": engagement_trends
                },
                "insights": self._generate_performance_insights(recent_videos)
            }

        except Exception as e:
            logger.error(f"Failed to analyze performance: {e}")
            return {"error": str(e)}

    async def analyze_trends(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze content trends and patterns

        Args:
            videos: List of videos to analyze

        Returns:
            Trend analysis results
        """
        try:
            # Sort videos by publish date
            sorted_videos = sorted(
                videos,
                key=lambda v: self._extract_publish_date(v),
                reverse=True
            )

            # Monthly trends
            monthly_stats = self._calculate_monthly_stats(sorted_videos)

            # Topic analysis
            topic_performance = self._analyze_topic_performance(sorted_videos)

            # Seasonal patterns
            seasonal_patterns = self._analyze_seasonal_patterns(sorted_videos)

            return {
                "monthly_trends": monthly_stats,
                "topic_performance": topic_performance,
                "seasonal_patterns": seasonal_patterns,
                "predictions": self._generate_trend_predictions(sorted_videos)
            }

        except Exception as e:
            logger.error(f"Failed to analyze trends: {e}")
            return {"error": str(e)}

    # Private helper methods

    def _filter_videos_by_date(self, videos: List[Dict[str, Any]], cutoff_date: datetime) -> List[Dict[str, Any]]:
        """Filter videos published after cutoff date"""
        filtered = []
        for video in videos:
            publish_date = self._extract_publish_date(video)
            if publish_date and publish_date > cutoff_date:
                filtered.append(video)
        return filtered

    def _extract_publish_date(self, video: Dict[str, Any]) -> Optional[datetime]:
        """Extract publish date from video"""
        try:
            date_str = video.get("snippet", {}).get("publishedAt")
            if date_str:
                # Handle different date formats
                if date_str.endswith('Z'):
                    date_str = date_str[:-1] + '+00:00'
                return datetime.fromisoformat(date_str)
        except Exception:
            pass
        return None

    def _extract_view_count(self, video: Dict[str, Any]) -> int:
        """Extract view count from video"""
        try:
            return int(video.get("statistics", {}).get("viewCount", 0))
        except (ValueError, TypeError):
            return 0

    def _extract_like_count(self, video: Dict[str, Any]) -> int:
        """Extract like count from video"""
        try:
            return int(video.get("statistics", {}).get("likeCount", 0))
        except (ValueError, TypeError):
            return 0

    def _extract_comment_count(self, video: Dict[str, Any]) -> int:
        """Extract comment count from video"""
        try:
            return int(video.get("statistics", {}).get("commentCount", 0))
        except (ValueError, TypeError):
            return 0

    def _calculate_average_engagement(self, videos: List[Dict[str, Any]]) -> float:
        """Calculate average engagement rate"""
        if not videos:
            return 0.0

        total_engagement = 0
        for video in videos:
            views = self._extract_view_count(video)
            likes = self._extract_like_count(video)
            comments = self._extract_comment_count(video)

            if views > 0:
                engagement_rate = (likes + comments) / views
                total_engagement += engagement_rate

        return total_engagement / len(videos) if videos else 0.0

    def _calculate_growth_rate(self, videos: List[Dict[str, Any]], days: int) -> Dict[str, Any]:
        """Calculate growth metrics"""
        if len(videos) < 2:
            return {"error": "Insufficient data for growth calculation"}

        # Sort by date
        sorted_videos = sorted(videos, key=lambda v: self._extract_publish_date(v) or datetime.min)

        # Calculate view growth
        recent_views = sum(self._extract_view_count(v) for v in sorted_videos[-10:])  # Last 10 videos
        older_views = sum(self._extract_view_count(v) for v in sorted_videos[-20:-10])  # Previous 10

        growth_rate = 0.0
        if older_views > 0:
            growth_rate = ((recent_views - older_views) / older_views) * 100

        return {
            "view_growth_rate": growth_rate,
            "recent_avg_views": recent_views / 10 if recent_views > 0 else 0,
            "trend": "growing" if growth_rate > 10 else "stable" if growth_rate > -10 else "declining"
        }

    def _get_top_performing_videos(self, videos: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing videos by views"""
        sorted_videos = sorted(
            videos,
            key=lambda v: self._extract_view_count(v),
            reverse=True
        )

        return [{
            "title": v.get("snippet", {}).get("title", "Unknown"),
            "views": self._extract_view_count(v),
            "likes": self._extract_like_count(v),
            "comments": self._extract_comment_count(v),
            "published_at": v.get("snippet", {}).get("publishedAt")
        } for v in sorted_videos[:limit]]

    def _analyze_publishing_patterns(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze publishing patterns"""
        if not videos:
            return {"error": "No videos to analyze"}

        publish_days = []
        publish_hours = []

        for video in videos:
            publish_date = self._extract_publish_date(video)
            if publish_date:
                publish_days.append(publish_date.weekday())  # 0=Monday, 6=Sunday
                publish_hours.append(publish_date.hour)

        # Most common publish day
        if publish_days:
            most_common_day = max(set(publish_days), key=publish_days.count)
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            best_day = day_names[most_common_day]
        else:
            best_day = "Unknown"

        # Most common publish hour
        if publish_hours:
            most_common_hour = max(set(publish_hours), key=publish_hours.count)
            best_hour = f"{most_common_hour}:00"
        else:
            best_hour = "Unknown"

        return {
            "best_publish_day": best_day,
            "best_publish_hour": best_hour,
            "total_videos_analyzed": len(videos)
        }

    def _generate_recommendations(self, videos: List[Dict[str, Any]]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []

        if not videos:
            return ["Upload your first video to start getting analytics!"]

        # Analyze engagement
        avg_engagement = self._calculate_average_engagement(videos)
        if avg_engagement < 0.02:  # Less than 2%
            recommendations.append("Increase engagement by asking viewers questions in your videos")
            recommendations.append("Respond to comments to build community")

        # Analyze posting frequency
        if len(videos) < 5:
            recommendations.append("Increase posting frequency to grow your audience")

        # Analyze top performers
        top_video = self._get_top_performing_videos(videos, 1)
        if top_video:
            top_views = top_video[0]["views"]
            if top_views > 10000:
                recommendations.append("Great job! Your top video performs well - create more similar content")
            elif top_views < 1000:
                recommendations.append("Focus on improving video quality and SEO to increase views")

        return recommendations

    def _analyze_performance_by_duration(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance by video duration"""
        # This would require duration data from contentDetails
        # For now, return placeholder
        return {"short": {"avg_views": 0, "count": 0}, "medium": {"avg_views": 0, "count": 0}, "long": {"avg_views": 0, "count": 0}}

    def _analyze_performance_by_publish_day(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance by day of week"""
        day_performance = {}
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for video in videos:
            publish_date = self._extract_publish_date(video)
            if publish_date:
                day = day_names[publish_date.weekday()]
                views = self._extract_view_count(video)

                if day not in day_performance:
                    day_performance[day] = {"total_views": 0, "count": 0}

                day_performance[day]["total_views"] += views
                day_performance[day]["count"] += 1

        # Calculate averages
        for day, stats in day_performance.items():
            if stats["count"] > 0:
                stats["avg_views"] = stats["total_views"] / stats["count"]

        return day_performance

    def _analyze_performance_by_publish_hour(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance by hour of day"""
        hour_performance = {}

        for video in videos:
            publish_date = self._extract_publish_date(video)
            if publish_date:
                hour = publish_date.hour
                views = self._extract_view_count(video)

                if hour not in hour_performance:
                    hour_performance[hour] = {"total_views": 0, "count": 0}

                hour_performance[hour]["total_views"] += views
                hour_performance[hour]["count"] += 1

        # Calculate averages
        for hour, stats in hour_performance.items():
            if stats["count"] > 0:
                stats["avg_views"] = stats["total_views"] / stats["count"]

        return hour_performance

    def _calculate_view_trends(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate view count trends"""
        if len(videos) < 2:
            return {"trend": "insufficient_data"}

        # Sort by date
        sorted_videos = sorted(videos, key=lambda v: self._extract_publish_date(v) or datetime.min)

        # Get view counts
        view_counts = [self._extract_view_count(v) for v in sorted_videos[-20:]]  # Last 20 videos

        if len(view_counts) < 2:
            return {"trend": "insufficient_data"}

        # Calculate trend
        first_half = statistics.mean(view_counts[:len(view_counts)//2])
        second_half = statistics.mean(view_counts[len(view_counts)//2:])

        if second_half > first_half * 1.1:
            trend = "increasing"
        elif second_half < first_half * 0.9:
            trend = "decreasing"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "recent_avg": second_half,
            "previous_avg": first_half,
            "change_percent": ((second_half - first_half) / first_half) * 100 if first_half > 0 else 0
        }

    def _calculate_engagement_trends(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate engagement trends"""
        if len(videos) < 2:
            return {"trend": "insufficient_data"}

        # Calculate engagement rates
        engagement_rates = []
        for video in videos:
            views = self._extract_view_count(video)
            likes = self._extract_like_count(video)
            comments = self._extract_comment_count(video)

            if views > 0:
                rate = (likes + comments) / views
                engagement_rates.append(rate)

        if len(engagement_rates) < 2:
            return {"trend": "insufficient_data"}

        # Split into halves
        mid = len(engagement_rates) // 2
        first_half = statistics.mean(engagement_rates[:mid])
        second_half = statistics.mean(engagement_rates[mid:])

        if second_half > first_half * 1.05:
            trend = "increasing"
        elif second_half < first_half * 0.95:
            trend = "decreasing"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "recent_avg": second_half,
            "previous_avg": first_half,
            "change_percent": ((second_half - first_half) / first_half) * 100 if first_half > 0 else 0
        }

    def _generate_performance_insights(self, videos: List[Dict[str, Any]]) -> List[str]:
        """Generate performance insights"""
        insights = []

        if not videos:
            return ["Upload videos to start getting performance insights!"]

        # Analyze view distribution
        view_counts = [self._extract_view_count(v) for v in videos]
        if view_counts:
            avg_views = statistics.mean(view_counts)
            max_views = max(view_counts)

            if max_views > avg_views * 3:
                insights.append("You have viral potential - focus on what made your top video successful")

            if avg_views < 1000:
                insights.append("Consider improving video SEO and promotion strategies")

        # Analyze engagement
        engagement_rates = []
        for video in videos:
            views = self._extract_view_count(video)
            likes = self._extract_like_count(video)
            comments = self._extract_comment_count(video)

            if views > 0:
                rate = (likes + comments) / views
                engagement_rates.append(rate)

        if engagement_rates:
            avg_engagement = statistics.mean(engagement_rates)
            if avg_engagement > 0.05:  # Over 5%
                insights.append("Excellent engagement! Keep creating content that resonates with your audience")
            elif avg_engagement < 0.01:  # Under 1%
                insights.append("Consider strategies to increase viewer interaction and community building")

        return insights

    def _calculate_monthly_stats(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate monthly statistics"""
        monthly_data = {}

        for video in videos:
            publish_date = self._extract_publish_date(video)
            if publish_date:
                month_key = f"{publish_date.year}-{publish_date.month:02d}"
                views = self._extract_view_count(video)

                if month_key not in monthly_data:
                    monthly_data[month_key] = {"videos": 0, "views": 0}

                monthly_data[month_key]["videos"] += 1
                monthly_data[month_key]["views"] += views

        return monthly_data

    def _analyze_topic_performance(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance by topic (simplified)"""
        # This would use AI/ML to categorize videos by topic
        # For now, return placeholder
        return {"topics": {}, "note": "Topic analysis requires AI categorization"}

    def _analyze_seasonal_patterns(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze seasonal publishing patterns"""
        seasonal_data = {"winter": [], "spring": [], "summer": [], "fall": []}

        for video in videos:
            publish_date = self._extract_publish_date(video)
            if publish_date:
                month = publish_date.month
                views = self._extract_view_count(video)

                if month in [12, 1, 2]:
                    seasonal_data["winter"].append(views)
                elif month in [3, 4, 5]:
                    seasonal_data["spring"].append(views)
                elif month in [6, 7, 8]:
                    seasonal_data["summer"].append(views)
                else:  # 9, 10, 11
                    seasonal_data["fall"].append(views)

        # Calculate averages
        for season, views in seasonal_data.items():
            if views:
                seasonal_data[season] = {
                    "avg_views": statistics.mean(views),
                    "total_videos": len(views)
                }
            else:
                seasonal_data[season] = {"avg_views": 0, "total_videos": 0}

        return seasonal_data

    def _generate_trend_predictions(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate trend predictions (simplified)"""
        if len(videos) < 10:
            return {"note": "Need more videos for accurate predictions"}

        # Simple linear trend
        view_counts = [self._extract_view_count(v) for v in videos[-20:]]  # Last 20 videos

        if len(view_counts) >= 2:
            trend = "stable"
            if view_counts[-1] > view_counts[0] * 1.2:
                trend = "improving"
            elif view_counts[-1] < view_counts[0] * 0.8:
                trend = "declining"

            return {
                "performance_trend": trend,
                "confidence": "low",
                "recommendations": [
                    "Continue monitoring performance metrics",
                    "Experiment with different content types",
                    "Analyze what works for your audience"
                ]
            }

        return {"note": "Insufficient data for predictions"}
