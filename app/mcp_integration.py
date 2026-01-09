"""
MCP Integration for YouTube Agent

Demonstrates how agents can automatically discover and utilize MCP capabilities.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

# Import the shared MCP registry and activation manager
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent / 'admin' / 'shared'))
from mcp_registry import (
    get_mcp_registry,
    reflect_on_mcp_capabilities,
    activate_mcps_for_task,
    get_context_optimized_mcp_recommendations,
    optimize_mcp_context_usage,
    MCPTool
)

logger = logging.getLogger(__name__)


class YouTubeMCPIntegration:
    """
    MCP integration layer for YouTube agent.

    This class demonstrates how agents can:
    1. Automatically discover available MCPs
    2. Reflect on their capabilities
    3. Utilize MCP tools for operations
    """

    def __init__(self):
        self.registry = get_mcp_registry()
        self.youtube_mcps: List[str] = []
        self.available_tools: Dict[str, List[MCPTool]] = {}
        self._initialized = False

    async def initialize(self):
        """Initialize MCP integration by discovering available YouTube MCPs"""
        if self._initialized:
            return

        try:
            # Discover available YouTube MCPs
            self.youtube_mcps = await self.registry.get_available_servers_for_service('youtube')

            if self.youtube_mcps:
                logger.info(f"Found YouTube MCPs: {self.youtube_mcps}")

                # Get available tools for each MCP
                tools_by_server = await self.registry.get_tools_for_service('youtube')
                self.available_tools = tools_by_server

                # Log discovered capabilities
                for server_name, tools in self.available_tools.items():
                    logger.info(f"YouTube MCP '{server_name}' provides {len(tools)} tools")
                    for tool in tools:
                        logger.debug(f"  - {tool.name}: {tool.description}")

            else:
                logger.warning("No YouTube MCPs found - agent will operate in limited mode")

            self._initialized = True

        except Exception as e:
            logger.error(f"Failed to initialize YouTube MCP integration: {e}")
            self._initialized = False

    async def reflect_on_capabilities(self, context: str = "") -> Dict[str, Any]:
        """
        Allow the agent to reflect on available MCP capabilities

        Args:
            context: Context about what the agent needs

        Returns:
            Dictionary describing available capabilities
        """
        await self.initialize()

        reflection = await self.registry.reflect_on_capabilities(
            f"YouTube agent needs: {context}"
        )

        # Focus on YouTube-specific capabilities
        youtube_capabilities = reflection.get('mcp_capabilities', {}).get('youtube', {})

        return {
            'youtube_mcp_available': youtube_capabilities.get('status') == 'available',
            'available_servers': youtube_capabilities.get('available_servers', []),
            'available_tools': youtube_capabilities.get('tools', {}),
            'full_reflection': reflection
        }

    async def search_videos(self, query: str, max_results: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Search for YouTube videos using available MCPs

        Args:
            query: Search query
            max_results: Maximum results to return
            **kwargs: Additional search parameters

        Returns:
            Search results
        """
        await self.initialize()

        if not self.youtube_mcps:
            return {
                'success': False,
                'error': 'No YouTube MCPs available',
                'fallback_mode': True
            }

        # Use the first available MCP (could implement load balancing/failover)
        primary_mcp = self.youtube_mcps[0]

        try:
            result = await self.registry.execute_tool(
                primary_mcp,
                'search_videos',
                {
                    'query': query,
                    'maxResults': max_results,
                    **kwargs
                }
            )

            return {
                'success': True,
                'mcp_used': primary_mcp,
                'results': result,
                'query': query
            }

        except Exception as e:
            logger.error(f"YouTube search failed via MCP {primary_mcp}: {e}")
            return {
                'success': False,
                'error': str(e),
                'mcp_used': primary_mcp
            }

    async def get_channel_info(self, channel_id: str = None, **kwargs) -> Dict[str, Any]:
        """Get channel information using MCP"""
        await self.initialize()

        if not self.youtube_mcps:
            return {'success': False, 'error': 'No YouTube MCPs available'}

        primary_mcp = self.youtube_mcps[0]

        try:
            result = await self.registry.execute_tool(
                primary_mcp,
                'get_channel_info',
                {'channelId': channel_id, **kwargs}
            )

            return {
                'success': True,
                'mcp_used': primary_mcp,
                'channel_info': result
            }

        except Exception as e:
            logger.error(f"Channel info retrieval failed: {e}")
            return {'success': False, 'error': str(e)}

    async def get_video_details(self, video_ids: List[str], **kwargs) -> Dict[str, Any]:
        """Get video details using MCP"""
        await self.initialize()

        if not self.youtube_mcps:
            return {'success': False, 'error': 'No YouTube MCPs available'}

        primary_mcp = self.youtube_mcps[0]

        try:
            result = await self.registry.execute_tool(
                primary_mcp,
                'get_video_details',
                {'videoIds': video_ids, **kwargs}
            )

            return {
                'success': True,
                'mcp_used': primary_mcp,
                'video_details': result
            }

        except Exception as e:
            logger.error(f"Video details retrieval failed: {e}")
            return {'success': False, 'error': str(e)}

    async def update_video_metadata(self, video_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update video metadata using MCP"""
        await self.initialize()

        if not self.youtube_mcps:
            return {'success': False, 'error': 'No YouTube MCPs available'}

        primary_mcp = self.youtube_mcps[0]

        try:
            result = await self.registry.execute_tool(
                primary_mcp,
                'update_video_metadata',
                {'videoId': video_id, **updates}
            )

            return {
                'success': True,
                'mcp_used': primary_mcp,
                'update_result': result
            }

        except Exception as e:
            logger.error(f"Video metadata update failed: {e}")
            return {'success': False, 'error': str(e)}

    async def get_available_tools(self) -> Dict[str, List[MCPTool]]:
        """Get all available YouTube MCP tools"""
        await self.initialize()
        return self.available_tools

    async def health_check(self) -> Dict[str, Any]:
        """Check MCP integration health"""
        await self.initialize()

        return {
            'initialized': self._initialized,
            'youtube_mcps_available': len(self.youtube_mcps) > 0,
            'available_mcps': self.youtube_mcps,
            'total_tools': sum(len(tools) for tools in self.available_tools.values()),
            'registry_status': 'connected' if self.registry else 'disconnected'
        }

    async def activate_for_task(self, task_description: str) -> Dict[str, Any]:
        """
        Context-aware MCP activation for YouTube tasks

        Automatically activates relevant MCPs based on task while managing context window

        Args:
            task_description: What the agent needs to do

        Returns:
            Activation results with context optimization
        """
        return await activate_mcps_for_task(
            f"YouTube agent: {task_description}",
            agent_type="google_youtube_agent"
        )

    async def get_context_optimized_recommendations(self, task_description: str) -> Dict[str, Any]:
        """
        Get comprehensive MCP recommendations with context optimization

        Args:
            task_description: What the agent plans to do

        Returns:
            Full recommendations including capability discovery and activation
        """
        return await get_context_optimized_mcp_recommendations(
            f"YouTube operations: {task_description}",
            agent_type="google_youtube_agent"
        )

    async def optimize_context_usage(self) -> Dict[str, Any]:
        """Optimize MCP usage for better context efficiency"""
        return await optimize_mcp_context_usage()

    async def context_aware_search_videos(self, query: str, max_results: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Context-aware video search that ensures MCPs are activated

        Args:
            query: Search query
            max_results: Maximum results
            **kwargs: Additional parameters

        Returns:
            Search results with context management
        """
        # Ensure YouTube MCP is activated for this task
        activation_result = await self.activate_for_task(f"search for videos about: {query}")

        # Proceed with search
        search_result = await self.search_videos(query, max_results, **kwargs)

        # Add activation context to result
        search_result['activation_context'] = {
            'activated_services': activation_result.get('activated_services', []),
            'context_efficiency': activation_result.get('context_efficiency', 0)
        }

        return search_result


# Convenience functions for agent usage
async def get_youtube_capabilities(context: str = "") -> Dict[str, Any]:
    """
    Convenience function for agents to check YouTube MCP capabilities

    Usage:
        capabilities = await get_youtube_capabilities("I need video analytics")
        if capabilities['youtube_mcp_available']:
            # Use MCP tools
            pass
    """
    return await reflect_on_mcp_capabilities(f"YouTube agent: {context}")


async def create_youtube_mcp_client() -> YouTubeMCPIntegration:
    """Create and initialize a YouTube MCP client"""
    client = YouTubeMCPIntegration()
    await client.initialize()
    return client


# Example usage for agents
async def example_agent_usage():
    """Example of how an agent would use the context-aware MCP integration"""

    print("=== Context-Aware YouTube MCP Integration Example ===\n")

    # Initialize MCP integration
    mcp_client = await create_youtube_mcp_client()

    # 1. Get context-optimized recommendations before starting
    print("1. Getting context-optimized MCP recommendations:")
    recommendations = await mcp_client.get_context_optimized_recommendations("analyze video performance and create content strategy")
    print(f"   Available services: {list(recommendations.get('available_capabilities', {}).get('mcp_capabilities', {}).keys())}")
    suggestions = recommendations.get('context_optimized_suggestions', [])
    if suggestions:
        print(f"   Context suggestions: {suggestions[0]}")

    # 2. Activate MCPs for specific task
    print("\n2. Activating MCPs for video analysis task:")
    activation = await mcp_client.activate_for_task("analyze YouTube video performance metrics")
    activated = activation.get('activated_services', [])
    print(f"   Activated services: {activated}")
    print(".1f")

    # 3. Use context-aware search (automatically manages activation)
    print("\n3. Context-aware video search:")
    search_results = await mcp_client.context_aware_search_videos("Python tutorials", max_results=3)
    if search_results['success']:
        videos_found = len(search_results.get('results', {}).get('videos', []))
        print(f"   Found {videos_found} videos")
        activation_ctx = search_results.get('activation_context', {})
        print(f"   Context efficiency: {activation_ctx.get('context_efficiency', 0):.1f}%")

    # 4. Traditional MCP usage (for comparison)
    if search_results.get('results', {}).get('videos'):
        print("\n4. Traditional MCP tool usage:")
        video_id = search_results['results']['videos'][0]['id']['videoId']
        details = await mcp_client.get_video_details([video_id])
        if details['success']:
            print(f"   Got details for video: {video_id}")

    # 5. Context optimization
    print("\n5. Optimizing context usage:")
    optimization = await mcp_client.optimize_context_usage()
    deactivated = optimization.get('deactivated_services', [])
    if deactivated:
        print(f"   Deactivated unused MCPs: {deactivated}")
    else:
        print("   No unused MCPs to deactivate")

    # 6. Health check with context status
    print("\n6. MCP Integration Health:")
    health = await mcp_client.health_check()
    print(f"   Initialized: {health['initialized']}")
    print(f"   YouTube MCPs available: {health['youtube_mcps_available']}")
    print(f"   Total tools: {health['total_tools']}")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    # Run example
    asyncio.run(example_agent_usage())
