---
date: 2026-07-17
version: V4-realtime-asr
status: active
---

# feishu-meeting-listen V4 实时语音版

## 架构变更

V3 → V4 最大变化：**字幕轮询 → 实时音频流 ASR**

```
V3:  lark-cli 字幕(3秒轮询) → DeepSeek → 豆包TTS  (~5-7秒)
V4:  BlackHole → Paraformer-realtime-v2 → DeepSeek → 豆包TTS  (~2-3秒)
```

## 新增

- 音频采集线程：PyAudio → BlackHole 2ch (16kHz, 200ms chunks)
- ASR：DashScope WebSocket `paraformer-realtime-v2` (流式，句末触发)
- 去轮询：不再依赖 lark-cli `+meeting-events` 3 秒轮询
- 延迟：从 5-7 秒 → 2-3 秒

## 凭据

全部从 `config/.env` 读取，无需在脚本中硬编码。

## 启动方式

```bash
# 1. 确保音频路由: 系统输出 → "会议旁听" (BlackHole + 扬声器)
# 2. 进入飞书会议
# 3. 运行:
python3 ~/.hermes/scripts/meeting_voice.py
# 4. 说「浪子」触发语音回复
```
