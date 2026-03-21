# 外部MCP发现实施计划

- 阶段：03-plan
- 提交时间：20260320-163234
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/00-governance/20260320-162533-external-mcps-run-ledger.md
  - docx/01-requirements/20260320-142228-requirements-baseline-import.md
  - docx/02-architecture/20260320-142228-architecture-baseline-import.md
  - docx/07-delivery/20260320-161543-other-cli-external-skills-delivery.md

## 目标

1. 为“外部 MCP 发现”切片建立单独实施计划。
2. 在不重复已完成 CRUD 的前提下，补齐 `cludea` / `opencode` 外部 MCP 的 discovered 接入。
3. 明确本轮验证点与非范围，避免将回写与编辑体验混入本切片。

## 核心内容

1. 基线沿用结论：
   - 不新增 `01-requirements` / `02-architecture` 文档。
   - 继续沿用 `docx/01-requirements/20260320-142228-requirements-baseline-import.md` 与 `docx/02-architecture/20260320-142228-architecture-baseline-import.md`。
2. 本轮范围：
   - 扩展 `backend/app/services/discovery.py`，将外部 JSON MCP 文件解析为 discovered MCP 资源。
   - 扩展 `backend/app/routers/mcps.py`，让 `/api/mcps` 与 `/api/mcps/{id}` 支持 discovered MCP 列表与详情。
   - 继续沿用只读保护语义，禁止更新和删除 discovered MCP。
   - 扩展 `backend/app/routers/dashboard.py`，让 MCP 统计包含 discovered MCP。
   - 对 `src/pages/McpsPage.vue` 做最小可见性补充，展示来源类型。
3. 本轮非范围：
   - 不重复做 managed `Skills` / `MCPs` / `Agents` / `Workflows` CRUD。
   - 不实现外部 MCP 回写。
   - 不接入 `Monaco Editor`、不增强 `Workflows` 画布、不扩建自动化测试体系。
4. 推荐实现路径：
   - 对 MCP 继续采用候选目录 + JSON 最佳努力解析。
   - 统一输出 `source_kind=discovered`、`is_writable=false`。
   - 让 `MCPs` 页、Dashboard、Discovery 都继续复用既有契约与字段模型。
5. 并行拆分结论：
   - 不建议并行 worker。
   - 原因：核心改动集中在 discovery / mcps / dashboard 同一条后端聚合链路，拆并行会产生高耦合。

## 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| 主代理 | MCP discovery、路由聚合、前端最小可见性、验证、`docx/` | `backend/app/services/discovery.py`、`backend/app/routers/mcps.py`、`backend/app/routers/dashboard.py`、`src/pages/McpsPage.vue`、`README.md`、`docx/` | 本文档与既有批准基线 | 发现逻辑、验证结果、阶段文档 |

## 完成定义

1. `npm run build` 通过。
2. `GET /api/mcps` 可返回 discovered MCP 列表。
3. `GET /api/mcps/{id}` 返回 discovered MCP 详情，且 `source_kind=discovered`、`is_writable=false`。
4. `PUT` / `DELETE /api/mcps/{discovered_id}` 返回 `403 mcp_read_only`。
5. `GET /api/dashboard` 中 `cludea` / `opencode` 的 MCP 统计增加。
6. `GET /api/discovery` 中两者的 `discovered_mcp_files` 与 fixture 数量一致。

## 风险与待确认项

1. 真实第三方 MCP JSON 格式可能比当前 fixture 更复杂，本轮只能做最佳努力解析。
2. discovered MCP 进入 `/api/mcps` 后，Agents 页也会读取到这些 MCP；需要保证该变化不影响既有 managed 路径。
3. 本轮只补发现与只读展示，不代表外部 MCP 回写已完成。

## 交接输出

1. 允许实施阶段按 discovery / mcps / dashboard / MCP 页面最小可见性四块直接落地。
2. 允许测试阶段使用环境变量覆盖候选根目录并用临时 fixture 做真实 HTTP 验证。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-163234
- 备注：本轮为“外部 MCP 发现”增强切片，不新开需求与架构分叉。
