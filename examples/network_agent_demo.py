"""
网络产品推荐智能体使用示例
演示如何使用智能体进行网络产品推荐
"""

import asyncio
from typing import Dict, Any

class NetworkProductAgentDemo:
    """网络产品推荐智能体演示类"""
    
    def __init__(self):
        self.demo_queries = [
            "我需要一个企业级路由器用于分支机构",
            "小公司需要支持PoE的交换机，要连接20个IP摄像头",
            "推荐一个防火墙，支持VPN功能",
            "为50人的办公室设计完整的网络方案",
            "WiFi 6路由器推荐，预算在500美元以内",
            "数据中心需要高性能交换机"
        ]
    
    async def simulate_agent_response(self, query: str) -> Dict[str, Any]:
        """模拟智能体响应"""
        
        # 模拟查询分析
        analysis = self._analyze_query(query)
        
        # 模拟产品推荐
        recommendations = self._get_mock_recommendations(analysis)
        
        return {
            "query": query,
            "analysis": analysis,
            "recommendations": recommendations,
            "buying_guide": self._get_buying_guide(analysis["category"])
        }
    
    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """分析查询意图"""
        query_lower = query.lower()
        
        # 产品类别识别
        category = "综合方案"
        if "路由器" in query or "router" in query_lower:
            category = "路由器"
        elif "交换机" in query or "switch" in query_lower:
            category = "交换机"
        elif "防火墙" in query or "firewall" in query_lower:
            category = "防火墙"
        
        # 业务规模识别
        business_size = "中小企业"
        if "企业级" in query or "enterprise" in query_lower or "数据中心" in query:
            business_size = "企业级"
        
        # 特殊需求识别
        features = []
        if "poe" in query_lower or "PoE" in query:
            features.append("PoE支持")
        if "vpn" in query_lower or "VPN" in query:
            features.append("VPN功能")
        if "wifi 6" in query_lower or "WiFi 6" in query:
            features.append("WiFi 6")
        if "摄像头" in query or "camera" in query_lower:
            features.append("IP摄像头支持")
        
        # 预算检测
        budget_mentioned = any(word in query_lower for word in ["预算", "budget", "美元", "元", "价格"])
        
        return {
            "category": category,
            "business_size": business_size,
            "features": features,
            "budget_mentioned": budget_mentioned,
            "user_count": self._extract_user_count(query)
        }
    
    def _extract_user_count(self, query: str) -> int:
        """提取用户数量"""
        import re
        # 查找数字模式
        numbers = re.findall(r'\d+', query)
        if numbers:
            for num in numbers:
                if int(num) > 5:  # 假设大于5的数字是用户数
                    return int(num)
        return 0
    
    def _get_mock_recommendations(self, analysis: Dict[str, Any]) -> list:
        """获取模拟推荐"""
        category = analysis["category"]
        business_size = analysis["business_size"]
        
        recommendations = []
        
        if category == "路由器" or category == "综合方案":
            if business_size == "企业级":
                recommendations.append({
                    "产品": "Cisco ISR 4431",
                    "类型": "企业级分支路由器",
                    "价格": "$3,500-5,000",
                    "特点": ["SD-WAN就绪", "集成安全功能", "模块化设计", "高可用性"],
                    "适用": "中大型企业分支机构"
                })
            else:
                recommendations.append({
                    "产品": "ASUS AX6000 (RT-AX88U)",
                    "类型": "WiFi 6企业路由器",
                    "价格": "$250-350",
                    "特点": ["WiFi 6支持", "8个千兆端口", "高级QoS", "AiMesh支持"],
                    "适用": "小企业高性能需求"
                })
        
        if category == "交换机" or category == "综合方案":
            if "PoE支持" in analysis["features"]:
                recommendations.append({
                    "产品": "Netgear ProSAFE GS728TP",
                    "类型": "智能管理PoE交换机",
                    "价格": "$400-600",
                    "特点": ["24个千兆PoE+端口", "380W PoE预算", "VLAN支持", "Web管理"],
                    "适用": "IP摄像头和VoIP部署"
                })
            else:
                recommendations.append({
                    "产品": "Cisco Catalyst 9300-48P",
                    "类型": "可堆叠接入交换机",
                    "价格": "$4,000-6,500",
                    "特点": ["48个千兆PoE+端口", "740W PoE预算", "可堆叠", "高级安全"],
                    "适用": "企业高密度部署"
                })
        
        if category == "防火墙" or category == "综合方案":
            if "VPN功能" in analysis["features"]:
                recommendations.append({
                    "产品": "Palo Alto PA-3220",
                    "类型": "下一代防火墙",
                    "价格": "$6,000-9,000",
                    "特点": ["应用识别", "高级威胁防护", "SSL解密", "GlobalProtect VPN"],
                    "适用": "高级威胁防护需求"
                })
            else:
                recommendations.append({
                    "产品": "pfSense SG-3100",
                    "类型": "开源防火墙",
                    "价格": "$200-350",
                    "特点": ["开源灵活性", "VPN服务器", "流量整形", "包生态系统"],
                    "适用": "预算有限的技术团队"
                })
        
        return recommendations
    
    def _get_buying_guide(self, category: str) -> Dict[str, list]:
        """获取购买指南"""
        guides = {
            "路由器": [
                "考虑互联网带宽和选择能处理的路由器",
                "商业用途优先考虑安全功能和管理能力",
                "WiFi 6推荐用于未来保障",
                "评估同时连接设备数量"
            ],
            "交换机": [
                "计算所需端口数量，留20%增长缓冲",
                "考虑IP电话、摄像头、接入点的PoE需求",
                "管理型交换机提供更好的控制和监控",
                "规划上行带宽避免瓶颈"
            ],
            "防火墙": [
                "根据互联网带宽确定防火墙规格",
                "考虑远程用户的VPN需求",
                "下一代防火墙提供更好保护",
                "处理敏感数据时规划SSL检查"
            ],
            "综合方案": [
                "整体规划网络架构，考虑所有组件",
                "确保各设备间兼容性和管理一致性",
                "规划未来3-5年的扩展需求",
                "考虑统一的监控和管理平台"
            ]
        }
        
        return {
            "选择要点": guides.get(category, guides["综合方案"]),
            "实施步骤": [
                "需求收集和现场调研 (2-4周)",
                "设备采购和配置准备 (1-2周)", 
                "安装实施和测试 (1-3天)",
                "优化调试和培训 (1-2周)"
            ]
        }
    
    async def run_demo(self):
        """运行演示"""
        print("🌐 网络产品推荐智能体演示")
        print("=" * 60)
        
        for i, query in enumerate(self.demo_queries, 1):
            print(f"\n📝 示例 {i}: {query}")
            print("-" * 40)
            
            response = await self.simulate_agent_response(query)
            
            # 显示分析结果
            analysis = response["analysis"]
            print(f"🔍 分析结果:")
            print(f"   产品类别: {analysis['category']}")
            print(f"   业务规模: {analysis['business_size']}")
            if analysis['features']:
                print(f"   特殊需求: {', '.join(analysis['features'])}")
            if analysis['user_count']:
                print(f"   用户数量: {analysis['user_count']}人")
            
            # 显示推荐结果
            print(f"\n💡 推荐产品:")
            for j, rec in enumerate(response["recommendations"], 1):
                print(f"   {j}. {rec['产品']} ({rec['类型']})")
                print(f"      价格: {rec['价格']}")
                print(f"      适用: {rec['适用']}")
            
            # 显示购买建议
            guide = response["buying_guide"]
            print(f"\n📋 购买要点:")
            for point in guide["选择要点"][:2]:  # 只显示前两个要点
                print(f"   • {point}")
            
            print()

async def main():
    """主函数"""
    demo = NetworkProductAgentDemo()
    await demo.run_demo()
    
    print("\n" + "=" * 60)
    print("🎉 演示完成!")
    print("\n💡 实际使用时，智能体会提供:")
    print("   • 更详细的产品规格和对比")
    print("   • 实时价格和市场信息")
    print("   • 完整的购买和实施指南")
    print("   • 个性化的配置建议")
    print("\n🚀 启动AIQ Toolkit服务即可开始使用!")

if __name__ == "__main__":
    asyncio.run(main())