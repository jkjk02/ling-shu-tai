# 工作流编排体验增强运行台账

- 阶段：00-governance
- 提交时间：20260320-164024
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/07-delivery/20260320-163234-external-mcps-delivery.md
  - docx/07-delivery/20260320-155331-final-product-handoff.md
  - docx/07-delivery/20260320-151548-workflows-vertical-slice-delivery.md

## 目标

1. 为新一轮“工作流编排体验增强”切片建立独立台账。
2. 在不引入新依赖和不重做既有 CRUD 的前提下，把 Workflows 从最小画布提升到更接近完整编排器的体验。
3. 固定本轮范围、验证门槛和交付文档链，方便后续新会话接手。

## 核心内容

1. 当前项目状态：
   - 项目仍为阶段性交付成品，不是最终完整版。
   - `Skills` / `MCPs` / `Agents` / `Workflows` managed CRUD 已完成。
   - 外部 Skill 发现与外部 MCP 发现已接入只读读链路。
2. 本轮优先级判断：
   - 用户明确要求“接近完整编排体验”并继续推进。
   - 现有 `WorkflowsPage.vue` 仍是最小实现：仅支持节点拖拽、简单连线表单和保存加载。
   - 因此本轮锁定为“工作流编排体验增强”，暂不进入 Monaco 与自动化测试体系建设。
3. 继续沿用的批准基线：
   - 需求基线：`docx/01-requirements/20260320-142228-requirements-baseline-import.md`
   - 架构基线：`docx/02-architecture/20260320-142228-architecture-baseline-import.md`
   - 既有 Workflows 交付基线：`docx/07-delivery/20260320-151548-workflows-vertical-slice-delivery.md`
4. 本轮范围：
   - 升级 Workflows 前端画布体验：节点模板、缩放平移、自动布局、结构化节点配置、连线条件编辑、结构校验提示。
   - 补齐前端对后端已有 `node.config` / `edge.condition` 的映射和保存。
   - 在后端新增 workflow 结构校验，阻止引用不存在 Agent、无效连线、重复 ID 等脏数据落盘。
   - 补充 README 与本轮 `docx` 文档链。
5. 本轮非范围：
   - 不引入 `Vue Flow` 或其它新前端依赖。
   - 不重做已完成的 CRUD。
   - 不实现工作流运行时执行引擎。
   - 不在本轮接入 Monaco 或自动化测试框架。
6. 验证门槛：
   - `backend/.venv/bin/python -m py_compile ...`
   - `npm run build`
   - 真实 HTTP 验证 workflow 富载荷的创建、读取、删除和后端校验失败场景

## 风险与待确认项

1. 本轮通过自研画布增强提升体验，但仍不是完整 `Vue Flow` 等级的可视化引擎。
2. 新增 `node.config` 与 `edge.condition` 后，前后端字段映射必须保持一致，否则会出现“UI 改了但未持久化”的假闭环。
3. 当前目录不是 Git 仓库，本轮继续只通过 `docx` 文档固化状态。

## 交接输出

1. 允许计划阶段按“前端画布体验 + 后端结构校验 + 真实 HTTP 验证”组织实施。
2. 要求测试阶段至少覆盖：
   - `POST /api/workflows`
   - `GET /api/workflows/{id}`
   - `DELETE /api/workflows/{id}`
   - 非法 `agent_id` workflow 提交返回 `422 workflow_invalid`
3. 交付阶段需要额外生成一份新的 handoff 文档，方便新会话快速接手。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-164024
- 备注：本轮沿用既有批准基线，仅新增“工作流编排体验增强”切片。
