#!/usr/bin/env python3
"""
YouTube Content Service

AI-powered content creation and strategy services for YouTube management.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class ContentService:
    """
    YouTube Content Service

    Provides AI-powered content creation, strategy, and competitor analysis.
    """

    def __init__(self, mcp_client):
        self.mcp_client = mcp_client

    async def generate_content_suggestions(self, niche: str, performance_data: Dict[str, Any],
                                        trending_topics: List[str]) -> List[Dict[str, Any]]:
        """
        Generate content suggestions based on niche and performance data

        Args:
            niche: Content niche/category
            performance_data: Historical performance data
            trending_topics: Current trending topics

        Returns:
            List of content suggestions with expected performance
        """
        try:
            suggestions = []

            # Analyze top performing content
            top_performers = performance_data.get("top_videos", [])
            successful_topics = []

            for video in top_performers[:3]:  # Top 3 performers
                title = video.get("title", "").lower()
                # Simple keyword extraction (would use NLP in production)
                if any(word in title for word in ["review", "tutorial", "guide"]):
                    successful_topics.append("how-to")
                elif any(word in title for word in ["top", "best", "worst"]):
                    successful_topics.append("list")
                elif any(word in title for word in ["vs", "versus", "comparison"]):
                    successful_topics.append("comparison")

            # Generate suggestions based on successful patterns
            for topic_type in set(successful_topics):
                if topic_type == "how-to":
                    suggestions.extend(self._generate_tutorial_suggestions(niche, trending_topics))
                elif topic_type == "list":
                    suggestions.extend(self._generate_list_suggestions(niche))
                elif topic_type == "comparison":
                    suggestions.extend(self._generate_comparison_suggestions(niche))

            # Add trending topic suggestions
            for trend in trending_topics[:3]:
                suggestions.append({
                    "title": f"{trend} - {niche} Perspective",
                    "type": "trend_analysis",
                    "expected_performance": "high",
                    "reasoning": f"Capitalizing on trending topic '{trend}'",
                    "estimated_views": 5000,
                    "production_time": "medium"
                })

            # Remove duplicates and limit to 10
            seen_titles = set()
            unique_suggestions = []

            for suggestion in suggestions:
                title = suggestion.get("title", "")
                if title not in seen_titles and len(unique_suggestions) < 10:
                    seen_titles.add(title)
                    unique_suggestions.append(suggestion)

            return unique_suggestions

        except Exception as e:
            logger.error(f"Failed to generate content suggestions: {e}")
            return []

    async def analyze_competitor_strategy(self, competitor_videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze competitor content strategy

        Args:
            competitor_videos: List of competitor videos

        Returns:
            Competitor analysis results
        """
        try:
            analysis = {
                "total_videos_analyzed": len(competitor_videos),
                "content_patterns": {},
                "performance_insights": {},
                "strategy_recommendations": []
            }

            if not competitor_videos:
                return analysis

            # Analyze titles for patterns
            titles = [v.get("snippet", {}).get("title", "") for v in competitor_videos]

            # Simple pattern analysis (would use NLP in production)
            title_patterns = {
                "questions": sum(1 for t in titles if "?" in t),
                "numbers": sum(1 for t in titles if any(char.isdigit() for char in t)),
                "emojis": sum(1 for t in titles if any(ord(char) > 127 for char in t)),
                "how_to": sum(1 for t in titles if "how" in t.lower() and "to" in t.lower())
            }

            analysis["content_patterns"]["title_patterns"] = title_patterns

            # Analyze performance by title pattern
            pattern_performance = {}
            for video in competitor_videos:
                title = video.get("snippet", {}).get("title", "")
                views = int(video.get("statistics", {}).get("viewCount", 0))

                pattern = "other"
                if "?" in title:
                    pattern = "questions"
                elif any(char.isdigit() for char in title):
                    pattern = "numbers"
                elif "how" in title.lower() and "to" in title.lower():
                    pattern = "how_to"

                if pattern not in pattern_performance:
                    pattern_performance[pattern] = {"total_views": 0, "count": 0}

                pattern_performance[pattern]["total_views"] += views
                pattern_performance[pattern]["count"] += 1

            # Calculate averages
            for pattern, stats in pattern_performance.items():
                if stats["count"] > 0:
                    stats["avg_views"] = stats["total_views"] / stats["count"]

            analysis["performance_insights"]["pattern_performance"] = pattern_performance

            # Generate recommendations
            recommendations = []

            if title_patterns["questions"] > title_patterns["numbers"]:
                recommendations.append("Consider using more question-based titles")
            else:
                recommendations.append("Numbered lists perform well - try 'Top X' format")

            if title_patterns["how_to"] > len(competitor_videos) * 0.3:
                recommendations.append("How-to content is popular in this niche")

            top_pattern = max(pattern_performance.items(), key=lambda x: x[1]["avg_views"])
            recommendations.append(f"Focus on {top_pattern[0]} format (highest performing)")

            analysis["strategy_recommendations"] = recommendations

            return analysis

        except Exception as e:
            logger.error(f"Failed to analyze competitor strategy: {e}")
            return {"error": str(e)}

    async def optimize_content_calendar(self, existing_schedule: List[Dict[str, Any]],
                                     performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize content publishing calendar

        Args:
            existing_schedule: Current content schedule
            performance_data: Historical performance data

        Returns:
            Optimized content calendar
        """
        try:
            # Analyze best publishing times
            publishing_patterns = performance_data.get("publishing_patterns", {})

            best_day = publishing_patterns.get("best_publish_day", "Tuesday")
            best_hour = publishing_patterns.get("best_publish_hour", "14:00")

            # Generate optimized schedule
            optimized_schedule = []

            # Suggest 4 weeks of content
            for week in range(4):
                for day_offset in [0, 2, 4, 6]:  # Every other day
                    publish_date = datetime.now() + timedelta(days=week*7 + day_offset)

                    # Adjust to best day of week
                    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                    target_day_index = day_names.index(best_day) if best_day in day_names else 1  # Default Tuesday

                    while publish_date.weekday() != target_day_index:
                        publish_date += timedelta(days=1)

                    optimized_schedule.append({
                        "date": publish_date.strftime("%Y-%m-%d"),
                        "time": best_hour,
                        "content_type": self._suggest_content_type_for_date(publish_date),
                        "expected_performance": "optimized"
                    })

            return {
                "optimized_schedule": optimized_schedule,
                "best_publishing_day": best_day,
                "best_publishing_hour": best_hour,
                "recommendations": [
                    f"Publish on {best_day}s at {best_hour}",
                    "Maintain consistent posting schedule",
                    "Batch content creation for efficiency"
                ]
            }

        except Exception as e:
            logger.error(f"Failed to optimize content calendar: {e}")
            return {"error": str(e)}

    # Private helper methods

    def _generate_tutorial_suggestions(self, niche: str, trending_topics: List[str]) -> List[Dict[str, Any]]:
        """Generate tutorial content suggestions"""
        templates = [
            f"How to Get Started with {niche}",
            f"{niche} Tutorial for Beginners",
            f"Advanced {niche} Techniques",
            f"Common {niche} Mistakes to Avoid",
            f"{niche} Tips and Tricks"
        ]

        suggestions = []
        for template in templates[:3]:  # Limit to 3
            suggestions.append({
                "title": template,
                "type": "tutorial",
                "expected_performance": "high",
                "reasoning": "Tutorial content performs well in educational niches",
                "estimated_views": random.randint(2000, 8000),
                "production_time": "medium",
                "difficulty": "medium"
            })

        return suggestions

    def _generate_list_suggestions(self, niche: str) -> List[Dict[str, Any]]:
        """Generate list-based content suggestions"""
        templates = [
            f"Top 10 {niche} Tools in 2025",
            f"Best {niche} Practices",
            f"Ultimate Guide to {niche}",
            f"{niche} Hacks You Need to Know",
            f"Most Common {niche} Questions Answered"
        ]

        suggestions = []
        for template in templates[:2]:  # Limit to 2
            suggestions.append({
                "title": template,
                "type": "list",
                "expected_performance": "high",
                "reasoning": "List-based content drives high engagement",
                "estimated_views": random.randint(3000, 10000),
                "production_time": "low",
                "difficulty": "low"
            })

        return suggestions

    def _generate_comparison_suggestions(self, niche: str) -> List[Dict[str, Any]]:
        """Generate comparison content suggestions"""
        templates = [
            f"{niche} vs Competitor Analysis",
            f"Best {niche} Options Compared",
            f"{niche} Showdown: Feature Comparison",
            f"Comparing Top {niche} Solutions"
        ]

        suggestions = []
        for template in templates[:2]:  # Limit to 2
            suggestions.append({
                "title": template,
                "type": "comparison",
                "expected_performance": "medium",
                "reasoning": "Comparison content helps viewers make decisions",
                "estimated_views": random.randint(1500, 6000),
                "production_time": "high",
                "difficulty": "high"
            })

        return suggestions

    def _suggest_content_type_for_date(self, date: datetime) -> str:
        """Suggest content type based on day of week"""
        day_of_week = date.weekday()  # 0=Monday, 6=Sunday

        # Simple content type rotation
        content_types = [
            "tutorial",     # Monday
            "review",       # Tuesday
            "tips",         # Wednesday
            "comparison",   # Thursday
            "list",         # Friday
            "entertainment", # Saturday
            "reflection"    # Sunday
        ]

        return content_types[day_of_week]

    async def analyze_content_gaps(self, existing_content: List[Dict[str, Any]],
                                 competitor_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze content gaps compared to competitors

        Args:
            existing_content: Your existing videos
            competitor_content: Competitor videos

        Returns:
            Content gap analysis
        """
        try:
            # Extract topics from existing content
            existing_topics = set()
            for video in existing_content:
                title = video.get("snippet", {}).get("title", "").lower()
                # Simple topic extraction (would use NLP in production)
                if "tutorial" in title or "how" in title:
                    existing_topics.add("tutorial")
                elif "review" in title:
                    existing_topics.add("review")
                elif "tips" in title or "hacks" in title:
                    existing_topics.add("tips")
                elif "vs" in title or "comparison" in title:
                    existing_topics.add("comparison")

            # Extract topics from competitor content
            competitor_topics = set()
            for video in competitor_content:
                title = video.get("snippet", {}).get("title", "").lower()
                if "tutorial" in title or "how" in title:
                    competitor_topics.add("tutorial")
                elif "review" in title:
                    competitor_topics.add("review")
                elif "tips" in title or "hacks" in title:
                    competitor_topics.add("tips")
                elif "vs" in title or "comparison" in title:
                    competitor_topics.add("comparison")

            # Find gaps
            content_gaps = competitor_topics - existing_topics
            unique_content = existing_topics - competitor_topics

            return {
                "content_gaps": list(content_gaps),
                "unique_content": list(unique_content),
                "recommendations": [
                    f"Consider creating {gap} content" for gap in content_gaps
                ] + [
                    f"Your {unique} content gives you competitive advantage" for unique in unique_content
                ]
            }

        except Exception as e:
            logger.error(f"Failed to analyze content gaps: {e}")
            return {"error": str(e)}

    async def generate_content_series(self, niche: str, series_length: int = 5) -> Dict[str, Any]:
        """
        Generate a complete content series

        Args:
            niche: Content niche
            series_length: Number of videos in series

        Returns:
            Complete content series plan
        """
        try:
            # Generate series structure
            series_title = f"Complete {niche} Masterclass"

            episodes = []
            for i in range(series_length):
                episode_number = i + 1
                if i == 0:
                    title = f"{series_title} - Introduction"
                    focus = "overview"
                elif i == series_length - 1:
                    title = f"{series_title} - Advanced Techniques & Next Steps"
                    focus = "advanced"
                else:
                    topics = ["fundamentals", "intermediate", "practical", "case studies"]
                    focus = topics[i-1] if i-1 < len(topics) else "techniques"
                    title = f"{series_title} - {focus.title()}"

                episodes.append({
                    "episode": episode_number,
                    "title": title,
                    "focus": focus,
                    "estimated_duration": "10-15 minutes",
                    "key_points": self._generate_episode_keypoints(focus, niche),
                    "call_to_action": f"Like and subscribe for episode {episode_number + 1}!"
                })

            return {
                "series_title": series_title,
                "total_episodes": series_length,
                "episodes": episodes,
                "publishing_schedule": "Weekly on Tuesdays",
                "estimated_total_views": series_length * 2000,
                "engagement_strategy": [
                    "End screen cards linking to next episode",
                    "Cards highlighting key timestamps",
                    "Community posts teasing next episode",
                    "Email list for series updates"
                ]
            }

        except Exception as e:
            logger.error(f"Failed to generate content series: {e}")
            return {"error": str(e)}

    def _generate_episode_keypoints(self, focus: str, niche: str) -> List[str]:
        """Generate key points for episode based on focus"""
        keypoint_templates = {
            "overview": [
                f"What is {niche} and why it matters",
                f"Benefits of learning {niche}",
                f"What you'll learn in this series",
                f"Prerequisites and requirements"
            ],
            "fundamentals": [
                f"Core concepts of {niche}",
                f"Basic terminology and definitions",
                f"Essential tools and resources",
                f"Getting started guide"
            ],
            "intermediate": [
                f"Advanced {niche} techniques",
                f"Common challenges and solutions",
                f"Best practices and tips",
                f"Practical examples"
            ],
            "practical": [
                f"Real-world {niche} applications",
                f"Step-by-step tutorials",
                f"Troubleshooting common issues",
                f"Optimization strategies"
            ],
            "advanced": [
                f"Expert-level {niche} strategies",
                f"Cutting-edge techniques and trends",
                f"Scaling and automation",
                f"Future of {niche}"
            ]
        }

        return keypoint_templates.get(focus, [
            f"Introduction to {focus}",
            f"Key concepts and principles",
            f"Practical applications",
            f"Next steps and resources"
        ])
