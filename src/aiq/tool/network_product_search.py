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

from typing import Optional

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig


class NetworkProductSearchConfig(FunctionBaseConfig, name="network_product_search"):
    """
    Tool for searching and recommending network products like routers, switches, firewalls.
    Combines internet search with curated product knowledge.
    """
    max_results: int = 5
    api_key: str = ""
    include_specifications: bool = True
    price_range: Optional[str] = None


@register_function(config_type=NetworkProductSearchConfig)
async def network_product_search(tool_config: NetworkProductSearchConfig, builder: Builder):
    
    async def _search_network_products(query: str) -> str:
        """
        Search for network products and provide recommendations based on query.
        
        Args:
            query (str): User query about network products (e.g., "recommend enterprise router", 
                        "best switches for small office", "firewall with VPN support")
        
        Returns:
            str: Formatted recommendations with product details, specifications, and advice
        """
        
        # Network product database with common products and their key features
        network_products = {
            "routers": {
                "enterprise": [
                    {
                        "name": "Cisco ISR 4000 Series",
                        "model": "ISR4431",
                        "type": "Enterprise Router",
                        "price_range": "$2000-5000",
                        "key_features": [
                            "High-performance routing for branch offices",
                            "Integrated security features",
                            "SD-WAN support",
                            "Modular design"
                        ],
                        "specifications": {
                            "throughput": "2.5 Gbps",
                            "wan_ports": "3",
                            "lan_ports": "3",
                            "power": "250W"
                        },
                        "use_case": "Medium to large enterprise branch offices"
                    },
                    {
                        "name": "Juniper MX Series",
                        "model": "MX240",
                        "type": "Service Provider Router",
                        "price_range": "$15000-30000",
                        "key_features": [
                            "Carrier-grade reliability",
                            "High-density 10/40/100GE interfaces",
                            "Advanced MPLS support",
                            "Network slicing capabilities"
                        ],
                        "specifications": {
                            "throughput": "480 Gbps",
                            "interface_slots": "8",
                            "redundancy": "Dual RE support",
                            "power": "AC/DC options"
                        },
                        "use_case": "Service provider edge and core networks"
                    }
                ],
                "small_business": [
                    {
                        "name": "ASUS AX6000",
                        "model": "RT-AX88U",
                        "type": "WiFi 6 Router",
                        "price_range": "$200-400",
                        "key_features": [
                            "WiFi 6 (802.11ax) support",
                            "8 Gigabit LAN ports",
                            "AiMesh support for mesh networking",
                            "Advanced QoS"
                        ],
                        "specifications": {
                            "wifi_speed": "6000 Mbps",
                            "lan_ports": "8 x Gigabit",
                            "wan_ports": "1 x Gigabit",
                            "antennas": "4 external"
                        },
                        "use_case": "Small to medium businesses, home offices"
                    },
                    {
                        "name": "Ubiquiti Dream Machine",
                        "model": "UDM-Pro",
                        "type": "All-in-One Security Gateway",
                        "price_range": "$400-600",
                        "key_features": [
                            "Integrated firewall and IDS/IPS",
                            "Network video recorder",
                            "UniFi controller built-in",
                            "Advanced threat management"
                        ],
                        "specifications": {
                            "throughput": "3.5 Gbps",
                            "lan_ports": "8 x Gigabit",
                            "wan_ports": "2 x Gigabit",
                            "storage": "HDD bay for surveillance"
                        },
                        "use_case": "Small businesses requiring integrated security"
                    }
                ]
            },
            "switches": {
                "enterprise": [
                    {
                        "name": "Cisco Catalyst 9300",
                        "model": "C9300-48P",
                        "type": "Stackable Access Switch",
                        "price_range": "$3000-6000",
                        "key_features": [
                            "48 x 1G ports + 4 x 10G uplinks",
                            "PoE+ support (740W)",
                            "Stackable up to 8 units",
                            "Advanced security with TrustSec"
                        ],
                        "specifications": {
                            "ports": "48 x 1GbE + 4 x 10GbE",
                            "poe_budget": "740W",
                            "switching_capacity": "176 Gbps",
                            "forwarding_rate": "130.95 Mpps"
                        },
                        "use_case": "Enterprise access layer, high-density deployments"
                    },
                    {
                        "name": "Arista 7050X3",
                        "model": "7050SX3-48YC8",
                        "type": "Data Center Switch",
                        "price_range": "$8000-15000",
                        "key_features": [
                            "48 x 25GbE + 8 x 100GbE ports",
                            "Ultra-low latency design",
                            "Advanced automation with EOS",
                            "Zero Touch Provisioning"
                        ],
                        "specifications": {
                            "ports": "48 x 25GbE + 8 x 100GbE",
                            "switching_capacity": "3.2 Tbps",
                            "latency": "<300ns",
                            "power": "450W"
                        },
                        "use_case": "Data center top-of-rack, high-performance computing"
                    }
                ],
                "small_business": [
                    {
                        "name": "Netgear ProSAFE",
                        "model": "GS728TP",
                        "type": "Smart Managed Switch",
                        "price_range": "$300-500",
                        "key_features": [
                            "24 x Gigabit PoE+ ports",
                            "4 x 10G SFP+ uplinks",
                            "Advanced VLAN support",
                            "Web-based management"
                        ],
                        "specifications": {
                            "ports": "24 x 1GbE PoE+ + 4 x 10GbE",
                            "poe_budget": "380W",
                            "switching_capacity": "128 Gbps",
                            "management": "Web GUI, SNMP"
                        },
                        "use_case": "Small to medium businesses, IP camera deployments"
                    }
                ]
            },
            "firewalls": [
                {
                    "name": "Palo Alto Networks",
                    "model": "PA-3220",
                    "type": "Next-Generation Firewall",
                    "price_range": "$5000-8000",
                    "key_features": [
                        "App-ID and User-ID technology",
                        "Threat prevention and WildFire",
                        "SSL decryption capabilities",
                        "GlobalProtect VPN"
                    ],
                    "specifications": {
                        "throughput": "2 Gbps",
                        "vpn_throughput": "750 Mbps",
                        "new_sessions": "66000/sec",
                        "interfaces": "8 x 1GbE + 2 x 10GbE"
                    },
                    "use_case": "Medium enterprises, advanced threat protection"
                },
                {
                    "name": "pfSense",
                    "model": "SG-3100",
                    "type": "Open Source Firewall",
                    "price_range": "$200-400",
                    "key_features": [
                        "Open source flexibility",
                        "VPN server capabilities",
                        "Traffic shaping and monitoring",
                        "Package ecosystem"
                    ],
                    "specifications": {
                        "throughput": "1 Gbps",
                        "vpn_throughput": "120 Mbps",
                        "interfaces": "3 x 1GbE",
                        "power": "15W"
                    },
                    "use_case": "Small businesses, budget-conscious deployments"
                }
            ]
        }
        
        # Parse query to understand user needs
        query_lower = query.lower()
        recommendations = []
        
        # Determine product category and business size
        if "router" in query_lower:
            if "enterprise" in query_lower or "large" in query_lower or "branch" in query_lower:
                products = network_products["routers"]["enterprise"]
                category = "Enterprise Routers"
            else:
                products = network_products["routers"]["small_business"]
                category = "Small Business Routers"
        elif "switch" in query_lower:
            if "enterprise" in query_lower or "data center" in query_lower or "high" in query_lower:
                products = network_products["switches"]["enterprise"]
                category = "Enterprise Switches"
            else:
                products = network_products["switches"]["small_business"]
                category = "Small Business Switches"
        elif "firewall" in query_lower or "security" in query_lower:
            products = network_products["firewalls"]
            category = "Firewalls"
        else:
            # General network equipment query - provide overview of all categories
            result = "# Network Product Recommendations\n\n"
            result += "Based on your query, here are recommendations across different network equipment categories:\n\n"
            
            # Add router recommendations
            result += "## Routers\n"
            result += "**For Small Business:** ASUS AX6000 (RT-AX88U) - WiFi 6 router with excellent performance\n"
            result += "**For Enterprise:** Cisco ISR 4000 Series - Reliable branch office routing with security\n\n"
            
            # Add switch recommendations
            result += "## Switches\n"
            result += "**For Small Business:** Netgear ProSAFE GS728TP - Managed switch with PoE+\n"
            result += "**For Enterprise:** Cisco Catalyst 9300 - Stackable access switch with advanced features\n\n"
            
            # Add firewall recommendations
            result += "## Firewalls\n"
            result += "**Budget Option:** pfSense SG-3100 - Open source firewall with VPN\n"
            result += "**Enterprise:** Palo Alto PA-3220 - Next-gen firewall with advanced threat protection\n\n"
            
            result += "💡 **Tip:** Please specify the type of equipment and your business size for more detailed recommendations!"
            return result
        
        # Format recommendations
        result = f"# {category} Recommendations\n\n"
        result += f"Based on your query: '{query}'\n\n"
        
        for i, product in enumerate(products[:tool_config.max_results], 1):
            result += f"## {i}. {product['name']} ({product['model']})\n"
            result += f"**Type:** {product['type']}\n"
            result += f"**Price Range:** {product['price_range']}\n"
            result += f"**Use Case:** {product['use_case']}\n\n"
            
            result += "**Key Features:**\n"
            for feature in product['key_features']:
                result += f"• {feature}\n"
            result += "\n"
            
            if tool_config.include_specifications and 'specifications' in product:
                result += "**Technical Specifications:**\n"
                for spec, value in product['specifications'].items():
                    result += f"• {spec.replace('_', ' ').title()}: {value}\n"
                result += "\n"
            
            result += "---\n\n"
        
        # Add buying advice
        result += "## 💡 Buying Advice\n\n"
        
        if "router" in query_lower:
            result += "**Router Selection Tips:**\n"
            result += "• Consider your internet speed and choose a router that can handle it\n"
            result += "• For businesses, prioritize security features and management capabilities\n"
            result += "• WiFi 6 is recommended for future-proofing\n"
            result += "• Evaluate the number of devices that will connect simultaneously\n"
        elif "switch" in query_lower:
            result += "**Switch Selection Tips:**\n"
            result += "• Calculate the number of ports needed with 20% growth buffer\n"
            result += "• Consider PoE requirements for IP phones, cameras, and access points\n"
            result += "• Managed switches offer better control and monitoring\n"
            result += "• Plan for uplink bandwidth to avoid bottlenecks\n"
        elif "firewall" in query_lower:
            result += "**Firewall Selection Tips:**\n"
            result += "• Size the firewall based on your internet bandwidth\n"
            result += "• Consider VPN requirements for remote users\n"
            result += "• Next-generation firewalls offer better protection\n"
            result += "• Plan for SSL inspection if handling sensitive data\n"
        
        result += "\n**Need more specific recommendations?** Please provide:\n"
        result += "• Your business size and number of users\n"
        result += "• Specific requirements (VPN, WiFi, PoE, etc.)\n"
        result += "• Budget constraints\n"
        result += "• Current network infrastructure\n"
        
        return result

    # Create a Generic AIQ Toolkit tool that can be used with any supported LLM framework
    yield FunctionInfo.from_fn(
        _search_network_products,
        description="""This tool provides intelligent recommendations for network products including routers, 
        switches, and firewalls. It combines curated product knowledge with specifications and buying advice.
        
        Use this tool when users ask about:
        - Network equipment recommendations
        - Product comparisons for routers, switches, firewalls
        - Technical specifications and features
        - Buying advice for network infrastructure
        - Enterprise vs small business networking solutions
        
        Args:
            query (str): User's network product inquiry or requirements
        """,
    )