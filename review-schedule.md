---
title: Review Schedule
created: 2026-06-18
updated: 2026-06-22
type: meta
tags: [meta, review]
---

# 艾宾浩斯复习调度表

> 基于艾宾浩斯遗忘曲线（1/4/7/14/30天间隔）
> 24个主题分6批启动，每天4个，6天完成首轮
> Cron job 每天9:00读取此表，推送到期内容

## 用户上下文（思考题适配依据）

| 维度 | 内容 |
|------|------|
| 角色 | 飞书商业化老客户销售（消费电子） |
| 核心目标 | 存量保护 + 增量挖掘 |
| 日常 | 客户回访、CRM 流程、内部资源协调 |
| AI 在用 | Aime（商机/CRM）、马斯克/Aily（客户动态监控） |
| 约束 | 非技术背景，思考题必须映射到销售/客户/组织场景 |

## 调度规则

- **间隔**: 首次复习后第1、4、7、14、30天
- **每天推送**: 所有 `next_review <= today` 的主题
- **复习后**: `interval_index++`，next_review 按下一个间隔更新
- **新内容**: 对话延伸自动更新对应主题的 Timeline，并标记 `next_review = today`

## 批次分布

| 批次 | 开始日期 | 主题 |
|------|----------|------|
| 1 | 2026-06-18 | 🤖 [[主题1-Agentic Coding]] · 🤖 [[主题2-多Agent架构]] · 🤖 [[主题3-Harness工程]] · 📊 [[主题4-训模型式管理]] |
| 2 | 2026-06-19 | 🎯 [[主题5-AI落地框架]] · 🧠 [[主题6-提示词工程]] · 🎯 [[主题7-暗知识壁垒与卡点思维]] · 🤖 [[主题8-PaperClip Skill设计]] |
| 3 | 2026-06-20 | 🤖 [[主题9-AI Native范式]] · 🚀 [[主题10-AI暴露度]] · 🚀 [[主题11-模型选择策略]] · 📊 [[主题12-AI转型与组织]] |
| 4 | 2026-06-21 | 🧠 [[主题13-大模型架构与知识编译范式]] · 📊 [[主题14-张一鸣管理哲学]] · 🎯 [[主题15-Vibe调研法]] · 🎯 [[主题16-消费电子行业报告反驳方法论]] |
| 5 | 2026-06-22 | 🎯 [[主题17-中美AI谈判与普通人机会框架]] · 🧠 [[主题18-目标式Prompt vs 命令式Prompt]] · 📊 [[主题19-Context not Control 的三层同构]] · 🚀 [[主题20-可复制性与涌现概率框架]] |
| 6 | 2026-06-23 | 📊 [[主题21-AI原生组织建设]] · 🤖 [[主题22-Skill 设计方法论]] · 📊 [[主题23-Anthropic组织文化]] · 🚀 [[主题24-Agent时代个人知识图谱构建链路]] |

## 当前状态

```json
[
  {
    "theme": "主题1-Agentic Coding",
    "icon": "🤖",
    "batch": 0,
    "start_date": "2026-06-18",
    "review_count": 2,
    "next_review": "2026-06-29",
    "interval_index": 2,
    "history": [
      {
        "date": "2026-06-18",
        "review_count": 1,
        "next_review": "2026-06-22"
      },
      {
        "date": "2026-06-22",
        "review_count": 2,
        "next_review": "2026-06-29"
      }
    ]
  },
  {
    "theme": "主题2-多Agent架构",
    "icon": "🤖",
    "batch": 0,
    "start_date": "2026-06-18",
    "review_count": 2,
    "next_review": "2026-06-29",
    "interval_index": 2,
    "history": [
      {
        "date": "2026-06-18",
        "review_count": 1,
        "next_review": "2026-06-22"
      },
      {
        "date": "2026-06-22",
        "review_count": 2,
        "next_review": "2026-06-29"
      }
    ]
  },
  {
    "theme": "主题3-Harness工程",
    "icon": "🤖",
    "batch": 0,
    "start_date": "2026-06-18",
    "review_count": 2,
    "next_review": "2026-06-29",
    "interval_index": 2,
    "history": [
      {
        "date": "2026-06-18",
        "review_count": 1,
        "next_review": "2026-06-22"
      },
      {
        "date": "2026-06-22",
        "review_count": 2,
        "next_review": "2026-06-29"
      }
    ]
  },
  {
    "theme": "主题4-训模型式管理",
    "icon": "📊",
    "batch": 0,
    "start_date": "2026-06-18",
    "review_count": 2,
    "next_review": "2026-06-29",
    "interval_index": 2,
    "history": [
      {
        "date": "2026-06-18",
        "review_count": 1,
        "next_review": "2026-06-22"
      },
      {
        "date": "2026-06-22",
        "review_count": 2,
        "next_review": "2026-06-29"
      }
    ]
  },
  {
    "theme": "主题5-AI落地框架",
    "icon": "🎯",
    "batch": 1,
    "start_date": "2026-06-19",
    "review_count": 1,
    "next_review": "2026-06-23",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-19",
        "review_count": 1,
        "next_review": "2026-06-23"
      }
    ]
  },
  {
    "theme": "主题6-提示词工程",
    "icon": "🧠",
    "batch": 1,
    "start_date": "2026-06-19",
    "review_count": 1,
    "next_review": "2026-06-23",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-19",
        "review_count": 1,
        "next_review": "2026-06-23"
      }
    ]
  },
  {
    "theme": "主题7-暗知识壁垒与卡点思维",
    "icon": "🎯",
    "batch": 1,
    "start_date": "2026-06-19",
    "review_count": 2,
    "next_review": "2026-07-15",
    "interval_index": 2,
    "history": [
      {
        "date": "2026-06-19",
        "review_count": 1,
        "next_review": "2026-06-23"
      },
      {
        "date": "2026-07-11",
        "review_count": 2,
        "next_review": "2026-07-15"
      }
    ]
  },
  {
    "theme": "主题8-PaperClip Skill设计",
    "icon": "🤖",
    "batch": 1,
    "start_date": "2026-06-19",
    "review_count": 1,
    "next_review": "2026-06-23",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-19",
        "review_count": 1,
        "next_review": "2026-06-23"
      }
    ]
  },
  {
    "theme": "主题9-AI Native范式",
    "icon": "🤖",
    "batch": 2,
    "start_date": "2026-06-20",
    "review_count": 2,
    "next_review": "2026-06-28",
    "interval_index": 2,
    "history": [
      {
        "date": "2026-06-20",
        "review_count": 1,
        "next_review": "2026-06-21"
      },
      {
        "date": "2026-06-21",
        "review_count": 2,
        "next_review": "2026-06-28"
      }
    ]
  },
  {
    "theme": "主题10-AI暴露度",
    "icon": "🚀",
    "batch": 2,
    "start_date": "2026-06-20",
    "review_count": 2,
    "next_review": "2026-06-28",
    "interval_index": 2,
    "history": [
      {
        "date": "2026-06-20",
        "review_count": 1,
        "next_review": "2026-06-21"
      },
      {
        "date": "2026-06-21",
        "review_count": 2,
        "next_review": "2026-06-28"
      }
    ]
  },
  {
    "theme": "主题11-模型选择策略",
    "icon": "🚀",
    "batch": 2,
    "start_date": "2026-06-20",
    "review_count": 2,
    "next_review": "2026-06-28",
    "interval_index": 2,
    "history": [
      {
        "date": "2026-06-20",
        "review_count": 1,
        "next_review": "2026-06-21"
      },
      {
        "date": "2026-06-21",
        "review_count": 2,
        "next_review": "2026-06-28"
      }
    ]
  },
  {
    "theme": "主题12-AI转型与组织",
    "icon": "📊",
    "batch": 2,
    "start_date": "2026-06-20",
    "review_count": 2,
    "next_review": "2026-06-28",
    "interval_index": 2,
    "history": [
      {
        "date": "2026-06-20",
        "review_count": 1,
        "next_review": "2026-06-21"
      },
      {
        "date": "2026-06-21",
        "review_count": 2,
        "next_review": "2026-06-28"
      }
    ]
  },
  {
    "theme": "主题13-大模型架构与知识编译范式",
    "icon": "🧠",
    "batch": 3,
    "start_date": "2026-06-21",
    "review_count": 1,
    "next_review": "2026-06-25",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-21",
        "review_count": 1,
        "next_review": "2026-06-25"
      }
    ]
  },
  {
    "theme": "主题14-张一鸣管理哲学",
    "icon": "📊",
    "batch": 3,
    "start_date": "2026-06-21",
    "review_count": 1,
    "next_review": "2026-06-25",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-21",
        "review_count": 1,
        "next_review": "2026-06-25"
      }
    ]
  },
  {
    "theme": "主题15-Vibe调研法",
    "icon": "🎯",
    "batch": 3,
    "start_date": "2026-06-21",
    "review_count": 1,
    "next_review": "2026-06-25",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-21",
        "review_count": 1,
        "next_review": "2026-06-25"
      }
    ]
  },
  {
    "theme": "主题16-消费电子行业报告反驳方法论",
    "icon": "🎯",
    "batch": 3,
    "start_date": "2026-06-21",
    "review_count": 2,
    "next_review": "2026-07-07",
    "interval_index": 3,
    "history": [
      {
        "date": "2026-06-21",
        "review_count": 1,
        "next_review": "2026-06-25"
      },
      {
        "date": "2026-06-25",
        "review_count": 2,
        "next_review": "2026-06-29"
      },
      {
        "date": "2026-07-02",
        "review_count": 3,
        "next_review": "2026-07-07"
      }
    ]
  },
  {
    "theme": "主题17-中美AI谈判与普通人机会框架",
    "icon": "🎯",
    "batch": 4,
    "start_date": "2026-06-22",
    "review_count": 2,
    "next_review": "2026-07-17",
    "interval_index": 3,
    "history": [
      {
        "date": "2026-06-22",
        "review_count": 1,
        "next_review": "2026-06-26"
      },
      {
        "date": "2026-07-03",
        "review_count": 2,
        "next_review": "2026-07-17"
      }
    ]
  },
  {
    "theme": "主题18-目标式Prompt vs 命令式Prompt",
    "icon": "🧠",
    "batch": 4,
    "start_date": "2026-06-22",
    "review_count": 1,
    "next_review": "2026-06-26",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-22",
        "review_count": 1,
        "next_review": "2026-06-26"
      }
    ]
  },
  {
    "theme": "主题19-Context not Control 的三层同构",
    "icon": "📊",
    "batch": 4,
    "start_date": "2026-06-22",
    "review_count": 1,
    "next_review": "2026-06-26",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-22",
        "review_count": 1,
        "next_review": "2026-06-26"
      }
    ]
  },
  {
    "theme": "主题20-可复制性与涌现概率框架",
    "icon": "🚀",
    "batch": 4,
    "start_date": "2026-06-22",
    "review_count": 1,
    "next_review": "2026-06-26",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-22",
        "review_count": 1,
        "next_review": "2026-06-26"
      }
    ]
  },
  {
    "theme": "主题21-AI原生组织建设",
    "icon": "📊",
    "batch": 5,
    "start_date": "2026-06-23",
    "review_count": 1,
    "next_review": "2026-06-25",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-24",
        "review_count": 1,
        "next_review": "2026-06-25"
      }
    ]
  },
  {
    "theme": "主题22-Skill 设计方法论",
    "icon": "🤖",
    "batch": 5,
    "start_date": "2026-06-23",
    "review_count": 0,
    "next_review": "2026-06-23",
    "interval_index": 0,
    "history": []
  },
  {
    "theme": "主题23-Anthropic组织文化",
    "icon": "📊",
    "batch": 5,
    "start_date": "2026-06-23",
    "review_count": 1,
    "next_review": "2026-06-27",
    "interval_index": 1,
    "history": [
      {
        "date": "2026-06-23",
        "review_count": 1,
        "next_review": "2026-06-27"
      }
    ]
  },
  {
    "theme": "主题24-Agent时代个人知识图谱构建链路",
    "icon": "🚀",
    "batch": 5,
    "start_date": "2026-06-23",
    "review_count": 0,
    "next_review": "2026-06-23",
    "interval_index": 0,
    "history": []
  }
]
```