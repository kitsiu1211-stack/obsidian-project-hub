# Hermes Skill 版本管理

## 规则

1. **每次升级前**：在 `hermes-skills/<skill-name>/versions/` 创建旧版本快照
2. **快照内容**：
   - 完整代码文件（SKILL.md、脚本、配置）
   - 版本号 + 日期 + 状态
   - 当前 cron 配置列表
3. **升级铁律**：
   - 新版本 = 旧版本全部功能 + 新增功能
   - 不加不减，只叠加
   - 改动前先读 `versions/` 里的历史快照
4. **回退**：从 `versions/` 找到目标版本 → 复制回 hermes 目录 → 恢复 cron 配置

## 目录结构

```
hermes-skills/
└── <skill-name>/
    ├── retrospective.md      # 版本演进复盘
    ├── SKILL.md              # 当前主配置快照
    ├── <脚本名>.py           # 当前脚本快照
    └── versions/
        └── V<版本号>-<日期>.md  # 版本快照
```

## 已有 Skill 档案

| Skill | 最新版本 | 状态 |
|-------|---------|------|
| feishu-meeting-listen | V3-restored (2026-07-16) | active |
