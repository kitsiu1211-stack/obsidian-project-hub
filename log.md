     1|     1|     1|     1|     1|---
     2|     2|     2|     2|     2|title: Wiki Log
     3|     3|     3|     3|     3|created: 2026-06-18
     4|     4|     4|     4|     4|updated: 2026-06-18
     5|     5|     5|     5|     5|type: meta
     6|     6|     6|     6|     6|tags: [meta, log]
     7|     7|     7|     7|     7|---
     8|     8|     8|     8|     8|
     9|     9|     9|     9|     9|# Wiki Log
    10|    10|    10|    10|    10|
    11|    11|    11|    11|    11|> Chronological record of all wiki actions. Append-only.
    12|    12|    12|    12|    12|
    13|    13|    13|    13|    13|## [2026-06-18] create | Wiki initialized
    14|    14|    14|    14|    14|
    15|    15|    15|    15|    15|- Domain: AI/ML 思考与实践
    16|    16|    16|    16|    16|- Source: 飞书文档 OGBVdDVjJohAGkxItSXcODxunjh（2026.2.26-2026.5.6 思考日记）
    17|    17|    17|    17|    17|- Structure: 升级为 Karpathy LLM Wiki 标准结构（SCHEMA.md + index.md + log.md + raw/ + concepts/）
    18|    18|    18|    18|    18|- Pages created: 24 个概念页面（concepts/），1 个主索引（index.md）
    19|    19|    19|    19|    19|- Raw source saved: raw/articles/feishu-ai-thinking-knowledge-graph.md
    20|    20|    20|    20|    20|- Previous flat structure (25 .md files in root) reorganized into layered wiki
    21|    21|    21|    21|    21|
    22|    22|    22|    22|    22|## [2026-06-18] update | All 24 concept pages
    23|    23|    23|    23|    23|
    24|    24|    24|    24|    24|- 统一四板块结构：Compiled Truth + 关键要点 + 关联主题 + Timeline
    25|    25|    25|    25|    25|- Timeline 补充了从飞书原始文档提取的思考演变记录
    26|    26|    26|    26|    26|- 主题22 新增延伸：歸藏「爆款Skills万字长文」阅读收获
    27|    27|    27|    27|    27|- 主题24 新增延伸：知识图谱从飞书迁移到 Obsidian
    28|    28|    28|    28|    28|
    29|    29|    29|    29|## [2026-06-18] extend | 对话延伸写入
    30|    30|    30|    30|
    31|    31|    31|    31|- 主题22: 瑞幸MCP实践验证 + 艾宾浩斯复习系统设计
    32|    32|    32|    32|- 主题24: LLM Wiki标准升级 + 艾宾浩斯集成闭环
    33|    33|    33|    33|- 主题13: Karpathy LLM Wiki模式实践
    34|    34|    34|    34|- Cron job 创建: 艾宾浩斯知识复习（job_id: 3a456f2fcccb，每天9:00）
    35|    35|    35|    35|
    36|    36|    36|## [2026-06-18] extend | 艾宾浩斯复习延伸写入
    37|    37|    37|
    38|    38|    38|- 主题1: Plan模式深度剖析——演化路径（Claude Code → Codex → Cursor）+ 哲学本质（= 阿基米德式提问法）+ 95%理解度门禁
    39|    39|    39|- Memory: 新建「Plan 模式门禁」约束，精简3条冗余条目
    40|    40|    40|
    41|    41|## [2026-06-18] fix | 复习系统个性化升级
    42|    42|
    43|    43|- ebbinghaus-review skill: 新增「思考题适配规则」——用户画像+场景转换模板，禁止技术实现类问题
    44|    44|- review-schedule.md: 新增用户上下文字段，cron job 读取后适配思考题
    45|    45|- Cron job 3a456f2fcccb: Prompt 更新——嵌入用户角色+场景转换表+具体示例
    46|    46|- User profile: 新增业务画像（老客户销售/消费电子/存量保护+增量挖掘）
    47|    47|- Memory: 新增 Plan 模式门禁约束（≥95% 理解度再执行）
    48|    48|
    49|## [2026-06-18] extend | 艾宾浩斯复习延伸——多Agent架构
    50|
    51|- 主题2: 新增「实战模式：协作群 + Orchestrator 编排」章节——Hermes/Aime/马斯克三Agent协同，Context Protection + Parallelization + Specialization 三判据在老客户销售场景的落地
    52|- 核心洞察：多Agent拆分不是炫技，是任务复杂度超出单Agent上下文容量的自然结果
    53|
## [2026-06-18] extend | 艾宾浩斯复习延伸——训模型 × 涌现概率

- 主题4（训模型式管理）↔ 主题20（涌现概率框架）：双向打通
- 核心合成：两者是同一逻辑链的两种表述——识别可燃的人（初始化/可燃性）→ 给体验（环境触发）→ 首次成功 → 自燃扩散
- 新增对照表：罗福莉三要素 ↔ 涌现公式三因子
- 新增逻辑链路图：从筛选到扩散的完整闭环

## [2026-06-18] create | 主题25：反馈即负熵与人机协作怀疑论

- 触发：用户阅读维纳《人有人的用处》，思考反馈/上下文对AI输出的放大效应
- 维纳视角：信息是负熵，上下文越丰富→AI不确定性越低→输出越定制化
- 笛卡尔视角：AI不会怀疑自己（无第一人称自反性），幻觉是架构性的，不是bug
- 核心合成：人机协作不是"人决定+AI干活"，而是"人持续喂养上下文→AI持续逼近人的判断标准"——师徒模型取代工具模型
- 关联：主题3（Harness反馈回路）、主题19（Context not Control）、主题6（上下文压缩）、主题18（约束优于指令）
- 分类：「提示词与知识工程」
