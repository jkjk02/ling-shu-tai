# Codex外部Skill发现实施计划

- 阶段：03-plan
- 提交时间：20260320-153601
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/00-governance/20260320-153710-external-skills-run-ledger.md
  - docx/02-architecture/20260320-142228-architecture-baseline-import.md
  - docx/07-delivery/20260320-151548-workflows-vertical-slice-delivery.md

## 目标

1. 为 Codex 外部 Skills 补齐真实发现、解析与只读展示能力。
2. 让平台的 `Skills`、`Dashboard`、`Discovery` 能反映 `/root/.codex/skills/*/SKILL.md` 的真实存在。
3. 在不破坏现有 managed CRUD 的前提下，完成 discovered + managed 的统一读取闭环。

## 核心内容

### 方案比较

1. 路径 A：启动时把 discovered skills 导入 `backend/data/skills.json`
   - 优点：复用现有 `ResourceService` 与 CRUD 路径，改动面小。
   - 缺点：会污染 managed 数据文件；外部文件变化无法实时反映；读写边界混乱，容易把外部资源误当成本地可写资源。
2. 路径 B：请求时动态扫描外部目录并与 managed 数据做聚合返回
   - 优点：保持 managed / discovered 边界清晰；外部文件变化可直接反映；天然支持 `is_writable=false` 只读语义。
   - 缺点：需要新增解析和聚合逻辑，读取路径比纯仓储稍复杂。
3. 本轮推荐：路径 B。
   - 理由：本轮目标是“发现与只读展示”，不是“导入外部资源后本地接管”；动态聚合更符合需求基线中的“外部文件解析与 managed 兜底保存”。

### 本轮范围

1. 发现 `/root/.codex/skills/*/SKILL.md` 形式的外部 Skill。
2. 解析 front matter 中的 `name`、`description`，并提取 Markdown 正文。
3. 为 discovered skill 生成与 `Skill` schema 兼容的只读记录：
   - `source_kind=discovered`
   - `is_writable=false`
   - `source_path` 指向真实文件
4. `GET /api/skills`、`GET /api/skills/{id}` 返回 managed + discovered 聚合结果。
5. Dashboard 的 skill 数量与 Discovery 的发现统计反映真实 discovered skills。
6. 前端 `Skills` 页面补充来源可见性，避免用户误把 discovered skill 当成可写资源。

### 不在本轮范围

1. 外部 Skill 的回写或覆盖保存。
2. `MCPs` 的真实外部文件解析。
3. Monaco Editor 接入。
4. 完整端到端自动化测试框架建设。

## 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| worker-backend | `backend/app/services/discovery.py`、`backend/app/routers/skills.py`、`backend/app/routers/dashboard.py` | 仅后端发现、解析、聚合与统计 | 本文档 | Codex discovered skills 聚合读取能力 |
| worker-frontend | `src/pages/SkillsPage.vue` | 仅前端来源展示与文案 | 本文档 | discovered / managed 来源可见性 |

## 完成定义

1. `GET /api/skills` 至少返回 2 个来自 `/root/.codex/skills` 的 discovered skills。
2. `GET /api/skills/{id}` 可读取 discovered skill 详情，并返回 `is_writable=false`。
3. `GET /api/dashboard` 中 Codex 的 `skillCount` 包含 discovered skills。
4. `GET /api/discovery` 中 Codex 的 `discovered_skill_files` 反映真实发现数量，而不是固定为 0。
5. 前端 `Skills` 列表与详情能区分 managed / discovered 来源。
6. `npm run build` 通过。
7. 真实 HTTP 至少验证：
   - `GET /api/skills`
   - `GET /api/skills/{discovered_id}`
   - `GET /api/dashboard`
   - `GET /api/discovery`

## 风险与待确认项

1. `SKILL.md` 的元数据格式不是严格 JSON，需要采用最佳努力解析；异常文件不能拖垮整体列表接口。
2. discovered skills 的唯一 ID 必须稳定，避免与 managed skills 冲突。
3. 动态扫描会引入轻微读取开销，但本轮发现数量很小，可接受。

## 交接输出

1. 开发阶段以本文件作为唯一实施拆分依据。
2. 评审阶段重点核对：
   - discovered 与 managed 边界是否清晰
   - 只读语义是否落地
   - 真实外部源是否被实际解析，而不是静态 mock

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-153601
- 备注：批准进入 Codex 外部 Skill 发现切片开发。
