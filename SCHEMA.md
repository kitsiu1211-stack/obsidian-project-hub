---
title: Schema
created: 2026-06-18
updated: 2026-06-18
type: meta
tags: [meta, schema]
---

# Wiki Schema

## Domain

AI/ML 思考与实践——涵盖 Agent 架构、Harness 工程、管理哲学、AI 落地、Skill 设计、组织转型等主题。起源自 Karpathy GBrain 模式，将个人思考日记编译为结构化知识图谱。

## Conventions

- **File names**: 中文主题名，不带编号前缀（放在 concepts/ 目录下由 index.md 统一管理）
- **Wikilinks**: 使用 `[[filename]]` 格式，Obsidian 自动解析最短路径
- **Frontmatter**: 每个 wiki 页面必须包含 `title`、`created`、`updated`、`type`、`tags`
- **Page structure**: 每个概念页面包含 Compiled Truth → 关键要点 → 关联主题 → Timeline 四个板块
- **更新时**：必须 bump `updated` 日期，并追加到 `log.md`
- **新增页面**：必须加入 `index.md` 对应分类，至少 2 个 wikilinks
- **Provenance**: 合成类页面标注来源 `^[raw/articles/source.md]`

## Tag Taxonomy

- **架构**: agent, multi-agent, harness, skill-design, context-engineering
- **管理**: management-philosophy, org-transformation, talent-density, ai-native-org
- **技术**: prompting, model-selection, knowledge-compilation, vibe-coding, agentic-coding
- **商业**: ai-adoption, dark-knowledge, rebuttal-framework, opportunity-framework
- **个人**: personal-growth, emergence, knowledge-graph, ai-exposure
- **Meta**: meta, schema, index

## Page Thresholds

- **Create a page** when a concept appears in 2+ sources OR is central to one source
- **Add to existing page** when new info relates to an existing concept
- **Split a page** when it exceeds ~200 lines — break into sub-topics
- **Archive a page** when fully superseded — move to `_archive/`

## Update Policy

When new information conflicts:
1. Check dates — newer sources generally supersede
2. Note both positions with dates and sources
3. Flag for review in the lint report
