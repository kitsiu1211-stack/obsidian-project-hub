# Skill 路由表 v1

> 8 Zone 匹配。收到消息先匹配 Zone，只加载命中 Zone 的 skill。

## Zone 1 · 会议

feishu-meeting-listen, meeting-audit, meeting-minutes, meeting-followup-material, lark-vc, lark-vc-agent, lark-minutes, lark-note, 客户AI场景需求整理

## Zone 2 · 客户/销售

c360-cli, sales-playbook, renewal-proposal, client-handover-checklist, customer-research, workshop-interest-activation, opportunity-cross-analysis, manager-ai-onboarding, output-style-xiaoguanjia

## Zone 3 · 文章/内容分析

文章分析, ljg-rank, ljg-learn, ljg-plain, ljg-card, ljg-qa, human-writing, explain-like-village-elder, deep-grill, grill-with-docs, diverge-converge, knowledge-capture

## Zone 4 · 飞书工具

lark-cli, lark-doc, lark-im, feishu-api, feishu-card-send, feishu-group-chat, beautiful-feishu-whiteboard, hermes-feishu-gateway, lark-shared, feishu-thread-reply, lark-apps, miaoda-deploy, lark-base, lark-sheets, lark-drive, lark-wiki, lark-calendar, lark-mail, lark-task, lark-okr, lark-approval, lark-markdown, lark-contact, lark-slides, lark-whiteboard, lark-event, lark-openapi-explorer, lark-skill-maker, lark-attendance

## Zone 5 · 知识/记忆

obsidian, ebbinghaus-review, memory-compress, memory-management, daily-session-summary, weekly-deep-read, skill-hub, 双周Skill同步, weread, ai-industry-brief

## Zone 6 · 代理协作

agent-group-collab, aime-query, multi-agent-orchestration, trae-loop-engineering, subagent-driven-development

## Zone 7 · 生活

my-coffee, find-nearby, xitter

## Zone 8 · 不加载

除非用户点名，永远不碰：
humanizer, bolt-slides, sketch, petdex, kanban-orchestrator, kanban-worker, kanban-codex-lane, mcporter, native-mcp, fish-audio-tts, volcengine-tts, doubao-tts, to-spec, writing-plans, upload-file-to-tos, loop-me, loop-engineering-pipeline, post-handover-intelligence, tech-project-evaluation, chinese-company-research, whisper, hermes-agent-skill-authoring, code-review, implement, plan, to-tickets, handoff, setup-matt-pocock-skills, html-generation, side-hustle-planning, xianyu-listing-writer, linear, supabase-auth-otp-v2, share-material-review, no-fabrication, apple-design, emil-design-eng, animation-vocabulary, find-animation-opportunities, improve-animations, review-animations, agent-world, popular-web-designs, design-taste-frontend, baoyu-design, claude-design, apple-notes, apple-reminders, findmy, imessage, maps, airtable, google-workspace, teams-meeting-pipeline, notion, himalaya, xurl, blogwatcher, polymarket, openhue, arxiv, llm-wiki, comfyui, audiocraft, llama-cpp, serving-llms-vllm, segment-anything-model, evaluating-llms-harness, weights-and-biases, ascii-art, ascii-video, manim-video, p5js, songsee, heartmula, songwriting, touchdesigner-mcp, pretext, excalidraw, architecture-diagram, baoyu-infographic, gif-search, jupyter-live-kernel, dogfood, design-md, ocr-and-documents, nano-pdf, powerpoint, no-fabrication, github-code-review, github-issues, github-pr-workflow, github-repo-management, codebase-inspection, spike, simplify-code, systematic-debugging, test-driven-development, python-debugpy, node-inspect-debugger, requesting-code-review, opencode, claude-code, codex, computer-use, biweekly-skill-sync, client-ai-scenario-extract, renewal-proposal, research-paper-writing, xunji-diet-api, xunji-training-api, youtube-content, macos-computer-use

## 匹配规则

| 触发词 | Zone |
|--------|------|
| 旁听/入会/会议 | 1 |
| 客户/销售/方案/续约 | 2 |
| 发链接/分析文章/看看 | 3 |
| lark-cli/飞书API/卡片 | 4 |
| Obsidian/记忆/回顾/技能同步 | 5 |
| @Agent群/代理/Aime | 6 |
| 咖啡/地图/附近 | 7 |

## Token 分析

| 版本 | Skill 数 | 注入 Token | vs 当前 |
|------|---------|-----------|---------|
| 当前（全量） | 243 | ~5554 | - |
| 拆 Profile 到 40 个 | 40 | ~914 | 省 84% |
| 拆 Profile 到 25 个 | 25 | ~571 | 省 90% |
| 拐点 | ≤50 | ≤1143 | 省 79%+ |
