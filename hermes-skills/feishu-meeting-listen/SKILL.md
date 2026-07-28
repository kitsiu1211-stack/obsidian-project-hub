---
name: feishu-meeting-listen
description: Auto-detect and silently join all Feishu meetings as an observer — capture real-time transcripts to JSONL, generate structured summaries, and for customer meetings additionally push C360 enrichment (opportunity + follow-up). The agent appears invisible to other participants. Published to GitHub for team sharing.
category: feishu
---

# 飞书会议旁听（智能体入会）

## 触发条件

- 用户说「监听会议」「加入会议」「听一下会议」「会议旁听」
- 用户分享会议链接或会议号
- 用户要求获取会议字幕/内容/纪要
- 🆕 **自动触发**：v6 cron 守护已在运行，用户入会即自动旁听，无需手动触发

## 核心需求（用户 2026-07-16 明确）

> **所有会议都要监听并产出纪要**——内部会议、外部会议、客户会议，一个不落。
> C360 客户情报只在客户会议（标题含「客户名 x 飞书」）时附加推送，不作为唯一功能。

| 需求 | 实现 |
|---|---|
| 入会自动监听（所有会议） | ✅ v6 `meeting_detect.py` → `poll.sh` |
| 客户会议推 C360（商机+跟进） | ✅ 会议大脑 cron (`f64f153f96ec`) 每 3 分钟 |
| 会议结束后产出纪要 | ✅ 会议大脑 cron → 读 JSONL → 飞书卡片 |
| 会后自动执行（找 agents） | ✅ Step 7 赛后执行：AUTO 立刻干 / DRAFT 备好 / USER 标注 |
| 非客户会议不推 C360 | ✅ 仅监听+纪要，不推情报 |

## ⛔ bash 轮询方案已废弃（2026-07-16） → 迁移至 Python no_agent cron

**poll-v5.sh + launchd 守护经过 5 版迭代，从未稳定运行。后续尝试 LLM cron 也因 token 消耗过高被否决。**

用户原话：「每次都说修复好，自从迭代后没有一次成功的」「用 Cron 任务去挂载的话 token 消耗也太高了」。

**🚨 教训：v5 迁移大失败（2026-07-16）**：从 bash poll.sh 迁移到 Python `meeting_detect.py` 时，**只保留了 C360 推送能力，彻底丢失了 poll.sh 入会监听和会议纪要产出能力**。用户：「自从脚本更新到 V5 之后，好像都没有产出会议纪要了。就是这整个升级版本简直就是个大失败。」

**教训**：任何架构迁移必须保留核心能力清单对照。核心能力 = 监听（poll.sh）+ 纪要（LLM 分析 JSONL）+ C360（客户会议附加）。迁移时丢掉任何一项就是回归。

---

### v6 终局架构（2026-07-16）：全会议监听 + 客户会议 C360 附加

**cron 配置**：job `272cdc68a518`，`schedule: every 1m`，`script: meeting_detect.py`，`no_agent: true`。

**脚本位置**：`~/.hermes/scripts/meeting_detect.py`（v6）

**v6 核心逻辑**：

| 会议类型 | 动作 |
|---|---|
| **任何会议入会** | 自动启动 `poll.sh` 后台监听，每 10s 轮询字幕写入 JSONL |
| **poll.sh 退出** | 标记 `completed`，JSONL 中包含完整字幕/聊天/进出事件 |
| **客户会议（标题匹配「客户名 x 飞书」）** | 在监听基础上，额外调 C360 推商机信息到 stdout（cron 递送） |
| **非客户会议** | 仅监听，不推送 |

**与旧方案对比**：

| | bash poll-v5 | LLM cron | v5 Python no_agent | **v6 Python no_agent ✅** |
|---|---|---|---|---|
| 守护 | launchd | 调度器 | 调度器 | 调度器 |
| 超时 | 循环卡死 | 单次失败 | subprocess timeout=15s | subprocess timeout=15s |
| Token | 零 | 巨额 | **零** | **零** |
| 状态 | 无 | meeting_state.json | meeting_state.json | meeting_state.json + PID 追踪 |
| 监听所有会议 | ✅ (poll.sh) | ❌ | ❌ | ✅ (poll.sh 自动启动) |
| C360 推送 | ✅ | ✅ | ✅ | ✅（客户会议附加） |
| 纪要产出 | ❌ (依赖 Agent) | ❌ | ❌ | ✅ (LLM cron `f64f153f96ec`) |
| 会后执行 | ❌ | ❌ | ❌ | ✅ (Step 7 AUTO/DRAFT/USER) |

**状态字段**：`new` → `monitoring` → `completed`（poll.sh 退出后自动标记）。`pid` 字段追踪 poll.sh 进程存活。

**旧 poll-v5.sh / launchd / LLM cron 已全部停用。**

---

### v6 终局架构：双轨 cron（2026-07-16）

```
你入会
  │
  ▼
🔄 会议检测 (272cdc68a518, 每 1 分钟, 零 token)
  │  meeting_detect.py
  │  ├─ lark-cli vc +meeting-list-active → 活跃会议
  │  ├─ 标记 client/non-client（标题匹配）
  │  ├─ 启动 poll.sh 后台监听 → ~/meeting_logs/<id>.jsonl
  │  ├─ 追踪 PID → 检测退出 → 标记 completed
  │  └─ 状态持久化 → meeting_state.json
  │
  ▼
🧠 会议大脑 (f64f153f96ec, 每 3 分钟, LLM)
  │  skill: feishu-meeting-listen
  │
  ├─ 客户会议入会 (status=new, client≠null)
  │   ✅ lark-c360 search all → 在途商机
  │   🆕 lark-c360 follow_up +recent → 最近跟进
  │   → 飞书卡片推送 → 标记 c360_sent
  │
  ├─ 会议结束 (status=completed, !summarized)
  │   → 读 ~/meeting_logs/<id>.jsonl
  │   → 提取去重字幕 → 类型识别 → 框架匹配
  │   → 飞书卡片纪要
  │   → Step 7 会后自动执行 (AUTO/DRAFT/USER)
  │   → 标记 summarized
  │
  └─ 无事 → 静默退出
```

| 层 | 脚本 | Cron ID | 频率 | Token | 职责 |
|---|---|---|---|---|---|
| 检测层 | `meeting_detect.py` | `272cdc68a518` | 每 1 分钟 | **零** | 入会检测 + poll.sh 启动 + 状态管理 |
| 智能层 | LLM prompt | `f64f153f96ec` | 每 3 分钟 | ~¥1/天 | C360 推送 + 纪要生成 + 会后执行 |

> ⚠️ **纪要生成缺失**：v6 当前状态——poll.sh 产出 JSONL → `meeting_detect.py` 标记 `completed`，但缺少 LLM cron 从 JSONL 生成纪要。需单独创建摘要 cron（建议每 5 分钟检查，成本 ~¥0.05/次）。

> 📦 **公开发布**：[GitHub repo](https://github.com/kitsiu1211-stack/hermes-feishu-meeting-listen) — Agent 无关，任何 Agent（Hermes / Claude Code / Codex / Workbuddy）均可通过 `git clone && bash install.sh` 安装。含 `setup.sh` 自动安装 C360 CLI、`install.sh` 一键部署。发布流程见 `references/skill-publishing.md`。

| 能力 | 说明 |
|---|---|---|
| **全会议自动监听 ✅** | v6 核心：任何会议入会 → 自动启动 `poll.sh` 后台轮询字幕/聊天/进出事件 → 写入 `~/meeting_logs/<id>.jsonl`。零 token 消耗。 |
| **会议纪要产出 ⚠️** | poll.sh 退出后 → JSONL 中已有完整字幕 → 需 LLM 分析生成飞书卡片纪要。当前缺失：待创建摘要 cron job。 |
| **C360 客户情报（附加）** | 仅客户会议（标题匹配「客户名 x 飞书」）：`lark-c360 search all` 查商机产品 SKU + ARR + 阶段 → `follow_up +recent --account-id` 查最近跟进。**仅推送用户在会议中不知道的信息**（商机细节+跟进摘要），不推已知的行业/CSM/付费状态。发送一次后继续旁听。 |
| **🎙️ 实时音频 ASR** | 🆕 DashScope Paraformer-v2 实时语音识别 + Qwen-Plus 分析。BlackHole 采集系统音频 → WebSocket 推流 → 实时转写。详见 `references/dashscope-realtime-asr.md` |

## 🚨 会议总结格式铁律

**所有会议总结必须用飞书卡片输出，禁止纯文本。** 如果内容超出单张卡片长度，自动拆分为多张卡片发送。

```bash
# 飞书卡片 JSON 模板（lark-cli 发送）
lark-cli im +messages-send \
  --chat-id "<chat_id>" \
  --msg-type interactive \
  --as bot \
  --content '{
    "config": {"wide_screen_mode": true},
    "header": {
      "title": {"tag": "plain_text", "content": "📹 会议标题"},
      "template": "blue"
    },
    "elements": [
      {"tag": "div", "text": {"tag": "lark_md", "content": "**参会信息 / 时长**"}},
      {"tag": "hr"},
      {"tag": "div", "text": {"tag": "lark_md", "content": "正文（支持 markdown 表格/列表）"}},
      {"tag": "hr"},
      {"tag": "note", "elements": [{"tag": "plain_text", "content": "卡片 N/M"}]}
    ]
  }'
```

**分片规则**：
- 每张卡片 `elements` 数组不超过 10 个元素（含 `hr` 分隔线）
- 逻辑分段：第一张 = 会议概览 + 核心结论，后续 = 详细内容
- 每张末尾加 `note` 标注 "卡片 N/M"
- 按顺序依次发送（`for card in card1 card2 card3`）

### v5 脚本

```bash
# 自动检测模式（推荐）：无需参数，后台自动扫描
bash poll-v5.sh

# 手动模式（兼容 v3）：指定会议 ID
bash poll-v5.sh <meeting_id> [title]
```

### 告警发送目标

告警通过飞书 IM 发送到 `ALERT_CHAT` 环境变量指定的群或用户。不包含 Agent 协作群联动（纯会议场景 + C360）。

客户名单见 `~/.hermes/data/client_list.json`（可独立更新，自动同步）。

C360 字段速查见 `references/c360-fields.md` —— 含已验证的 field name、`search all` 返回结构、已知限制（多产品线 CSM 仅 `csm_owner`、商机类型未暴露、ISV 商机不可读）。

## 告警输出原则

> **只输出用户不知道的信息。** 会议中用户已知的基础信息（行业、CSM 姓名、客户类型、付费状态）一律不输出。告警聚焦于：
> 1. 商机产品 + 阶段（用户未必记得每个客户的最新商机细节）
> 2. 最近跟进笔记摘要（用户可能忘了上次聊了什么）
>
> 关键词告警照常（预算/价格/签约等），这些是实时提醒，不涉及已知信息。

---

## 核心原理

Agent 以**用户身份**旁听会议，通过飞书 VC API 轮询拉取会中事件（字幕、聊天、参会人进出），分析后通过飞书 IM 发给用户。**其他参会者感知不到 Agent 的存在**。

```
用户本人在飞书会议中
    ↓
Agent 调用 GetUserActiveMeeting → 拿到 meeting_id
    ↓
Agent 调用 ListMeetingEvents 轮询拉取事件（字幕、聊天等）
    ↓
Agent 分析内容，通过飞书 IM 将结果发给用户
```

## 能力边界

- ✅ 实时获取字幕（transcript）
- ✅ 实时获取会中聊天（chat）
- ✅ 参会人进出通知
- ✅ 多会议并行旁听（无硬上限，每会一个独立 bash 进程）
- ❌ 实时推送（需轮询拉取，无 webhook）
- ❌ 在会上发声（纯旁听，不说话）

### 成本效率

v3 脚本的核心设计：**轮询归轮询，分析归分析，互不污染**。

- 后台轮询脚本是独立 bash 进程，**零 token 消耗**
- 仅在提取字幕 + 生成总结时才消费 LLM
- 实测：两场 1 小时会议 ≈ 34K tokens ≈ **¥0.09**（DeepSeek V4 Pro 定价）
- 每小时会议成本 ≈ ¥0.05，远低于飞书妙记企业版 ¥75/人/月

### 适合场景

会议纪要、议程追踪、实时问答助手、背后支援型 Agent

### 🆕 Python no_agent Cron 自动守护（v6 终局架构，2026-07-16）

**v6 双轨机制**：`meeting_detect.py`（no_agent，每 1 分钟）自动启动 `poll.sh` 监听所有会议 + 客户会议额外推 C360。

```bash
# 无需手动操作。cron job 272cdc68a518 已在运行。
# 脚本位置：~/.hermes/scripts/meeting_detect.py
# poll.sh 位置：~/.hermes/skills/feishu/feishu-meeting-listen/scripts/poll.sh
# 验证监听状态：
cat ~/.hermes/cron/meeting_state.json | python3 -m json.tool
# 检查字幕日志：
ls -la ~/meeting_logs/
```

**v6 工作流**：

```
meeting_detect.py (cron, every 1min, no_agent)
  ├─ lark-cli vc +meeting-list-active → 获取活跃会议列表
  ├─ 新会议（所有类型）→ subprocess.Popen(poll.sh) 后台监听
  │   └─ poll.sh → 每 10s 轮询 meeting-events → 写入 ~/meeting_logs/<id>.jsonl
  ├─ 客户会议（标题匹配）→ 额外调 C360 → print 到 stdout（cron 递送）
  ├─ 检测 poll.sh 退出 → 标记 completed → log_size 记录
  └─ 状态持久化到 meeting_state.json（含 PID 追踪）
```

| 状态 | 含义 |
|------|------|
| `new` | 首次检测到，尚未启动 poll.sh |
| `monitoring` | poll.sh 正在后台轮询 |
| `completed` | poll.sh 已退出，JSONL 可读 |

**⚠️ 待完成**：纪要生成——需额外 LLM cron 读取 `completed` 状态的 meeting → 分析 JSONL → 生成飞书卡片纪要。当前 `completed` 状态仅记录，未自动生成纪要。详见 `references/cron-python-migration.md`。

### 会议类型识别 → 分析框架匹配

根据会议标题和内容，自动匹配对应的分析框架：

| 会议类型 | 标题特征 | 使用框架 | 输出重点 |
|---------|---------|---------|---------|
| **客户交接** | 「交接」「新客转老客」 | `client-handover-checklist` skill | 七维度 + 三盲区，结构化表格 |
| **客户交流** | 「x飞书」「交流」「沟通」 | JTBD / BANT / Kano / Mom Test | 客户需求矩阵 + 产品匹配度 + 销售建议 |
| **安全/产品演示** | 「安全」「功能介绍」「方案」 | 功能逐条对应 + 能力边界标注 | 已支持 vs 不支持 vs 需升级，报价路径 |
| **内部对齐** | 「目标对齐」「指标」「专项」「讨论」 | 决策点提取 + 行动项 | 拍定了什么、没拍定什么、你的待办 |
| **围炉夜话/分享** | 「围炉」「分享」「研修」 | 知识提取 | 核心观点 + 启发点，不需要行动项 |

**使用原则**：先看标题判断类型，再套框架。不要让框架驱动内容——让数据选出最合适的框架。

---

## 前提条件（一次性准备）

### ① 灰度资格

进入早鸟体验群获取灰度资格。

### ② 飞书应用 & 权限

1. 在飞书开放平台创建企业自建应用，获取 App ID / App Secret
2. 申请权限：`vc:meeting.meetingevent:read`（用户身份权限）
3. 数据权限范围选「按条件筛选」→ 会议的归属者 → 包含 → 与应用可用范围一致
4. 权限变更后重新发布应用

### ③ 客户端版本 & CLI 工具

- 飞书客户端 ≥ 7.68（飞书 → 头像 → 关于飞书 → 检查更新）
- lark-cli ≥ v1.0.55：`npm install -g @larksuite/cli@latest`
- **lark-c360**（C360 商机查询）：
  ```bash
  npm install -g https://lf-ldic360.feishucdn.com/obj/ldi-c360/cli/lark-c360/latest/customer360-lark-c360.tgz
  lark-c360 install-skills --force
  lark-c360 env use online
  lark-c360 auth login --no-wait --json   # 打开返回的 authorize_url 授权
  lark-c360 auth login --resume           # 授权后执行
  ```

> 也可运行 `bash scripts/setup.sh` 一键检查并安装上述工具。

### ④ 会议侧设置

每场会议的 owner 在会议安全设置里开启「**允许智能体入会**」。
（找不到该选项，先开 AI 总结。只有在灰度范围内才能打开。）

---

## 用户授权（首次使用）

Agent 独立使用时需要用户先授权 `vc:meeting.meetingevent:read` 权限。

### 第一阶段：生成授权链接

```bash
lark-cli auth login --scope "vc:meeting.meetingevent:read" --no-wait --json
```

从输出提取 `verification_url` 和 `device_code`，把 `verification_url` 发给用户点击完成授权。

### 第二阶段：用户授权后获取 token

```bash
lark-cli auth login --device-code <device_code_from_step1>
```

---

## 核心命令

### 查询用户当前所在会议

```bash
lark-cli vc +meeting-list-active --as user
```

**返回**：会议列表，每项含：
- `meeting_id` — 长会议 ID（用于拉事件，**不是 9 位会议号**）
- `meeting_no` — 9 位会议号（给用户看的）
- `meeting_title` — 会议标题

如果用户在多个会议中，列出所有会议让用户选择。

### 拉取会中事件（字幕、聊天等）

```bash
lark-cli vc +meeting-events --as user --meeting-id <meeting_id> --page-all --page-size 100
```

**参数说明**：

| 参数 | 说明 |
|------|------|
| `--meeting-id` | 长会议 ID（来自 GetUserActiveMeeting，非 9 位会议号） |
| `--page-all` | 自动翻页获取所有事件 |
| `--page-size` | 单页条数（20-100） |
| `--start` / `--end` | 时间范围（ISO 8601 / YYYY-MM-DD / Unix 秒），可选 |

### 脚本架构（v3，已验证稳定）

**v1** 直接 `--page-all` → 日志爆炸（每 10 秒全量追加重复数据）。
**v2** 引入 `page_token` 增量拉取 → token 约 40 分钟过期后死循环丢数据。
**v3** 彻底砍掉 `page_token`，永远用 `--page-all` 全量拉，靠 Python 从日志文件读取已有 `sentence_id` 做内存 `set()` 去重，只追加真正新的事件。

核心优势：
- 无 token 过期风险——page_token 这个不稳定因素从架构上消除了
- Python `set()` 去重——不依赖 bash 变量拼接，大会议（1600+ 句）也可靠
- 独立 bash 进程——**轮询零 token 消耗**，不进 LLM 上下文
- 成本实测：两场 1 小时会议 ≈ 34K tokens ≈ ¥0.09（仅提取字幕 + 生成总结时消费 LLM）

**多会议支持**：无硬上限。每个会议一个独立 `bash poll.sh` 进程，10 秒一次 API 调用的开销可忽略。实际瓶颈是用户能同时挂几个飞书会议（常态两场，偶尔三场）。

---

## 事件数据结构

按 `activity_event_type` 区分事件类型。

### 字幕 `transcript_received_items`

```json
{
  "speaker": { "id": "xxx", "user_type": 1, "user_name": "张三" },
  "text": "今天来讨论一下这个方案",
  "language": "zh-CN",
  "start_time_ms": "1716699012000",
  "end_time_ms": "1716699014000",
  "sentence_id": "100001"
}
```

- `user_type` 可能为声纹检测类型（100/101/102），需兼容处理
- 同一句话可能多次推送（修正/补全），用 `sentence_id` 去重

### 聊天消息 `chat_received_items`

```json
{
  "operator": { "id": "xxx", "user_name": "张三" },
  "message_id": "om_xxx",
  "message_type": 1,
  "content": "大家好",
  "send_time": "1716699030000"
}
```

`message_type`：1=文本，2=系统，3=表情，4=加密

### 参会人进入 `participant_joined_items`

```json
{
  "participant": { "id": "xxx", "user_type": 1, "user_role": 1, "user_name": "张三" },
  "join_time": "1716699010000"
}
```

### 参会人离开 `participant_left_items`

```json
{
  "participant": { "id": "xxx", "user_name": "张三" },
  "leave_reason": 1,
  "leave_time": "1716700000000"
}
```

`leave_reason`：1=主动离会，2=会议结束，3=被踢出

---

## 实战工作流

### Step 1: 检查用户在会

```bash
lark-cli vc +meeting-list-active --as user
```

如果返回空 → 告知用户「你当前不在任何会议中」。如果在多个会议中 → 列出让用户选。

### Step 2: 第一次拉事件（获取当前状态）

```bash
lark-cli vc +meeting-events --as user --meeting-id <meeting_id> --page-all --page-size 100 --format json
```

解析返回的 events，按类型分类：
- 字幕 → 按 speaker 和 sentence_id 聚合为对话流
- 聊天 → 按时间排序展示
- 进出 → 统计当前参会人列表

### Step 3: 处理并交付分析

将字幕流构建为可读的对话/摘要，通过飞书 IM 发给用户。首次交付包含：
- 会议基本信息（标题、当前参会人）
- 已有对话摘要
- 会中聊天记录

### Step 4: 启动后台轮询（持久化脚本）

使用 skill 内置的 `scripts/poll.sh`，自动将字幕写入 `~/meeting_logs/<meeting_id>.jsonl`。

```bash
# ⚠️ 必须用 bash 前缀运行（首次部署需 chmod +x，避免 Permission denied）
chmod +x ~/.hermes/skills/feishu/feishu-meeting-listen/scripts/poll.sh
bash ~/.hermes/skills/feishu/feishu-meeting-listen/scripts/poll.sh <meeting_id> <meeting_title> &
```

**脚本特性（v3）：**
- **全量拉取 + 内存去重**：永远用 `--page-all`，Python 从日志文件读已有 `sentence_id` 做 `set()` 去重，不依赖 page_token
- 每 10 秒拉一次字幕/聊天/进出事件，去重后追加写入 JSONL
- 检测到「user is not in the meeting」自动退出
- 所有路径使用绝对路径，不依赖 session 上下文
- 输出位置：`~/meeting_logs/<meeting_id>.jsonl`

**JSONL 格式（每行一条）：**
```json
{"type": "transcript", "speaker": "蔡璐", "text": "今天主要是交接", "sentence_id": "100001", "time": "1716699012000"}
{"type": "chat", "speaker": "张三", "text": "收到", "message_id": "om_xxx"}
{"type": "join", "speaker": "李四", "text": "入会", "time": "1716699010000"}
{"type": "leave", "speaker": "李四", "text": "主动离会", "time": "1716700000000"}
{"type": "meta", "event": "meeting_ended", "time": "14:32:05"}
```

**启动后告知用户：** 通知用户脚本已启动 + 日志路径。

**🚨 铁律：启动 poll.sh 后绝不可放任不管。这是用户最恼火的模式。**

1. `terminal(background=true, notify_on_complete=true)` 启动，返回的 `session_id` 必须保存
2. 收到 `notify_on_complete` 通知后，**立刻走 Step 4.5 → Step 5 → Step 7**，不得延迟
3. **做其他任务时也不能忘记会议旁听进程**——跟 TRAE 交互、读文章、查资料时，如果 notify 到了，必须立刻切换回来处理会议纪要
4. 如果用户说「会议结束了你没监听到」，立刻检查 `~/meeting_logs/` 中最新修改的 JSONL，看是否有漏掉的会议内容可以补救

**❌ 已发生事故**：
- 7.10 高驰×分贝通 + 7.11 卿志聊 AI：脚本退出后 Agent 未主动检测
- **7.14 南区RM周会后第二场会议**：Agent 在跟 TRAE 交互/读文章时收到 notify 但未及时处理，导致漏听。此后加入铁律——notify 到达时，**无论正在做什么，立刻切换处理会议纪要**

**终止条件**（脚本自动处理）：
- 用户离会（`user is not in the meeting`）→ 自动退出
- 会议结束（`leave_reason=2`）→ 自动退出

### Step 4.5: 检测脚本退出 → 恢复字幕

```bash
# 从日志文件读取全部字幕
cat ~/meeting_logs/<meeting_id>.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line.strip())
    t = d.get('type','')
    if t == 'transcript':
        print(f'[{d[\"speaker\"]}]: {d[\"text\"]}')
    elif t == 'chat':
        print(f'[聊天-{d[\"speaker\"]}]: {d[\"text\"]}')
    elif t in ('join','leave'):
        print(f'[{d[\"speaker\"]} {d[\"text\"]}]')
"
```

### Step 5: 会议结束后输出纪要

当检测到用户离会或会议结束，生成完整会议纪要。

**输出步骤**：
1. Python 提取唯一字幕（sentence_id 去重）
2. 根据会议标题判断类型（交接/交流/演示/对齐/分享）
3. 套用对应分析框架（见上方「会议类型识别 → 分析框架匹配」表）
4. 输出结构化纪要 + 用户待办

**分析框架速查**：

| 框架 | 适用场景 | 分析维度 |
|------|---------|---------|
| **七维度交接** | 客户交接会 | 金额/决策人/签约原因/决策过程/商机/风险/线下交接 + 服务断点/前任潜规则/组织变动三盲区 |
| **JTBD** | 客户交流 | 功能性/情感性/社会性三层需求 |
| **BANT** | 客户交流 | 预算/决策权/需求/时间线 → 成交优先级 |
| **Kano** | 产品演示后 | 基本型/期望型/兴奋型/反向需求 → 产品匹配度 |
| **Mom Test** | 客户交流 | 真痛点 vs 客套话 → 高/低信号标注 |
| **决策点提取** | 内部对齐 | 拍定了什么 + 没拍定什么 + 你的待办 |

**原则**：数据优先，框架适配在后。不要让框架驱动内容。

### Step 5.5: 需求 Grilling（自动触发）

当会议中出现模糊的客户需求（如"想做 AI 会议管理"、"想用 AI 提效"）时，不要直接输出一个含糊的总结。**自动启动 Grill 模式**：

**三个铁规则**：
1. **一次只问一个开放式问题** — 不用 clarify 的多选，让用户自由回答
2. **只问 Decisions，Facts 自己查** — 客户规模、行业、已用产品这些我通过 C360/公开信息/会议上下文自己补，不问
3. **问完等确认再动手** — 用户说"可以了"或需求边界清晰之后，再生成 spec / 录入多维表格

**Grill 方向**（根据需求类型自动选择切入角度）：
- 使用场景 → 谁用？触发条件是什么？输入输出是什么？
- 技术边界 → 必须用飞书原生？能接外部 API 吗？
- 规模 → 多少人用？每天多少次？峰值多少？
- 约束 → 预算上限？时间要求？合规/安全要求？
- 已有底座 → 客户现在用什么？哪些不能动？

**停止条件**：用户说「可以了」「差不多了」「先这样」或连续两轮追问已达到足够的边界清晰度。

### Step 6: 会后跟进（材料获取 + 情报补齐）

**6a. 材料获取**：会议中用户提到需要材料（ISV 产品、飞书案例、版本对比等）→ 会后去 Agent 协作群 @对应 Bot 获取。

**详见 `agent-group-collab` skill**——覆盖 Aime（业绩查询）、ISV 助手（产品材料）、样板间小管家（案例弹药库）、马斯克（客户名单）的完整交互流程 + 材料筛选规则（禁止搬运工，必须精选 1-3 条最匹配的交付）。

**6b. 客户交接情报补齐**：如果会议标题/内容含「交接」「新客转老客」「handover」关键词 → **自动触发 `post-handover-intelligence` skill**：

```
poll.sh 退出检测到会议类型=客户交接
    ↓
自动调用 post-handover-intelligence 五阶段流水线：
  Phase 1：从会议字幕提取客户名、KDM、待办
  Phase 2：C360 CLI 查帐号/订单/跟进记录
  Phase 3：公开搜索竞品对比、行业动态
  Phase 4：交叉验证 C360 vs 公开信息 vs 已有笔记
  Phase 5：飞书卡片交付 + Obsidian 客户笔记更新
```

**这个链路全自动。poll.sh 退出 = 触发。不需要用户说任何话。**

### Step 7: 会后待办自动执行（Universal Post-Meeting Action Executor）🚨

> **核心理念**：会议产生的待办，不是「用户看完了自己去干」——是我先分类，能干的立刻干，干完汇报。

**触发时机**：Step 5 会议总结产出后，立刻对总结中的「下一步」/「待办」表逐条执行。

#### 7a. 分类框架

对每条待办，四分类：

| 分类 | 含义 | 执行策略 |
|------|------|---------|
| **AUTO** | 我能用现有工具独立完成 | **立刻执行，不等待，不询问** |
| **DRAFT** | 我能准备内容，但发送/提交需用户确认 | 草拟好，标注「确认后发送」 |
| **USER** | 只能用户操作 | 清晰标注，不给假方案 |
| **DEP** | 缺少前置条件（API 权限、系统访问等） | 标注缺失什么 + 怎么补齐 |

#### 7b. AUTO 类判断标准

以下是我能独立完成的（非穷举，原则判断）：

- ✅ **发送文件/材料**：把本地文件通过飞书发给用户（用户自己转发）
- ✅ **@Agent 协作群 bot**：@ISV助手/@样板间小管家/@马斯克/@Aime 获取信息
- ✅ **信息搜索**：公开搜索、C360 查客户、飞书文档搜索
- ✅ **创建文档**：飞书文档、飞书卡片、飞书多维表格
- ✅ **写代码/脚本**：试跑 demo、写 MCP 集成脚本
- ✅ **读写本地文件**：笔记、配置、数据文件
- ✅ **查询 API**：lark-cli、feishu-cli、C360 CLI
- ✅ **启动后台任务**：cronjob、轮询脚本

#### 7c. 执行原则

1. **AUTO 不等待不询问**：能做的直接做完，汇报「已完成：X」
2. **DRAFT 备好待确认**：内容写好，用户一句话「发」即发
3. **诚实说做不到**：USER/DEP 类不说「我帮你」，而是说「这需要你 + 为什么」
4. **先做再说**：不要先问「要不要做」，先做完再汇报
5. **并行优先**：多条 AUTO 类待办同时推进

#### 7d. 交付格式

会后统一汇报：

```
🤖 已自动完成（N 项）：
✅ 已把 XX 材料发给你
✅ 已 @样板间小管家 获取消费电子案例
✅ 已查 C360：客户 9 月到期，商机阶段：方案沟通

📝 已备好待确认（M 项）：
📋 ISV 整改反馈草稿 → 确认后发
📋 客户方案大纲 → 确认后展开

👤 需要你操作（K 项）：
⚠️ 约感臻老板会议 — 需要你来定时间
⚠️ 找 ISV 负责人面谈 — 需要你当面沟通
```

**这是 Step 5（会议总结）的自然延伸。总结产出后不要停——立刻走 Step 7 把能干的都干了。**

#### 7e. AI 需求特殊分派路径 🆕

会议中如果识别到 AI 场景需求（关键词：AI、智能体、自动化、多维表格、妙搭、Aily、Agent），除标准四分类外，额外输出一条结构化 AI 需求记录。

**信号 vs 噪音过滤**：
- ✅ **信号**：客户明确提出需求（「我们想搞个…」「能不能用 AI 做…」）、已落地的具体场景（「用妙搭搭了 XX」）
- ❌ **噪音，不提取**：标准产品介绍（只说「飞书有这个功能」但不涉及客户需求）、客户只说「在用飞书」但无具体产出、买了包但没用起来
- 如果一场会议**全是噪音**，不强行提取 AI 需求。宁可空着别凑数。

**输出格式**（8 字段）：

> 🚨 **「已用 AI」质量铁律**：「买了 AI 包」「开了 AI 功能」不算落地场景。必须是客户用某个工具**搭了具体的东西**——能说出「用什么工具 + 做了什么」的才算。
> ✅ 正确：「用妙搭搭了读书打卡小程序」「用 Claude Code 写了个自动化脚本」
> ❌ 错误：「买了 3 个 AI 基础版」「开了知识问答功能」
> 判断标准：如果描述只能落到「买了/开了」而没有具体产出物，就不是已实现的 AI 场景，不应列在「已用 AI」中。

| 字段 | 说明 | 提取来源 |
|------|------|---------|
| 公司 | 客户公司名 | 会议标题 / 参会人身份 |
| 部门 | 哪个部门 | 会议中提到 |
| 提出人 | 具体谁 | 会议中提到 |
| 需求简述 | 一句话痛点 | 客户原话提炼 |
| 场景描述 | 使用上下文完整链路 | 会议对话流还原 |
| 实现路径 | Hermes 推理的技术方案 | 基于飞书能力矩阵匹配 |
| **已用 AI** | 🆕 客户当前的 AI 工具/路径 | 「我们在用…」「目前是…」等句式 |
| 匹配材料 | 参考案例/方案 | 样板间/ISV 查询结果 |

**分派规则**：

```
AI 需求识别
  ├─ 含 ISV/产品/方案/分贝通等 → @ISV助手 拿材料
  ├─ 含案例/行业/参考 → @样板间小管家 拿案例
  └─ 纯 AI 场景需求 → 结构化输出给用户 → 用户转交多维表格智能体落盘
```

当前 A2A 不可用，第三条路径是 **Hermes → 用户 → 智能体** 的人肉桥接模式。等 A2A 就绪后改为直连。

详见 `references/post-meeting-dispatch.md`。

---

## 排查清单

| 问题 | 原因 | 解决 |
|------|------|------|
| 拉事件报 120003 (无权限) | 用户不在会 | 确认用户在会中 |
| 拉事件报 120002 (开关未开) | 会议 owner 未开启「允许智能体入会」 | 让 owner 在会议安全设置中开启（不同于 120003，这是专门的开关校验） |
| meeting_id 用错 | 用了 9 位会议号 | 用 `+meeting-list-active` 查到的长 ID |
| 拿不到实时字幕 | 会议未开启字幕/转写功能 | 确认会议开启了字幕 |
| lark-cli 报 401 | 授权过期或 scope 不全 | 重新执行 `lark-cli auth login --scope "vc:meeting.meetingevent:read"` |
| `--as user` 报错 | 未完成用户授权 | 先执行授权流程（两个阶段） |
| 后台脚本 Permission denied | poll.sh 无执行权限 | chmod +x 并用 bash poll.sh 启动 |
| 日志膨胀 / page_token 过期 | v1/v2 历史问题 | v3 已修复：砍掉 page_token，永远 --page-all + Python set() 去重 |
| 后台脚本被 kill，字幕丢失 | 进程无持久化 | v3 每轮追加写入 `~/meeting_logs/<id>.jsonl`；会后从此文件恢复 |
| 🚨 脚本退出后没推送纪要 | Agent 启动脚本后放任不管，未主动检测进程状态。已发生两次：7.10 高驰×分贝通 + 7.11 卿志聊 AI，第三次是事故 | 启动时记录 session_id，每 2-3 分钟 `process(action='poll')` 检查；status=`exited` 立刻走 Step 4.5→5→7 |
| 🆕 v4 守护进程被 kill（无字幕会议） | `set -e` 导致 run_poll 遇到 API 空返回时直接杀死整个守护 | v4 已改为 `set -uo pipefail`，run_poll 出错后守护继续跑 |
| 🆕 一对一通话无字幕 | 飞书 VC API 在一对一通话中不产生 `transcript_received` 事件，仅产生 join/leave | 正常现象，不是 bug。点名 0 人 + 无字幕 = 一对一通话，静默处理即可 |
| 🆕 守护进程卡在上一场会 | v4 早期 auto_mode 中 `run_poll` 同步阻塞——一对一通话无结束事件，run_poll 不返回，检测循环永远进不去 | 改为 `run_poll "$cur_id" "$cur_title" &` 后台子进程，主循环 10s 独立扫描新会议。无活跃会议时 kill 残留子进程 |
| 🆕 告警含客户合作金额（敏感信息泄露） | C360 `search all` 返回的 `arr` 和 `opportunity list` 的 `amount` 是客户合作金额，属于敏感数据，不应出现在告警/摘要/cron 输出中 | 已从 poll-v5.sh 移除 `arr_str` 列，告警仅含产品线 + 阶段。所有 cron 输出和文档也需避免具体金额数字 |
| 🆕 **会议结束未检测到**（v5 auto_mode 竞争条件） | `auto_mode` 外层循环发现 `meeting-list-active` 返回空后，**立即 kill run_poll**，此时 run_poll 正在 `sleep 10` 等待下次轮询，来不及调 `meeting-events` 看到 `"user is not in the meeting"` 就被杀。结果：日志无 `meeting_ended`，无结束通知 | v5 已修复：auto_mode 等待 run_poll 自然退出（轮询中自行检测 `"user is not in the meeting"`），最多 120s 超时。详见 `references/auto-mode-race-condition.md` |
| 🆕 **客户名检测盲区** | `check_client_mention` 仅在字幕文本中 grep 客户名。实际会议中**几乎不会说出公司全称**（如「机智连接」「PLAUD」），导致已知客户会议不触发 C360。案例：2026-07-15 PLAUD 会议，字幕含迁移/停用/账号数，因未出现客户名，C360 未触发 | **已缓解：** `client_list.json` 现支持 `c360_search` 字段指定 C360 搜索关键词，支持客户更名/改主体场景（如机智连接→普洛德）。详见 `references/client-name-aliases.md`。**根因未解决：** 仍需字幕中出现客户名才触发。改进方向：会前匹配参与者域名、`client_list.json` 增加姓名映射 |
| 🆕 **poll-v5 多实例并发** | 多次启动守护（手动重启、Agent 自动重启等）未检查已有进程，导致 3-4 个 poll-v5 同时运行，每个都独立轮询 API → 浪费配额、日志混乱 | 启动前检查已有进程：`pgrep -f poll-v5.sh && echo "already running" && exit 0`。用 lock file 机制（`/tmp/poll-v5.lock`）防止并发。详见 `references/multi-instance-prevention.md` |
| 🆕 **字幕仅捕获用户本人语音** | 飞书 VC API 的 `transcript_received` 事件中，`speaker.user_name` 在所有条目中**均显示为当前用户**（如「袁鑫杰」），无法区分是谁在说话。客户方的发言内容虽然被转写，但 speaker 标注不可靠 | 这是飞书 ASR 的已知限制。无法从 speaker 字段识别客户方发言人。客户名检测只能依赖字幕**文本内容**中出现客户名/品牌名。会后核对时建议用飞书妙记（官方转写有正确的 speaker 标注） |
| 🆕 **DM 入会/离会通知** | 用户反馈入会后没有第一时间收到通知，需要在聊天中手动说「监听会议」。poll-v5 原本只发告警到 `ALERT_CHAT`（Agent 协作群） | v5 已新增 `send_dm()` 函数：入会/离会时同步发送通知到用户 DM（`USER_DM` 变量配置）。用户打开飞书即可看到，无需手动通知 Agent |
| 🆕 **v5 auto_mode 可靠性退化**（2026-07-16） | v5 auto_mode 加入工作时间限制（10-19点 sleep 300s）+ 会议结束等 120s 退出逻辑。导致：①非工作时间会议完全漏检（零壹创新会议 7662267088883370969 无日志）②用户反馈「v5 效果没 v4 好」 | **已修复：** auto_mode 回退到 v4 简洁逻辑——去掉时间窗口限制，会议结束时立即 `kill` run_poll 并 reset。v5 保留的改进（点名/C360/关键词告警）不受影响。教训：简洁优先，不要过度工程化 |
| 🆕 **信息噪音原则**（2026-07-16） | Agent 不能自动感知会议——poll-v5 独立运行不通知 Agent。用户反复提醒「会议开始了，是不是又没监测到」 | 设置 Hermes cron job 做桥接（`schedule: 1,6,11,...` 错开整点）。核心规则：**不推「检测到会议」这种纯噪音，只推 C360 可行动情报**（商机/工单/跟进）。无内容时输出 [SILENT] 静默跳过。详见 `references/agent-notification-bridge.md` |
| 🆕 **Agent 不知道用户在开会** | poll-v5 launchd 守护独立运行，不通知 Hermes Agent。用户需要手动提醒 Agent 检测会议 | 设置 Hermes cron job（`every 5m`）做桥接：定期扫描活跃会议 → 查 C360 → 主动汇报。详见 `references/agent-notification-bridge.md` |
| 🆕⛔ **bash 轮询 API 超时冻结**（2026-07-16 和汪航测试会议） | `lark-cli vc +meeting-list-active` 调用卡住 54 分钟（13:52→14:46），`while sleep 10` 循环完全停顿。会议恰好在冻结期开始，poll-v5 日志无任何记录 | **bash 方案已废弃。** 迁移到 Hermes cron：API 超时只影响单次调用，下分钟重试。临时缓解：`perl -e 'alarm shift; exec @ARGV' -- 30 lark-cli ...` 加 30s 超时（但 bash 轮询本质脆弱，不推荐继续使用） |
| ⛔ **bash 轮询 v1→v5 五次迭代全失败**（2026-07-16 终局） | 用户：「每次都说修复好，自从迭代后没有一次成功的」| **不再修补 bash。** Hermes cron 架构替代：`272cdc68a518` every 1m，`meeting_state.json` 去重。旧 poll-v5.sh / launchd 已停用 |
| 🚨 **v5→v6 迁移丢失纪要能力**（2026-07-16） | v5 `meeting_detect.py` 只做 C360 推送，**完全没有启动 poll.sh 入会监听和产出纪要**。用户：「自从脚本更新到 V5 之后，好像都没有产出会议纪要了。就是这整个升级版本简直就是个大失败。」 | v6 已修复：`meeting_detect.py` 对所有新会议自动启动 `poll.sh` 后台监听。客户会议额外推 C360。**教训**：任何迁移必须保留核心能力清单对照（监听 + 纪要 + C360），缺一不可。 |
| 🚨 **纪要自动生成已实现**（v6 2026-07-16） | v6 会议大脑 cron (`f64f153f96ec`, `*/3 * * * *`) 负责：① 客户会议入会 → C360 `search all` + `follow_up +recent` → 飞书卡片；② 会议结束（`completed` 状态）→ 读 JSONL → 分析 → 飞书卡片纪要 → Step 7 会后自动执行。成本 ~¥1/天。 | ✅ 已解决。两条 cron 互补：`272cdc68a518`（零 token 检测） + `f64f153f96ec`（LLM 智能处理）。 |

---

## 会议会前准备

当用户告知要去见某个客户或参加某场会议时，自动触发会前简报流程。详见 `references/meeting-pre-briefing.md`。

**三步流程**：
1. **C360 客户情报** — `search all` → 商机+ARR+阶段 → `follow_up +recent` → `contact list`
2. **行业/政策背景搜索** — 如适用（OPC 政策、竞品动态、官方媒体口径）
3. **延展话题准备** — 行业趋势、产品对标、AI 话题

**必须用飞书交互卡片输出**，格式参考 `output-style-xiaoguanjia` skill。

**实战案例**：2026-07-16 WeWork 社区负责人会议 — 非飞书客户，跳过 C360，搜索 OPC 政策 + WeWork 中国新闻 → 整理为话题清单卡片。

---

## 会后分析框架

会议结束后，从 JSONL 日志提取唯一字幕，套用以下框架生成结构化分析：

| 框架 | 分析维度 | 输出 |
|------|---------|------|
| **JTBD** | 客户"雇佣"飞书的底层任务（功能/情感/社会性） | 按三层分解需求 |
| **BANT** | 预算/决策权/需求紧迫度/时间线 | 成交可能性和优先级 |
| **Kano** | 基本型/期望型/兴奋型/反向需求 | 产品满足度评估 |
| **Mom Test** | 区分真痛点 vs 客套话 | 高/低信号标注 |

**使用原则**：数据优先，框架适配在后。不要用框架套数据，让数据选出最合适的框架。详见 `meeting-audit` skill 的「需求分析方法论」章节。

---

## 注意事项

1. **必须 `--as user`**：不能用 bot 身份，必须用户授权后以用户身份调用
2. **长 meeting_id ≠ 9 位会议号**：从 `+meeting-list-active` 拿的 `meeting_id` 才是正确的 API 参数
3. **无实时推送**：所有事件都靠轮询拉取，延迟 15-30 秒
4. **用户必须本人在会中**：Agent 不能替代用户入会，只能旁听用户已在的会议
5. **字幕需要去重**：同一 `sentence_id` 可能多次推送（修正/补全），保留最新版本
6. **旁听不可见**：会议里不会出现机器人，其他参会者感知不到
7. **发分析结果用 `--as bot`**：VC API 调用用 `--as user`，但飞书 IM 发消息用 `lark-cli im +messages-send --as bot`（当前无 `im:message.send_as_user` scope）
