# 会议轮询检测（已停用）

## 用法
需要时告诉 Hermes「把会议轮询加回来」即可一键恢复。

## 机制
- `meeting_detect.py` — 零 token 检测脚本
- Hermes cron 每 1 分钟触发一次
- 调用 `lark-cli vc +meeting-list-active --as user` 查活跃会议
- 客户会议（标题含「客户名 x 飞书」）→ 写触发标记 → LLM cron 读标记后启动 V4 + 纪要
- 非客户会议不处理

## 文件
- 检测脚本：`~/.hermes/scripts/meeting_detect.py`
- 状态文件：`~/.hermes/cron/meeting_state.json`
- 触发标记：`~/.hermes/cron/trigger_meeting_notes.json`

## 恢复命令
```
hermes cron create --schedule "every 1m" --prompt "运行 python3 ~/.hermes/scripts/meeting_detect.py" --name "会议检测（零token）" --no_agent true --script ~/.hermes/scripts/meeting_detect.py
```
