# 其他CLI外部Skill发现实现记录

- 阶段：04-implementation
- 提交时间：20260320-161543
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/03-plan/20260320-161542-other-cli-external-skills-plan.md
  - docx/00-governance/20260320-155940-other-cli-external-skills-run-ledger.md

## 目标

1. 按计划补齐 `cludea` / `opencode` 的外部 skill 发现能力。
2. 不破坏既有 Codex discovered skill 与 managed skill 行为。

## 核心内容

1. 实现文件：
   - `backend/app/services/discovery.py`
2. 主要实现点：
   - 保留 Codex `SKILL.md` 专用解析链路。
   - 为非 Codex CLI 增加通用外部 skill 文件发现逻辑，覆盖 `skills/`、`commands/`、`prompts/skills/` 等候选子目录。
   - 增加基于 Markdown front matter / JSON 内容的最佳努力元数据抽取。
   - 对 discovered skill 继续输出 `source_kind=discovered`、`is_writable=false`、`source_path`、`script_content`、`script_language`。
   - 让 `scan()`、`merge_skills()`、`count_skills_by()` 可将 `cludea` / `opencode` 的发现结果纳入现有统计链路。
3. 本轮未修改内容：
   - 前端页面未重构。
   - `Skills` / `MCPs` / `Agents` / `Workflows` managed CRUD 未重复实现。
   - 外部 MCP 详情读取与回写未进入本轮。
4. 自检结果：
   - `backend/.venv/bin/python -m py_compile ...` 通过。
   - `npm run build` 通过。

## 风险与待确认项

1. 当前通用解析是最佳努力实现，名称与触发命令仍可能受真实文件命名风格影响。
2. 由于没有真实用户目录，本轮对 `cludea` / `opencode` 的验证来自临时 fixture。
3. 当前目录不是 Git 仓库，无法提供提交哈希作为实现版本锚点。

## 交接输出

1. 评审阶段应重点检查：
   - 是否仅触及 discovery 链路
   - 是否保持 discovered 只读语义
   - 是否未回归既有 Codex discovered skill 行为
2. 测试阶段应使用临时目录覆盖：
   - `LINGSHU_CLUDEA_ROOT`
   - `LINGSHU_OPENCODE_ROOT`

## 批准记录

- 评审人：implementation_reviewer / 主代理
- 评审结论：approved
- 批准时间：20260320-161543
- 备注：`05-review` 已确认实现边界符合计划，允许进入测试并交付。
