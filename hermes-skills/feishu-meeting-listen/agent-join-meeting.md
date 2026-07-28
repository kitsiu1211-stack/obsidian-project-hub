# 智能体入会 — 完整上下文存档

## 演进历史

| 版本 | 时间 | 方案 | 核心技术 | 状态 |
|------|------|------|------|------|
| V1 | 早期 | bash 轮询 | lark-cli + shell 脚本 | 废弃 |
| V2 | 中期 | cron 轮询 | meeting_detect.py 零 token 检测 | 废弃 |
| V3 | 中期 | 字幕轮询 | meeting_transcribe.py 字幕采集 | 当前个人通话备用 |
| V4 | 0707-0717 | 实时语音旁听 | MacBook 麦克风 → Paraformer ASR → DeepSeek → Fish Audio TTS | 已停用 |
| V5 | 0717 | 零 Token 检测 | cron + Python 检测脚本 | 废弃 |
| **官方** | **0717** | **Bot 真实入会** | **ByteView WebSocket + 豆包端到端实时语音** | **当前主力** |

## 当前方案：官方 Bot 入会 + 豆包实时语音

### 项目位置
`~/Documents/Codex_Project/feishu-voice-agent-starter/`

### 文件结构
```
feishu-voice-agent-starter/
├── main.py                    # 主流程（自动检测会议号 + Bot入会 + ByteView + 豆包）
├── config.yaml                # 豆包凭证
├── requirements.txt           # websockets>=12.0
├── persona.md                 # AI 人设
└── voice_agent/
    ├── config.py              # 配置加载
    ├── lark_cli.py            # 入会/离会/endpoint
    ├── byteview_protocol.py   # Frontier Frame 编解码
    ├── byteview.py            # 飞书实时音频桥接
    ├── doubao_protocol.py     # 豆包二进制协议
    ├── doubao.py              # 豆包实时语音客户端
    ├── audio_utils.py         # PCM 重采样 (24k→16k)
    ├── ws_compat.py           # websockets 版本兼容
    └── logging_utils.py       # 日志
```

### 运行方式
```bash
cd ~/Documents/Codex_Project/feishu-voice-agent-starter
python3 main.py                      # 自动检测活跃会议并入会
python3 main.py --meeting-no <9位>   # 指定会议号
python3 main.py --check              # 检查配置
```

### 所需权限
- vc:meeting.bot.join:write（Bot 入会）
- vc:meeting.bot.realtime:write（实时音频流）

### 事件订阅（已配置）
- vc.bot.meeting_invited_v1（被邀请入会事件）
- 飞书开放平台控制台 → 事件订阅 → 已添加

### 豆包凭证
- APP ID: 2353725770
- Access Token + Secret Key: 见 config.yaml
- WebSocket: wss://openspeech.bytedance.com/api/v3/realtime/dialogue
- Resource ID: volc.speech.dialog

### 音频链路
```
会场语音(24kHz PCM) → ByteView WS → PcmRateConverter(24k→16k) → 豆包模型 → TTS(24kHz PCM) → ByteView WS → 会场播放
```

### 已知限制
- 仅支持标准会议（9 位会议号），不支持个人视频通话
- 需在会议设置中勾选「允许智能体加入会议」
- 豆包 Access Token 使用「服务接口认证信息」里的凭证，非 API Key 管理

## 备用方案：字幕旁听（个人通话）

### 脚本位置
`~/.hermes/scripts/meeting_transcribe.py`

### 运行方式
```bash
while true; do python3 ~/.hermes/scripts/meeting_transcribe.py; sleep 15; done
```

### 工作原理
- 每 15 秒轮询 lark-cli 获取字幕
- 写入 `~/.hermes/cache/meeting_logs/<meeting_id>.jsonl`
- 会议结束后由 Agent 生成纪要

## 已停用方案文件清单

| 文件 | 用途 | 停用日期 |
|------|------|------|
| ~/.hermes/scripts/meeting_voice.py | V4 实时语音旁听 | 0717 |
| ~/.hermes/scripts/meeting_detect.py | 零 token 会议检测 | 0717 |
| ~/.hermes/scripts/doubao_tts_proto.py | 豆包 TTS 协议（旧版） | 0717 |
| ~/.hermes/cron/meeting_state.json | 会议状态文件 | 0717 |
| ~/.hermes/cron/trigger_meeting_notes.json | 纪要触发标记 | 0717 |
| ~/.hermes/skills/feishu/feishu-meeting-listen/scripts/poll-v5.sh | bash 轮询 | 0717 |
| ~/.hermes/skills/feishu/feishu-meeting-listen/scripts/poll.sh | 旧版轮询 | 0717 |

## 关键文档
- 飞书智能体入会配置方案: https://bytedance.larkoffice.com/docx/VXnpdcUFWotAmexKWmUcAwA4nCe
- 智能体入会被 Call 入会指南: https://bytedance.larkoffice.com/docx/Q6nWdDKwIo8Zw4x7TLRcnXEDnYb
- 豆包实时语音 API: https://www.volcengine.com/docs/6561/1594356
