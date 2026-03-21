# Codex外部Skill发现实现

- 阶段：04-implementation
- 提交时间：20260320-153601
- 责任角色：systems_implementer
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/03-plan/20260320-153601-codex-external-skills-plan.md

## 目标

1. 为 Codex 外部 Skills 补齐真实发现、解析与只读展示能力。
2. 让 `Skills`、`Dashboard`、`Discovery` 三个读取面都能反映 `/root/.codex/skills/*/SKILL.md`。
3. 保持 managed CRUD 路径不变，不让外部资源误入可写链路。

## 核心内容

1. 当前实现拆分：
   - 主代理：`docx/`、前端来源可见性、集成验证
   - worker `Hubble`：后端 discovery / skills / dashboard 聚合逻辑
2. 当前已完成进展：
   - `DiscoveryService` 已支持扫描 `codex` 候选根目录下的 `skills/**/SKILL.md`
   - 已补充轻量 front matter 解析，提取 `name`、`description`、`trigger_command`
   - discovered skill 已映射为与现有 `Skill` schema 兼容的只读资源
   - `GET /api/skills` 与 `GET /api/skills/{id}` 已支持 managed + discovered 聚合读取
   - discovered skill 的 `PUT` / `DELETE` 已返回 `403 skill_read_only`
   - Dashboard 的 skill 统计与 Discovery 的发现数量已反映真实 discovered skills
   - `SkillsPage.vue` 已补充来源文案与来源标签列
   - `npm run build` 已通过
   - 真实 HTTP 已通过 `/api/skills`、`/api/dashboard`、`/api/discovery` 验证

## 代码归属

| 责任方 | 文件 |
| --- | --- |
| 主代理 | `src/pages/SkillsPage.vue` |
| worker `Hubble` | `backend/app/services/discovery.py` |
| worker `Hubble` | `backend/app/routers/skills.py` |
| worker `Hubble` | `backend/app/routers/dashboard.py` |

## 预期验证

1. `npm run build`
2. 真实 HTTP 通过 `5173/api/skills` 验证 discovered skills 聚合列表与详情
3. 真实 HTTP 通过 `5173/api/dashboard` 和 `5173/api/discovery` 验证统计结果
4. 真实 HTTP 验证 discovered skill 的 `PUT` / `DELETE` 返回 `403 skill_read_only`

## 实际验证结果

1. `npm run build`：通过
2. 真实 HTTP `Skills / Dashboard / Discovery`：
   - `/skills -> 200, total=6`
   - discovered Codex skills：5 个
   - `/skills/{discovered_id} -> 200`
   - `/dashboard -> 200, total_skills=6, codex skills=6`
   - `/discovery -> 200, codex discovered_skill_files=5`
   - `PUT /skills/{discovered_id} -> 403, code=skill_read_only`
   - `DELETE /skills/{discovered_id} -> 403, code=skill_read_only`
3. 代表性 discovered skill：
   - `codex-discovered-system-openai-docs`
4. 验证路径：
   - `http://127.0.0.1:5173/api/skills`
   - `http://127.0.0.1:5173/api/dashboard`
   - `http://127.0.0.1:5173/api/discovery`

## 风险与待确认项

1. 当前 front matter 解析是轻量实现，只支持单行 `key: value`，不支持复杂 YAML。
2. discovered skill 的 `created_at` / `updated_at` 当前都基于文件 `mtime`，不代表严格创建时间。
3. 当前只覆盖 Codex `SKILL.md` 发现，未扩展到其他 CLI 工具或外部 MCP 解析。

## 交接输出

1. 交给评审阶段：
   - discovered / managed 边界是否清晰
   - 只读语义是否完整落地
   - 外部真实文件是否已被解析而不是静态 mock
2. 交给测试阶段：
   - 构建结果
   - `/skills`、`/skills/{id}`、`/dashboard`、`/discovery` 真实 HTTP 结果
   - discovered skill 的只读保护结果
3. 本阶段唯一上游输入文件：
   - `docx/03-plan/20260320-153601-codex-external-skills-plan.md`

## 批准记录

- 评审人：implementation_reviewer
- 评审结论：approved
- 批准时间：20260320-154652
- 备注：实现文档已补齐，代码与验证证据一致，允许进入测试阶段。
