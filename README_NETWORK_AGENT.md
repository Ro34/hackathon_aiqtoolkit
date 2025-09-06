# 网络产品推荐智能体 (Network Product Recommendation Agent)

## 🎯 项目概述

基于NVIDIA NeMo Agent Toolkit实现的专业网络产品推荐智能体，能够智能分析用户需求并推荐合适的网络设备（路由器、交换机、防火墙等）。

## ✨ 核心特性

### 🧠 智能查询理解
- **自然语言处理**: 理解中英文混合查询
- **意图识别**: 自动识别产品类别、业务规模、特殊需求
- **需求分析**: 提取用户数量、预算、技术要求等关键信息

### 📊 专业产品推荐
- **多产品类别**: 路由器、交换机、防火墙、无线设备
- **分级推荐**: 企业级 vs 中小企业解决方案
- **规格详解**: 技术参数、性能指标、适用场景
- **价格区间**: 预算范围和性价比分析

### 🔍 实时市场信息
- **动态搜索**: 集成Tavily API获取最新产品信息
- **价格更新**: 实时市场价格和促销信息
- **用户评价**: 最新评测和用户反馈

### 📋 完整购买指南
- **选型要点**: 针对性的技术建议
- **实施计划**: 从规划到部署的完整时间表
- **风险提醒**: 常见误区和注意事项

## 🏗️ 技术架构

```
用户查询 → React Agent → 网络产品推荐工具 → 结果整合 → 响应输出
    ↓               ↓                 ↓
Web/API界面    LLM推理引擎     产品数据库 + 实时搜索
```

### 核心组件
1. **基础推荐工具** (`network_product_search.py`) - 静态产品库查询
2. **高级推荐智能体** (`network_product_recommendation_agent.py`) - 智能分析与推荐
3. **配置集成** (`hackathon_config.yml`) - 系统配置和工作流定义

## 🚀 快速开始

### 1. 配置文件更新

配置文件 `configs/hackathon_config.yml` 已包含网络产品推荐工具：

```yaml
functions:
  network_product_recommendation_agent:
    _type: network_product_recommendation_agent
    description: "高级网络产品推荐智能体"
    max_results: 3
    include_real_time_search: true
    include_specifications: true
    tavily_api_key: "" # 可选：配置实时搜索

workflow:
  _type: react_agent
  tool_names:
    - network_product_recommendation_agent
    # ... 其他工具
```

### 2. 运行演示

```bash
# 查看演示效果
python examples/network_agent_demo.py

# 运行功能测试
python test_network_agent.py
```

### 3. 启动服务

```bash
# 启动AIQ Toolkit服务
aiq serve --config_file configs/hackathon_config.yml
```

## 💬 使用示例

### 查询示例

| 用户查询 | 智能体响应 |
|---------|-----------|
| "我需要一个企业级路由器用于分支机构" | 推荐Cisco ISR 4000系列，包含SD-WAN功能和安全特性 |
| "小公司需要支持PoE的交换机" | 推荐Netgear ProSAFE等PoE交换机，适合IP摄像头部署 |
| "推荐防火墙，支持VPN功能" | 推荐Palo Alto PA系列，包含VPN和威胁防护 |
| "为50人办公室设计网络方案" | 提供路由器+交换机+防火墙完整方案 |

### 响应格式

```markdown
# 🌐 Network Product Recommendation Agent

**Query Analysis:** [查询分析结果]
**Detected Categories:** Router
**Business Size:** Enterprise

## 🔗 Router Recommendations

### 1. Cisco ISR 4431
**Type:** Enterprise Branch Router
**Price Range:** $3,500-5,000
**Best For:** Medium to large enterprise branch offices

**Key Highlights:**
• SD-WAN ready with Cisco DNA
• Integrated security and analytics
• Modular design for future expansion

**Specifications:** 2.5 Gbps throughput, 3 WAN ports

## 📋 Complete Buying Guide
[详细的购买指南和实施建议]
```

## 🔧 实现细节

### 查询理解算法

```python
def analyze_query(query):
    """
    查询分析流程：
    1. 产品类别识别 (router/switch/firewall)
    2. 业务规模判断 (enterprise/small business)
    3. 特殊需求提取 (PoE/VPN/WiFi6等)
    4. 预算和用户数量检测
    """
```

### 推荐引擎

- **静态知识库**: 精选的主流产品信息
- **动态匹配**: 基于需求的智能筛选
- **多维排序**: 性能、价格、适用性综合排序
- **实时增强**: 可选的互联网搜索补充

### 产品数据结构

```python
{
    "name": "Cisco ISR 4431",
    "type": "Enterprise Router", 
    "price_range": "$3500-5000",
    "key_features": [...],
    "specifications": {...},
    "use_case": "Medium to large enterprise branches"
}
```

## 📈 扩展方案

### 短期优化 (1-2个月)
- [ ] 增加更多产品品牌和型号
- [ ] 集成实时价格API
- [ ] 添加产品对比功能
- [ ] 支持多语言查询

### 中期发展 (3-6个月)  
- [ ] 垂直行业专业化 (教育、医疗、制造)
- [ ] 网络拓扑分析和设计
- [ ] 供应商库存集成
- [ ] 自动化配置生成

### 长期愿景 (6-12个月)
- [ ] AI驱动的性能优化建议
- [ ] 预测性维护推荐
- [ ] 智能容量规划
- [ ] 完整网络生命周期管理

## 🎯 最佳实践

### 查询优化建议
1. **具体描述需求**: "支持100用户的企业路由器" vs "路由器"
2. **提及关键特性**: "需要PoE供电" "支持VPN" "WiFi 6"
3. **说明使用场景**: "分支机构" "数据中心" "小办公室"
4. **预算范围**: "预算5000美元以内"

### 实施建议
1. **分阶段部署**: 先核心设备，再外围设备
2. **兼容性验证**: 确保各厂商设备间互操作性
3. **性能测试**: 部署前进行负载和压力测试
4. **培训计划**: 为IT团队提供设备管理培训

## 🔍 故障排除

### 常见问题

**Q: 智能体无法识别我的查询？**
A: 尝试使用更具体的产品术语，如"路由器"、"交换机"、"防火墙"

**Q: 推荐的产品价格过高？**
A: 在查询中明确提及预算，如"预算3000元以内的交换机"

**Q: 需要更详细的技术规格？**
A: 可以针对特定产品进行进一步查询，如"Cisco ISR 4431详细规格"

### 配置检查

```bash
# 检查工具是否正确注册
aiq list functions | grep network

# 验证配置文件语法
aiq validate --config_file configs/hackathon_config.yml

# 查看详细日志
aiq serve --config_file configs/hackathon_config.yml --verbose
```

## 📚 相关资源

### 技术文档
- [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit)
- [AIQ Toolkit官方文档](https://docs.nvidia.com/nemo-agent-toolkit/)
- [React Agent工作流](https://docs.nvidia.com/nemo-agent-toolkit/workflows/react-agent/)

### 网络技术参考
- [Cisco产品文档](https://www.cisco.com/c/en/us/support/index.html)
- [网络设备选型指南](https://www.networkworld.com/category/network-hardware/)
- [企业网络最佳实践](https://www.juniper.net/us/en/solutions/enterprise/)

## 👥 贡献指南

欢迎贡献代码和改进建议！

### 贡献方式
1. Fork项目仓库
2. 创建功能分支
3. 提交代码更改
4. 创建Pull Request

### 开发重点
- 新产品数据添加
- 查询理解算法优化
- 推荐精度提升
- 用户体验改进

## 📄 许可证

本项目基于Apache 2.0许可证开源。

---

**🎉 让网络设备选择变得简单！**

> 通过AI技术降低网络技术门槛，让每个人都能获得专业的网络设备建议。