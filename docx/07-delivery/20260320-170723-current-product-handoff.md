# 灵枢台当前成品接管说明（编排增强后）

- 阶段：07-delivery
- 提交时间：20260320-170723
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/07-delivery/20260320-170248-workflow-orchestration-ux-delivery.md
  - docx/07-delivery/20260320-163234-external-mcps-delivery.md

## 目标

1. 给新会话提供单一接管入口。
2. 让后续继续开发时不必回看全部历史聊天。

## 核心内容

## 当前状态

- 当前状态：阶段性交付可用
- 真实性质：不是最终完整版，但已具备更完整的本地管理与编排演示能力
- 最新增强基线：
  - `docx/07-delivery/20260320-170248-workflow-orchestration-ux-delivery.md`

## 当前已完成能力

1. `Skills`
   - managed CRUD
   - `codex` / `cludea` / `opencode` 外部 skill 发现
   - discovered skill 详情读取与只读保护
2. `MCPs`
   - managed CRUD
   - `cludea` / `opencode` 外部 MCP 发现
   - discovered MCP 详情读取与只读保护
3. `Agents`
   - managed CRUD
   - Skill 多选、MCP 关联、Tool Scope 配置
4. `Workflows`
   - CRUD
   - 节点模板
   - 缩放、平移、自动布局
   - 节点结构化配置
   - 连线标签与条件
   - 后端结构校验
5. `Dashboard / Discovery`
   - 汇总统计
   - 外部 skill / MCP 发现状态展示

## 已验证结果

1. `npm run build` 通过
2. `py_compile` 已覆盖关键后端文件
3. 真实 HTTP 已验证：
   - `Skills` CRUD
   - `MCPs` CRUD
   - 外部 discovered skill / MCP 详情与只读保护
   - `Workflows` richer payload round-trip
   - 非法 workflow `422 workflow_invalid`
   - `Dashboard` / `Discovery` 统计

## 主要文件入口

1. 前端：
   - `src/pages/SkillsPage.vue`
   - `src/pages/McpsPage.vue`
   - `src/pages/AgentsPage.vue`
   - `src/pages/WorkflowsPage.vue`
   - `src/pages/DashboardPage.vue`
2. 后端：
   - `backend/app/services/discovery.py`
   - `backend/app/routers/skills.py`
   - `backend/app/routers/mcps.py`
   - `backend/app/routers/workflows.py`
   - `backend/app/routers/dashboard.py`
   - `backend/app/routers/discovery.py`

## 明确未完成项

1. 外部 MCP 回写尚未实现
2. `Monaco Editor` 尚未接入
3. 自动化测试体系尚未建立
4. 当前编排器体验已明显增强，但仍不是完整第三方流程图引擎
5. 当前目录仍不是 Git 仓库

## 建议下一步优先级

1. 自动化测试
   - 后端 API 回归
   - Workflows 关键交互冒烟
2. `Monaco Editor`
   - Skill / Prompt / JSON 编辑体验升级
3. 外部 MCP 回写
   - 在确认真实格式样本后再补

## 新窗口接手提示

1. 若开新会话，优先读取本文件。
2. 再读取：
   - `docx/07-delivery/20260320-170248-workflow-orchestration-ux-delivery.md`
   - `docx/07-delivery/20260320-163234-external-mcps-delivery.md`
3. 若继续沿用 `docx` 工作流，新一轮应从 `00-governance` 新建时间戳台账开始。

## 风险与待确认项

1. 当前成品适合继续开发与演示，但不能宣称最终完整版已完成。
2. 后续若继续推进，应保持“真实验证先行、文档同步批准”的工作流。

## 交接输出

1. 本文件可作为压缩上下文后的最新单一接管入口。
2. 允许基于本文件在新会话继续推进。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-170723
- 备注：本文件用于编排体验增强后的最新接管，不改变项目仍为 partial 的判断。
