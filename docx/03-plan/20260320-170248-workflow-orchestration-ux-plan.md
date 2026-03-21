# 工作流编排体验增强实施计划

- 阶段：03-plan
- 提交时间：20260320-170248
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/00-governance/20260320-164024-workflow-orchestration-ux-run-ledger.md
  - docx/01-requirements/20260320-142228-requirements-baseline-import.md
  - docx/02-architecture/20260320-142228-architecture-baseline-import.md
  - docx/07-delivery/20260320-163234-external-mcps-delivery.md
  - docx/07-delivery/20260320-151548-workflows-vertical-slice-delivery.md

## 目标

1. 为“工作流编排体验增强”切片建立单独实施计划。
2. 在不引入新依赖的前提下，把现有最小工作流编辑器升级到更接近真实编排器的交互。
3. 同步补齐后端结构校验，避免 richer workflow 数据模型写入脏数据。

## 核心内容

1. 基线沿用结论：
   - 不新增 `01-requirements` / `02-architecture` 文档。
   - 继续沿用既有已批准需求与架构基线。
2. 本轮范围：
   - 扩展前端 workflow 数据模型，接入 `node.config` 和 `edge.condition`。
   - 重构 `WorkflowsPage.vue`，加入节点模板、缩放平移、自动布局、连线标签与条件、结构化节点配置、校验提示。
   - 在 `backend/app/routers/workflows.py` 加入保存前结构校验。
   - 在 `README.md` 与 `docx` 中同步当前编排能力。
3. 本轮非范围：
   - 不引入 `Vue Flow` 等新依赖。
   - 不实现工作流执行引擎。
   - 不重做其它资源 CRUD。
   - 不接入 Monaco 或自动化测试框架。
4. 推荐实现路径：
   - 前端保持单文件页面实现，避免当前阶段过早组件化导致回归面扩大。
   - 画布采用“场景平移缩放 + SVG 连线 + 节点模板 + 右侧检查器”的方式增强体验。
   - 后端采用路由层轻量校验，优先拦住明显结构错误。
5. 并行拆分结论：
   - 不建议并行 worker。
   - 原因：核心改动集中在同一 workflow 前后端链路，拆分会造成强耦合冲突。

## 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| 主代理 | Workflows 前后端增强、验证、README、`docx/` | `src/pages/WorkflowsPage.vue`、`src/api/contracts.ts`、`src/types/resources.ts`、`src/data/mock.ts`、`src/styles/main.css`、`backend/app/routers/workflows.py`、`README.md`、`docx/` | 本文档与既有批准基线 | 增强后的编排体验、校验结果、阶段文档 |

## 完成定义

1. `npm run build` 通过。
2. Workflow 可保存并回读节点配置 `config` 与连线条件 `condition`。
3. 画布支持缩放、平移、自动布局和基于模板的新建节点。
4. 页面可视化呈现结构性告警，不再只依赖后端失败后再看错误。
5. 非法 workflow 数据提交会返回 `422 workflow_invalid`。
6. 真实 HTTP 验证通过 workflow 创建、读取、删除和非法 agent 校验场景。

## 风险与待确认项

1. 该方案显著提升体验，但仍然是“增强版自研画布”，不是完整第三方流程图引擎。
2. 画布复杂度提升后，浏览器级手工交互仍需要后续专门测试补强。
3. 若后续需要多人协同或执行态监控，需要新的架构切片，不应在本页继续堆叠。

## 交接输出

1. 允许实施阶段直接修改 workflow 相关前后端文件与样式。
2. 测试阶段需把真实 HTTP round-trip 和 `422 workflow_invalid` 的错误样例写入测试文档。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-170248
- 备注：本轮以“更接近完整编排体验”为目标，但仍保持无新依赖、无执行引擎的边界。
