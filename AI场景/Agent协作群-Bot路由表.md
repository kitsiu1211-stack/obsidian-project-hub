---
tags: [A2A, 路由表, agent协作]
created: 2026-07-22
source: lark-cli im +chat-members-list --chat-id oc_219a613c13292855c2dc4b80e59dfd6e
---

# Agent 协作群 — Bot 路由表

群 ID：`oc_219a613c13292855c2dc4b80e59dfd6e`
群名：早日让鑫杰实现

| 序号 | Bot 名称 | user_id | 角色/用途 |
|------|---------|---------|----------|
| 1 | 浪子（Mark 42） | `ou_9b18941c79156bd08a70431dc5dcf7f9` | Hermes — 我的主 Bot，路由中枢 |
| 2 | 南区 ISV 业务助手 | `ou_abdda0c6cd5e362bca041cb3dbd88f86` | ISV 业务咨询 |
| 3 | 大湾区样板间专项小管家 | `ou_459dac1c298c48d280a3ea3260aac80e` | 样板间案例/材料 |
| 4 | 马斯克 | `ou_ec816541777287f722b0896287c4486a` | 信息/观点助手 |
| 5 | Aime 个人助理 | `ou_b33d3f6e144a9730db025d288c81212c` | 个人日程/数据助手 |
| 6 | TC 交付数字员工 | `ou_c9cd24728752004e848f099d2b448d29` | 交付流程 |
| 7 | 客户 AI 场景登记表 智能体 | `ou_0ef4cd7a1f7ce714d503fa244edf95c0` | AI 场景登记 |
| 8 | TRAE ASSISITANT | `ou_1d0748623c4f90fd2f4a92b6a6734b45` | TRAE 编码助手 |
| 9 | 实习生 - 小帅 | `ou_4bc03452642a3b90fcf70a91aba695ea` | 实习生 Bot |
| 10 | Kimi Code | `ou_75e812630b3c51fc879295c78424898c` | 编码助手 |
| 11 | 企鹅兄弟 | `ou_a7276d80c5abc2abfd8da3140ac94e65` | 娱乐/互动 |

## 路由规则

1. **路由前强制查表**：根据任务类型匹配角色/用途列，找到对应 Bot 的 `user_id`
2. **@ 格式**：必须在消息中使用 `<at user_id="ou_xxx">名称</at>` 格式
3. **发送命令**：`lark-cli im +messages-send --chat-id oc_219a613c13292855c2dc4b80e59dfd6e --as bot --text '...'`
4. **浪子不路由给自己**：路由目标不应包含 ou_9b18941c79156bd08a70431dc5dcf7f9（自己）

## 已知陷阱

- ⚠️ 群内**不存在** "Kimi Agent"——只有 "Kimi Code"
- ⚠️ 部分 Bot 名称相似，路由时必须精确匹配完整名称
- ⚠️ 未列入上表的 Bot ID 均不可用