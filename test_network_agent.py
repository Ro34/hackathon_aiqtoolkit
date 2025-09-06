#!/usr/bin/env python3
"""
Simple test script for the network product recommendation agent.
This script demonstrates how to use the agent without requiring full installation.
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_network_product_tools():
    """Test the network product recommendation tools"""
    
    print("🌐 Testing Network Product Recommendation Tools\n")
    print("=" * 60)
    
    # Test the basic network product search tool
    try:
        from aiq.tool.network_product_search import NetworkProductSearchConfig
        from aiq.builder.builder import Builder
        
        # Mock builder for testing
        class MockBuilder:
            pass
        
        # Test configuration
        config = NetworkProductSearchConfig(
            max_results=3,
            include_specifications=True
        )
        
        print("\n✅ Network Product Search Tool loaded successfully")
        print(f"   Configuration: max_results={config.max_results}")
        
    except ImportError as e:
        print(f"❌ Failed to import network product search tool: {e}")
        return False
    
    # Test the advanced recommendation agent
    try:
        from aiq.tool.network_product_recommendation_agent import NetworkProductRecommendationAgentConfig
        
        config = NetworkProductRecommendationAgentConfig(
            max_results=3,
            include_real_time_search=False,  # Disable for testing
            include_specifications=True
        )
        
        print("✅ Network Product Recommendation Agent loaded successfully")
        print(f"   Configuration: max_results={config.max_results}")
        
    except ImportError as e:
        print(f"❌ Failed to import recommendation agent: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All network product tools loaded successfully!")
    print("\nExample queries you can try:")
    print("• '推荐一个企业级路由器'")
    print("• '需要支持PoE的交换机'") 
    print("• '小企业防火墙推荐'")
    print("• '路由器和交换机组合方案'")
    
    return True

def demo_product_search():
    """Demonstrate the product search functionality"""
    
    print("\n🔍 Demonstration: Network Product Search")
    print("=" * 50)
    
    # Simulate product search results
    demo_queries = [
        "企业级路由器推荐",
        "支持PoE的交换机", 
        "小企业防火墙",
        "WiFi 6 路由器"
    ]
    
    for query in demo_queries:
        print(f"\n📝 Query: {query}")
        print(f"   Category detected: {'router' if '路由器' in query else 'switch' if '交换机' in query else 'firewall' if '防火墙' in query else 'various'}")
        print(f"   Business size: {'enterprise' if '企业' in query else 'small business'}")
        print(f"   Special features: {'PoE support' if 'PoE' in query else 'WiFi 6' if 'WiFi 6' in query else 'standard'}")
    
    print("\n✨ The agent will provide detailed recommendations with:")
    print("   • Product specifications and features")
    print("   • Pricing information")
    print("   • Use case recommendations") 
    print("   • Buying guides and implementation tips")

if __name__ == "__main__":
    print("🚀 Network Product Recommendation Agent Test")
    print("=" * 60)
    
    # Run async test
    success = asyncio.run(test_network_product_tools())
    
    if success:
        demo_product_search()
        
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        print("\nTo use this in production:")
        print("1. Make sure all dependencies are installed")
        print("2. Configure Tavily API key for real-time search")
        print("3. Start the AIQ toolkit server with the updated config")
        print("4. Query the agent through the web interface or API")
    else:
        print("\n❌ Tests failed. Please check the implementation.")
        sys.exit(1)