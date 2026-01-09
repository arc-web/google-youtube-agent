#!/usr/bin/env python3
"""
YouTube Optimization Service

AI-powered optimization services for YouTube content, titles, descriptions, and metadata.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
import re
import string
import random

logger = logging.getLogger(__name__)

class OptimizationService:
    """
    YouTube Optimization Service

    Provides AI-powered optimization for titles, descriptions, tags, and thumbnails.
    """

    def __init__(self, mcp_client):
        self.mcp_client = mcp_client

        # Optimization rules and patterns
        self.title_max_length = 100
        self.description_max_length = 5000
        self.tags_max_count = 15
        self.tags_max_length = 100

    async def optimize_video_metadata(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize complete video metadata

        Args:
            video_data: Current video data from YouTube API

        Returns:
            Optimization recommendations and suggestions
        """
        try:
            optimizations = {
                "title_optimization": {},
                "description_optimization": {},
                "tags_optimization": {},
                "thumbnail_suggestion": {},
                "overall_score": 0,
                "recommendations": []
            }

            # Current metadata
            current_title = video_data.get("snippet", {}).get("title", "")
            current_description = video_data.get("snippet", {}).get("description", "")
            current_tags = video_data.get("snippet", {}).get("tags", [])

            # Optimize title
            title_opt = await self.optimize_title(current_title)
            optimizations["title_optimization"] = title_opt

            # Optimize description
            desc_opt = await self.optimize_description(current_description, current_title)
            optimizations["description_optimization"] = desc_opt

            # Optimize tags
            tags_opt = await self.optimize_tags(current_tags, current_title, current_description)
            optimizations["tags_optimization"] = tags_opt

            # Thumbnail suggestions
            thumb_opt = await self.suggest_thumbnail_ideas(current_title, current_description)
            optimizations["thumbnail_suggestion"] = thumb_opt

            # Calculate overall score
            scores = [
                title_opt.get("seo_score", 0),
                desc_opt.get("seo_score", 0),
                tags_opt.get("optimization_score", 0) * 25,  # Convert to 0-100
                75  # Thumbnail score (placeholder)
            ]
            optimizations["overall_score"] = sum(scores) / len(scores)

            # Generate recommendations
            optimizations["recommendations"] = self._generate_metadata_recommendations(
                title_opt, desc_opt, tags_opt, thumb_opt
            )

            return optimizations

        except Exception as e:
            logger.error(f"Failed to optimize video metadata: {e}")
            return {"error": str(e)}

    async def optimize_title(self, current_title: str, target_keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Optimize video title for SEO and engagement

        Args:
            current_title: Current video title
            target_keywords: Target keywords to include

        Returns:
            Title optimization results
        """
        try:
            analysis = {
                "current_title": current_title,
                "optimized_title": "",
                "seo_score": 0,
                "engagement_score": 0,
                "improvements": [],
                "keyword_suggestions": []
            }

            # Analyze current title
            current_length = len(current_title)
            has_numbers = bool(re.search(r'\d', current_title))
            has_emojis = any(ord(char) > 127 for char in current_title)
            has_question = '?' in current_title
            has_power_words = any(word in current_title.lower() for word in
                                ['best', 'top', 'ultimate', 'complete', 'master', 'guide'])

            # Calculate current score
            base_score = 50
            if 30 <= current_length <= self.title_max_length:
                base_score += 20
            if has_numbers:
                base_score += 10
            if has_question:
                base_score += 15
            if has_power_words:
                base_score += 10
            if not has_emojis:  # Clean titles often perform better
                base_score += 5

            analysis["seo_score"] = min(base_score, 100)

            # Generate optimized title
            optimized = current_title

            # Add power words if missing
            if not has_power_words:
                power_words = ['Best', 'Top', 'Ultimate', 'Complete', 'Guide to']
                optimized = f"{random.choice(power_words)} {current_title}"

            # Ensure proper length
            if len(optimized) > self.title_max_length:
                optimized = optimized[:self.title_max_length - 3] + "..."

            # Add numbers if missing and appropriate
            if not has_numbers and len(current_title.split()) > 3:
                # Could add "Top 10" or similar, but need to be careful
                pass

            analysis["optimized_title"] = optimized
            analysis["engagement_score"] = analysis["seo_score"] + 10  # Engagement often follows SEO

            # Generate improvements
            improvements = []
            if current_length > self.title_max_length:
                improvements.append(f"Title too long ({current_length} chars). Max: {self.title_max_length}")
            if not has_numbers and not has_question:
                improvements.append("Consider adding numbers or questions for better engagement")
            if not has_power_words:
                improvements.append("Add power words like 'Best', 'Top', 'Ultimate'")

            analysis["improvements"] = improvements

            # Keyword suggestions
            analysis["keyword_suggestions"] = self._extract_keywords_from_title(current_title)

            return analysis

        except Exception as e:
            logger.error(f"Failed to optimize title: {e}")
            return {"error": str(e)}

    async def optimize_description(self, current_description: str, video_title: str) -> Dict[str, Any]:
        """
        Optimize video description for SEO and engagement

        Args:
            current_description: Current description
            video_title: Video title for context

        Returns:
            Description optimization results
        """
        try:
            analysis = {
                "current_length": len(current_description),
                "optimized_description": "",
                "seo_score": 0,
                "engagement_score": 0,
                "improvements": [],
                "keyword_density": {}
            }

            # Analyze current description
            has_timestamps = bool(re.search(r'\d{1,2}:\d{2}', current_description))
            has_links = 'http' in current_description
            has_emojis = any(ord(char) > 127 for char in current_description)
            has_cta = any(word in current_description.lower() for word in
                         ['subscribe', 'like', 'comment', 'share', 'follow'])

            # Calculate SEO score
            seo_score = 40  # Base score
            if has_timestamps:
                seo_score += 20
            if has_links:
                seo_score += 10
            if len(current_description) >= 150:  # Good length
                seo_score += 15
            if has_cta:
                seo_score += 15

            analysis["seo_score"] = min(seo_score, 100)

            # Generate optimized description
            optimized = current_description

            # Add timestamps if missing
            if not has_timestamps and len(current_description) > 200:
                optimized = "0:00 - Introduction\n" + optimized

            # Add CTA if missing
            if not has_cta:
                cta = "\n\n👍 Like and subscribe for more content!\n💬 Comment your questions below\n🔗 Links in description"
                if len(optimized + cta) <= self.description_max_length:
                    optimized += cta

            # Ensure proper length
            if len(optimized) > self.description_max_length:
                optimized = optimized[:self.description_max_length - 50] + "\n\n... (truncated)"

            analysis["optimized_description"] = optimized
            analysis["engagement_score"] = min(seo_score + 10, 100)

            # Improvements
            improvements = []
            if not has_timestamps:
                improvements.append("Add chapter timestamps for better navigation")
            if not has_cta:
                improvements.append("Include clear call-to-action (subscribe, like, comment)")
            if len(current_description) < 150:
                improvements.append("Expand description with more details and keywords")
            if not has_links:
                improvements.append("Add relevant links to resources, social media, etc.")

            analysis["improvements"] = improvements

            return analysis

        except Exception as e:
            logger.error(f"Failed to optimize description: {e}")
            return {"error": str(e)}

    async def optimize_tags(self, current_tags: List[str], title: str, description: str) -> Dict[str, Any]:
        """
        Optimize video tags for better discoverability

        Args:
            current_tags: Current tags list
            title: Video title
            description: Video description

        Returns:
            Tag optimization results
        """
        try:
            analysis = {
                "current_tags": current_tags,
                "optimized_tags": [],
                "optimization_score": 0,
                "improvements": [],
                "tag_coverage": {}
            }

            # Analyze current tags
            current_count = len(current_tags)

            # Extract keywords from title and description
            title_keywords = self._extract_keywords(title)
            description_keywords = self._extract_keywords(description)

            # Combine and prioritize keywords
            all_keywords = list(set(title_keywords + description_keywords))

            # Create optimized tag list
            optimized_tags = []

            # Keep existing relevant tags
            optimized_tags.extend(current_tags[:5])  # Keep up to 5 existing tags

            # Add extracted keywords
            for keyword in all_keywords[:10]:  # Add up to 10 more
                if keyword not in optimized_tags and len(keyword) <= 50:
                    optimized_tags.append(keyword)

            # Ensure we don't exceed limits
            optimized_tags = optimized_tags[:self.tags_max_count]

            # Convert to lowercase and clean
            optimized_tags = [tag.lower().strip() for tag in optimized_tags if tag.strip()]

            analysis["optimized_tags"] = optimized_tags

            # Calculate optimization score
            score = 50  # Base score
            if current_count >= 5:
                score += 15
            if current_count <= self.tags_max_count:
                score += 15
            if len(set(optimized_tags)) > len(current_tags):
                score += 20  # Added new relevant tags

            analysis["optimization_score"] = min(score, 100)

            # Improvements
            improvements = []
            if current_count < 5:
                improvements.append(f"Add more tags (currently {current_count}, recommended: 8-12)")
            if current_count > self.tags_max_count:
                improvements.append(f"Too many tags (currently {current_count}, max: {self.tags_max_count})")
            if not any(tag in title.lower() for tag in current_tags):
                improvements.append("Include keywords from your title in tags")

            analysis["improvements"] = improvements

            return analysis

        except Exception as e:
            logger.error(f"Failed to optimize tags: {e}")
            return {"error": str(e)}

    async def suggest_thumbnail_ideas(self, title: str, description: str) -> Dict[str, Any]:
        """
        Generate thumbnail design suggestions

        Args:
            title: Video title
            description: Video description

        Returns:
            Thumbnail suggestions
        """
        try:
            suggestions = {
                "design_ideas": [],
                "color_schemes": [],
                "text_overlay_suggestions": [],
                "best_practices": []
            }

            # Extract key elements from title
            title_words = title.split()
            key_elements = [word for word in title_words if len(word) > 3][:3]

            # Generate design ideas based on content type
            content_type = self._detect_content_type(title, description)

            if content_type == "tutorial":
                suggestions["design_ideas"] = [
                    "Step-by-step numbered icons",
                    "Before/after comparison split",
                    "Progress bar or completion meter",
                    "Hand-drawn arrows pointing to key elements"
                ]
                suggestions["color_schemes"] = ["Blue and green (educational)", "Clean white background"]

            elif content_type == "review":
                suggestions["design_ideas"] = [
                    "Product images with rating stars",
                    "Pros/cons split design",
                    "Face expressions showing reaction",
                    "Comparison charts or graphs"
                ]
                suggestions["color_schemes"] = ["Red and black (attention-grabbing)", "Brand colors"]

            elif content_type == "list":
                suggestions["design_ideas"] = [
                    "Numbered list graphics",
                    "Top X badge or trophy",
                    "Collage of multiple items",
                    "Countdown style numbers"
                ]
                suggestions["color_schemes"] = ["Bright and colorful", "High contrast"]

            else:
                suggestions["design_ideas"] = [
                    "Bold text with question mark",
                    "Face showing emotion",
                    "Relevant imagery with text overlay",
                    "Minimalist design with key message"
                ]
                suggestions["color_schemes"] = ["Brand colors", "High contrast colors"]

            # Text overlay suggestions
            suggestions["text_overlay_suggestions"] = [
                f"\"{key_elements[0] if key_elements else 'WATCH NOW'}\"" if key_elements else "WATCH NOW",
                "You Won't Believe #X",
                "SHOCKING Results!",
                "Must-See Content"
            ]

            # Best practices
            suggestions["best_practices"] = [
                "Use high-contrast colors for text readability",
                "Include your face or a person for connection",
                "Keep text concise (5-7 words max)",
                "Use bright, eye-catching colors",
                "Test different versions for best performance"
            ]

            return suggestions

        except Exception as e:
            logger.error(f"Failed to suggest thumbnail ideas: {e}")
            return {"error": str(e)}

    # Private helper methods

    def _extract_keywords_from_title(self, title: str) -> List[str]:
        """Extract potential keywords from title"""
        words = title.lower().split()
        keywords = []

        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]

        # Get top words as keywords
        keywords.extend(filtered_words[:5])

        return keywords

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction (would use NLP in production)
        words = text.lower().split()
        keywords = []

        # Remove punctuation and filter
        clean_words = [word.strip(string.punctuation) for word in words]
        clean_words = [word for word in clean_words if len(word) > 2]

        # Remove stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        filtered_words = [word for word in clean_words if word not in stop_words]

        # Count frequency and get top keywords
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in sorted_words[:10]]

        return keywords

    def _detect_content_type(self, title: str, description: str) -> str:
        """Detect content type from title and description"""
        text = (title + " " + description).lower()

        if any(word in text for word in ['tutorial', 'how to', 'guide', 'learn']):
            return "tutorial"
        elif any(word in text for word in ['review', 'tested', 'unboxing']):
            return "review"
        elif any(word in text for word in ['top', 'best', 'list', 'ranking']):
            return "list"
        elif any(word in text for word in ['vs', 'versus', 'comparison', 'compared']):
            return "comparison"
        else:
            return "general"

    def _generate_metadata_recommendations(self, title_opt: Dict, desc_opt: Dict,
                                         tags_opt: Dict, thumb_opt: Dict) -> List[str]:
        """Generate overall metadata recommendations"""
        recommendations = []

        # Title recommendations
        if title_opt.get("seo_score", 0) < 70:
            recommendations.append("Optimize title for better SEO and engagement")

        # Description recommendations
        if desc_opt.get("seo_score", 0) < 60:
            recommendations.append("Improve description with timestamps and clear CTAs")

        # Tags recommendations
        if tags_opt.get("optimization_score", 0) < 60:
            recommendations.append("Add more relevant tags including keywords from title")

        # Thumbnail recommendations
        recommendations.append("Create custom thumbnails using the suggested design ideas")

        # Overall recommendations
        recommendations.extend([
            "A/B test different titles and thumbnails",
            "Monitor performance and iterate based on data",
            "Use YouTube Analytics to understand what works"
        ])

        return recommendations

    async def analyze_title_performance(self, titles: List[str],
                                      performance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze title performance patterns

        Args:
            titles: List of video titles
            performance_data: Corresponding performance data

        Returns:
            Title performance analysis
        """
        try:
            analysis = {
                "title_patterns": {},
                "best_performing_elements": [],
                "recommendations": []
            }

            # Analyze common patterns
            patterns = {
                "questions": sum(1 for title in titles if "?" in title),
                "numbers": sum(1 for title in titles if any(char.isdigit() for char in title)),
                "emojis": sum(1 for title in titles if any(ord(char) > 127 for char in title)),
                "caps": sum(1 for title in titles if any(char.isupper() for char in title)),
                "power_words": sum(1 for title in titles if any(word in title.lower() for word in
                               ['best', 'top', 'ultimate', 'shocking', 'secret']))
            }

            analysis["title_patterns"] = patterns

            # Identify best performing elements
            if performance_data:
                # Simple correlation (would be more sophisticated in production)
                if patterns["questions"] > patterns["numbers"]:
                    analysis["best_performing_elements"].append("Question-based titles")
                else:
                    analysis["best_performing_elements"].append("Numbered list titles")

                if patterns["power_words"] > len(titles) * 0.3:
                    analysis["best_performing_elements"].append("Power words")

            # Generate recommendations
            analysis["recommendations"] = [
                "Test question-based titles for higher engagement",
                "Include numbers in titles for list-based content",
                "Use power words strategically but not excessively",
                "Keep titles under 60 characters for mobile display"
            ]

            return analysis

        except Exception as e:
            logger.error(f"Failed to analyze title performance: {e}")
            return {"error": str(e)}
