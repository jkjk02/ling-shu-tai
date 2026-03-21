# 其他CLI外部Skill发现实施计划

- 阶段：03-plan
- 提交时间：20260320-161542
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/00-governance/20260320-155940-other-cli-external-skills-run-ledger.md
  - docx/01-requirements/20260320-142228-requirements-baseline-import.md
  - docx/02-architecture/20260320-142228-architecture-baseline-import.md
  - docx/07-delivery/20260320-155331-final-product-handoff.md

## 目标

1. 为“其他 CLI 外部 Skill 发现”切片建立单独实施计划。
2. 在不重复已完成 CRUD 的前提下，补齐 `cludea` / `opencode` 的 discovered skill 接入。
3. 明确本轮验证点与非范围，避免继续扩大切片。

## 核心内容

1. 基线沿用结论：
   - 不新增 `01-requirements` / `02-architecture` 文档。
   - 继续沿用 `docx/01-requirements/20260320-142228-requirements-baseline-import.md` 与 `docx/02-architecture/20260320-142228-architecture-baseline-import.md`。
2. 本轮范围：
   - 扩展 `backend/app/services/discovery.py`，让 `cludea` / `opencode` 在候选目录下也能发现外部 skill 文件。
   - 复用现有 `Skills` 路由与只读语义，不修改 managed CRUD 契约。
   - 复用 `Dashboard` / `Discovery` 统计链路，让 discovered skill 数量自动反映到现有页面。
3. 本轮非范围：
   - 不重复做 `Skills` / `MCPs` / `Agents` / `Workflows` 的 managed CRUD。
   - 不实现外部 MCP 详情读取、只读聚合和回写。
   - 不接入 `Monaco Editor`，不增强 `Workflows` 画布，不扩建自动化测试体系。
4. 推荐实现路径：
   - 在 `discovery.py` 内保留 Codex `SKILL.md` 专用解析。
   - 为 `cludea` / `opencode` 增加基于候选子目录的通用 skill 文件遍历与最佳努力解析。
   - 继续输出 `source_kind=discovered` 与 `is_writable=false`，保证只读保护沿用。
5. 并行拆分结论：
   - 不建议并行 worker。
   - 原因：核心改动集中在 discovery 单链路，拆分会造成同文件或强耦合写集冲突。

## 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| 主代理 | 后端 discovery、验证、`docx/` 文档 | `backend/app/services/discovery.py`、`docx/` | 本文档与既有批准基线 | 发现逻辑、验证结果、阶段文档 |

## 完成定义

1. `npm run build` 通过。
2. `GET /api/skills` 可返回 `cludea` / `opencode` discovered skills。
3. `GET /api/skills/{id}` 返回 discovered skill 详情，且 `source_kind=discovered`、`is_writable=false`。
4. `PUT` / `DELETE /api/skills/{discovered_id}` 返回 `403 skill_read_only`。
5. `GET /api/dashboard` 中 `cludea` / `opencode` 的 skill 统计增加。
6. `GET /api/discovery` 中两者的 `discovered_skill_files` 与实际 fixture/目录数量一致。

## 风险与待确认项

1. 当前环境没有真实 `~/.cludea` / `~/.opencode` 目录，验证需依赖临时 fixture。
2. 通用解析采用最佳努力策略，真实第三方格式若更复杂，后续仍可能需要针对性兼容。
3. 本轮只补 skill 发现，不代表外部 MCP 与编辑体验已闭环。

## 交接输出

1. 允许实施阶段直接修改 `backend/app/services/discovery.py`，不要求前端页面重构。
2. 允许测试阶段使用环境变量覆盖候选根目录并通过临时 fixture 做真实 HTTP 验证。

## 批准记录

- 评审人：Harvey / 主代理
- 评审结论：approved
- 批准时间：20260320-161542
- 备注：本轮为增强切片，不新开需求与架构分叉。
