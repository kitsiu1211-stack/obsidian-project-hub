---
title: "Hermes Agent 协作体系"
status: "active"
priority: "high"
category: "personal"
start_date: "2026-04"
tags: ["Agent", "飞书", "CLI", "多Agent", "自动化"]
summary: "构建以 Hermes 为核心的飞书多 Agent 协作群，实现 Agent-to-Agent 自动任务分派与执行"
---

# Hermes Agent 协作体系

## 核心目标
让多个 AI Agent 在飞书群内协同一一主 Agent（Hermes）自动分派任务给专业 Agent（Kimi Code、TRAE、安全合规等），减少人工切换成本。

## 当前进展
- ✅ 核心 Agent 群已搭建（7+ Agent 在线）
- ✅ 路由规则完善（关键词 → 专业 Agent）
- ✅ Agent-to-Agent 任务分派流程跑通
- 🔄 会议旁听 + 自动跟进方案持续优化
- 🔄 旁听脚本 V6 修复中（会议结束检测）

## 关键节点
| 日期 | 里程碑 |
|------|--------|
| 2026-Q1 | Hermes 主 Agent 上线 |
| 2026-04 | 多 Agent 群搭建 |
| 2026-06 | Agent-to-Agent 任务分派验证通过 |
| 2026-07 | 会议旁听 + 自动方案匹配上线 |

## 开发日志
### 2026-07-28
- 旁听脚本 V6 修复（会议结束检测移植 V3 的 `--page-all` + `user is not in the meeting`）
- lark-cli 更新至 1.0.79

### 2026-07-27
- 群内新增安全合规业务助手 Agent
- SkillHub 知识库检索层优化

## 关联资源
- [[SkillHub 技能仓库]]
- [[飞书商务计算器]]
- [[TRAE Work Specialist]]
