# SPDX-FileCopyrightText: Copyright (c) 2024-2025, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import Optional

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig


class NetworkProductRecommendationAgentConfig(FunctionBaseConfig, name="network_product_recommendation_agent"):
    """
    Advanced network product recommendation agent that combines curated knowledge 
    with real-time internet search for the latest product information and pricing.
    """
    max_results: int = 3
    tavily_api_key: str = ""
    include_real_time_search: bool = True
    include_specifications: bool = True
    include_pricing: bool = True


@register_function(config_type=NetworkProductRecommendationAgentConfig)
async def network_product_recommendation_agent(tool_config: NetworkProductRecommendationAgentConfig, builder: Builder):
    
    async def _recommend_network_products(query: str) -> str:
        """
        Advanced network product recommendation agent that provides intelligent recommendations
        by combining curated product knowledge with real-time internet search.
        
        Args:
            query (str): User query about network products, requirements, or specific use cases
        
        Returns:
            str: Comprehensive recommendations with product details, specifications, real-time pricing, 
                 and buying advice
        """
        
        # Initialize result
        result = "# 🌐 Network Product Recommendation Agent\n\n"
        
        # Parse query to understand requirements
        query_lower = query.lower()
        
        # Determine product category and requirements
        categories = []
        business_size = "unknown"
        budget_mentioned = False
        specific_features = []
        
        # Category detection
        if any(word in query_lower for word in ["router", "routing", "wan", "internet"]):
            categories.append("router")
        if any(word in query_lower for word in ["switch", "switching", "lan", "port"]):
            categories.append("switch")
        if any(word in query_lower for word in ["firewall", "security", "vpn", "protection"]):
            categories.append("firewall")
        if any(word in query_lower for word in ["wifi", "wireless", "access point", "ap"]):
            categories.append("wireless")
        
        # Business size detection
        if any(word in query_lower for word in ["enterprise", "large", "corporation", "campus"]):
            business_size = "enterprise"
        elif any(word in query_lower for word in ["small", "soho", "home office", "startup"]):
            business_size = "small"
        elif any(word in query_lower for word in ["medium", "mid-size", "growing"]):
            business_size = "medium"
        
        # Budget detection
        if any(word in query_lower for word in ["budget", "cheap", "affordable", "cost", "price"]):
            budget_mentioned = True
        
        # Feature detection
        if "poe" in query_lower:
            specific_features.append("PoE support")
        if any(word in query_lower for word in ["vpn", "remote"]):
            specific_features.append("VPN capabilities")
        if "stack" in query_lower:
            specific_features.append("Stackable design")
        if any(word in query_lower for word in ["10g", "10 gig", "10 gigabit"]):
            specific_features.append("10 Gigabit support")
        if "wifi 6" in query_lower or "802.11ax" in query_lower:
            specific_features.append("WiFi 6 (802.11ax)")
        
        # Add query analysis to result
        result += f"**Query Analysis:** {query}\n\n"
        if categories:
            result += f"**Detected Categories:** {', '.join(categories).title()}\n"
        if business_size != "unknown":
            result += f"**Business Size:** {business_size.title()}\n"
        if specific_features:
            result += f"**Key Requirements:** {', '.join(specific_features)}\n"
        result += "\n"
        
        # If no specific category detected, provide overview
        if not categories:
            result += "Since you didn't specify a particular type of network equipment, here's a comprehensive overview:\n\n"
            categories = ["router", "switch", "firewall"]
        
        # Get recommendations for each category
        for category in categories:
            result += await _get_category_recommendations(
                category, business_size, specific_features, budget_mentioned, tool_config
            )
        
        # Add real-time search if enabled
        if tool_config.include_real_time_search and tool_config.tavily_api_key:
            result += await _get_real_time_product_info(query, categories, tool_config)
        
        # Add comprehensive buying guide
        result += _get_buying_guide(categories, business_size)
        
        # Add consultation offer
        result += "\n## 🎯 Need Personalized Recommendations?\n\n"
        result += "For more specific recommendations, please provide:\n"
        result += "• **Number of users/devices** to support\n"
        result += "• **Current network infrastructure** (if any)\n"
        result += "• **Specific requirements** (VPN users, IP cameras, etc.)\n"
        result += "• **Budget range** for the project\n"
        result += "• **Timeline** for implementation\n"
        result += "• **Technical expertise** level of your team\n\n"
        result += "💡 **Pro Tip:** Consider future growth when sizing your network equipment!\n"
        
        return result
    
    async def _get_category_recommendations(category: str, business_size: str, features: list, 
                                          budget_focus: bool, config: NetworkProductRecommendationAgentConfig) -> str:
        """Get recommendations for a specific product category"""
        
        category_data = {
            "router": {
                "title": "🔗 Router Recommendations",
                "enterprise": [
                    {
                        "brand": "Cisco",
                        "model": "ISR 4431",
                        "type": "Enterprise Branch Router",
                        "price": "$3,500-5,000",
                        "highlights": [
                            "SD-WAN ready with Cisco DNA",
                            "Integrated security and analytics",
                            "Modular design for future expansion",
                            "High availability options"
                        ],
                        "specs": "2.5 Gbps throughput, 3 WAN ports, 250W PoE",
                        "best_for": "Medium to large enterprise branch offices"
                    },
                    {
                        "brand": "Fortinet",
                        "model": "FortiGate 100F",
                        "type": "Next-Gen Firewall Router",
                        "price": "$1,200-2,000",
                        "highlights": [
                            "Integrated NGFW and SD-WAN",
                            "Advanced threat protection",
                            "SSL inspection capabilities",
                            "Centralized management"
                        ],
                        "specs": "10 Gbps firewall, 1.5 Gbps VPN, 14 ports",
                        "best_for": "Security-focused deployments"
                    }
                ],
                "small": [
                    {
                        "brand": "ASUS",
                        "model": "AX6000 (RT-AX88U)",
                        "type": "WiFi 6 Business Router",
                        "price": "$250-350",
                        "highlights": [
                            "WiFi 6 with 6000 Mbps total speed",
                            "8 Gigabit LAN ports",
                            "Advanced QoS and traffic analyzer",
                            "AiMesh support for expansion"
                        ],
                        "specs": "4x4 MU-MIMO, 1.8GHz quad-core CPU",
                        "best_for": "Small businesses with high WiFi demands"
                    },
                    {
                        "brand": "Ubiquiti",
                        "model": "Dream Machine Pro",
                        "type": "All-in-One Gateway",
                        "price": "$450-550",
                        "highlights": [
                            "Router, firewall, and switch combined",
                            "Built-in network video recorder",
                            "Advanced monitoring and analytics",
                            "Enterprise-grade management UI"
                        ],
                        "specs": "3.5 Gbps routing, 8 Gigabit ports",
                        "best_for": "Small businesses wanting enterprise features"
                    }
                ]
            },
            "switch": {
                "title": "🔌 Switch Recommendations", 
                "enterprise": [
                    {
                        "brand": "Cisco",
                        "model": "Catalyst 9300-48P",
                        "type": "Stackable Access Switch",
                        "price": "$4,000-6,500",
                        "highlights": [
                            "48 x 1G PoE+ ports + 4 x 10G uplinks",
                            "740W PoE budget for high-power devices",
                            "Stackable up to 8 units (384 ports)",
                            "Advanced security with TrustSec"
                        ],
                        "specs": "176 Gbps switching, 130.95 Mpps forwarding",
                        "best_for": "High-density access deployments"
                    },
                    {
                        "brand": "HPE Aruba",
                        "model": "6300M 48-port",
                        "type": "Campus Core Switch",
                        "price": "$8,000-12,000",
                        "highlights": [
                            "48 x 1G + 4 x 10G/25G ports",
                            "Modular design with expansion slots",
                            "Advanced automation with AI insights",
                            "Zero-touch provisioning"
                        ],
                        "specs": "2.56 Tbps switching capacity",
                        "best_for": "Campus core and distribution layers"
                    }
                ],
                "small": [
                    {
                        "brand": "Netgear",
                        "model": "ProSAFE GS728TP",
                        "type": "Smart Managed PoE Switch",
                        "price": "$400-600",
                        "highlights": [
                            "24 x Gigabit PoE+ + 4 x 10G SFP+",
                            "380W PoE budget for IP cameras/phones",
                            "VLAN and QoS support",
                            "Web-based management"
                        ],
                        "specs": "128 Gbps switching capacity",
                        "best_for": "IP camera and VoIP deployments"
                    },
                    {
                        "brand": "TP-Link",
                        "model": "TL-SG3428MP",
                        "type": "JetStream Managed Switch",
                        "price": "$300-450",
                        "highlights": [
                            "24 x Gigabit PoE+ + 4 x SFP ports",
                            "384W PoE budget",
                            "L2+ features with static routing",
                            "Centralized cloud management"
                        ],
                        "specs": "56 Gbps switching capacity",
                        "best_for": "Budget-conscious SMB deployments"
                    }
                ]
            },
            "firewall": {
                "title": "🛡️ Firewall Recommendations",
                "enterprise": [
                    {
                        "brand": "Palo Alto",
                        "model": "PA-3220",
                        "type": "Next-Generation Firewall",
                        "price": "$6,000-9,000",
                        "highlights": [
                            "App-ID and User-ID technology",
                            "Advanced threat prevention",
                            "SSL decryption and inspection",
                            "GlobalProtect VPN gateway"
                        ],
                        "specs": "2 Gbps firewall, 750 Mbps VPN",
                        "best_for": "Advanced threat protection needs"
                    },
                    {
                        "brand": "SonicWall",
                        "model": "TZ670",
                        "type": "SMB Next-Gen Firewall",
                        "price": "$400-600",
                        "highlights": [
                            "Real-time deep packet inspection",
                            "Intrusion prevention system",
                            "Content filtering service",
                            "Secure mobile access"
                        ],
                        "specs": "1.5 Gbps firewall, 100 Mbps VPN",
                        "best_for": "Small to medium business security"
                    }
                ],
                "small": [
                    {
                        "brand": "pfSense",
                        "model": "SG-3100",
                        "type": "Open Source Firewall",
                        "price": "$200-350",
                        "highlights": [
                            "Open source flexibility",
                            "VPN server capabilities",
                            "Traffic shaping and monitoring",
                            "Extensive package ecosystem"
                        ],
                        "specs": "1 Gbps firewall, 3 x 1G ports",
                        "best_for": "Budget deployments with tech-savvy teams"
                    },
                    {
                        "brand": "WatchGuard",
                        "model": "Firebox T40",
                        "type": "Unified Threat Management",
                        "price": "$300-500",
                        "highlights": [
                            "Integrated security services",
                            "Easy setup and management",
                            "Application control",
                            "Reliable support and updates"
                        ],
                        "specs": "940 Mbps firewall, 75 Mbps VPN",
                        "best_for": "Small businesses needing simple security"
                    }
                ]
            }
        }
        
        if category not in category_data:
            return f"## ❌ Category '{category}' not supported\n\n"
        
        cat_info = category_data[category]
        result = f"## {cat_info['title']}\n\n"
        
        # Select appropriate products based on business size
        if business_size == "enterprise":
            products = cat_info.get("enterprise", cat_info.get("small", []))
        elif business_size in ["small", "medium"]:
            products = cat_info.get("small", [])
        else:
            # Show both enterprise and small business options
            products = cat_info.get("enterprise", [])[:1] + cat_info.get("small", [])[:1]
        
        # Filter by budget if mentioned
        if budget_focus:
            products = sorted(products, key=lambda x: int(x["price"].split("$")[1].split(",")[0].replace("-", "")))
        
        for i, product in enumerate(products[:config.max_results], 1):
            result += f"### {i}. {product['brand']} {product['model']}\n"
            result += f"**Type:** {product['type']}\n"
            result += f"**Price Range:** {product['price']}\n"
            result += f"**Best For:** {product['best_for']}\n\n"
            
            result += "**Key Highlights:**\n"
            for highlight in product['highlights']:
                result += f"• {highlight}\n"
            
            if config.include_specifications:
                result += f"\n**Specifications:** {product['specs']}\n"
            
            result += "\n---\n\n"
        
        return result
    
    async def _get_real_time_product_info(query: str, categories: list, config: NetworkProductRecommendationAgentConfig) -> str:
        """Get real-time product information using internet search"""
        
        if not config.tavily_api_key:
            return ""
        
        try:
            # Set up Tavily API
            if not os.environ.get("TAVILY_API_KEY"):
                os.environ["TAVILY_API_KEY"] = config.tavily_api_key
            
            from langchain_community.tools import TavilySearchResults
            
            result = "## 🔍 Latest Market Information\n\n"
            
            # Search for latest product information
            search_query = f"best {' '.join(categories)} 2024 network equipment latest prices reviews"
            
            tavily_search = TavilySearchResults(max_results=3)
            search_docs = await tavily_search.ainvoke({'query': search_query})
            
            result += "**Recent Market Updates:**\n\n"
            for i, doc in enumerate(search_docs, 1):
                result += f"{i}. **{doc.get('title', 'Latest Info')}**\n"
                result += f"   {doc.get('content', '')[:200]}...\n"
                result += f"   🔗 [Read more]({doc.get('url', '')})\n\n"
            
            result += "---\n\n"
            return result
            
        except Exception as e:
            return f"## ⚠️ Real-time search unavailable\n\nNote: Could not fetch latest market information ({str(e)})\n\n---\n\n"
    
    def _get_buying_guide(categories: list, business_size: str) -> str:
        """Generate comprehensive buying guide"""
        
        result = "## 📋 Complete Buying Guide\n\n"
        
        # General considerations
        result += "### 🎯 Key Selection Criteria\n\n"
        result += "**1. Performance Requirements**\n"
        result += "• Bandwidth needs (current and 3-year projection)\n"
        result += "• Number of concurrent users and devices\n"
        result += "• Application requirements (video, VoIP, file sharing)\n"
        result += "• Latency sensitivity of applications\n\n"
        
        result += "**2. Scalability Planning**\n"
        result += "• Growth projection for next 3-5 years\n"
        result += "• Modular vs fixed-configuration options\n"
        result += "• Stackability and clustering capabilities\n"
        result += "• Upgrade path considerations\n\n"
        
        result += "**3. Management and Support**\n"
        result += "• IT team technical expertise level\n"
        result += "• Centralized vs distributed management\n"
        result += "• Vendor support quality and availability\n"
        result += "• Training and certification requirements\n\n"
        
        # Category-specific advice
        if "router" in categories:
            result += "### 🔗 Router-Specific Considerations\n"
            result += "• WAN connection types and redundancy\n"
            result += "• SD-WAN capabilities for multi-site\n"
            result += "• Security features (built-in firewall, VPN)\n"
            result += "• QoS and traffic prioritization\n\n"
        
        if "switch" in categories:
            result += "### 🔌 Switch-Specific Considerations\n"
            result += "• Port density and PoE requirements\n"
            result += "• Uplink bandwidth and redundancy\n"
            result += "• Layer 2 vs Layer 3 switching needs\n"
            result += "• VLAN and security features\n\n"
        
        if "firewall" in categories:
            result += "### 🛡️ Firewall-Specific Considerations\n"
            result += "• Threat protection capabilities\n"
            result += "• VPN capacity and performance\n"
            result += "• SSL inspection requirements\n"
            result += "• Compliance and reporting needs\n\n"
        
        # Implementation timeline
        result += "### 📅 Implementation Timeline\n\n"
        result += "**Phase 1: Planning (2-4 weeks)**\n"
        result += "• Requirements gathering and site survey\n"
        result += "• Vendor evaluation and proof of concept\n"
        result += "• Budget approval and procurement\n\n"
        
        result += "**Phase 2: Preparation (1-2 weeks)**\n"
        result += "• Equipment delivery and staging\n"
        result += "• Configuration preparation\n"
        result += "• Migration planning\n\n"
        
        result += "**Phase 3: Implementation (1-3 days)**\n"
        result += "• Equipment installation and cabling\n"
        result += "• Configuration deployment\n"
        result += "• Testing and cutover\n\n"
        
        result += "**Phase 4: Optimization (1-2 weeks)**\n"
        result += "• Performance monitoring and tuning\n"
        result += "• User training and documentation\n"
        result += "• Warranty registration and support setup\n\n"
        
        return result

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _recommend_network_products,
        description="""Advanced network product recommendation agent that provides comprehensive, 
        intelligent recommendations for routers, switches, firewalls, and wireless equipment.
        
        This agent combines:
        - Curated product database with specifications
        - Real-time market information via internet search
        - Business size and requirement analysis
        - Complete buying guides and implementation timelines
        - Vendor-neutral recommendations
        
        Perfect for:
        - IT professionals planning network upgrades
        - Business owners needing network infrastructure
        - Technical consultants requiring product comparisons
        - Anyone seeking expert network equipment advice
        
        Args:
            query (str): Network requirements, product questions, or use case description
        """,
    )