# Codex外部Skill发现交付

- 阶段：07-delivery
- 提交时间：20260320-153601
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/06-test/20260320-153601-codex-external-skills-test.md
  - docx/05-review/20260320-153601-codex-external-skills-review.md

## 目标

1. 输出本轮 Codex 外部 Skill 发现切片交付总结。
2. 给出当前本地成品的操作说明和剩余限制说明。

## 核心内容

# 交付摘要

- 最终状态：partial
- 交付时间：20260320-154652
- 目标达成情况：平台已支持从真实 `/root/.codex/skills/*/SKILL.md` 发现 Codex 外部 Skills，并以只读资源方式在 `Skills`、`Dashboard`、`Discovery` 中展示；整项目仍未达到最终完整版目标。

## 阶段完成情况

| 阶段 | 状态 | 关键输出 |
| --- | --- | --- |
| 00 治理 | done | 新一轮外部 Skill 发现台账已建立 |
| 03 计划 | done | Codex 外部 Skill 发现实施计划已批准 |
| 04 开发 | done | discovered skill 聚合读取与只读保护已完成 |
| 05 评审 | done | 评审通过 |
| 06 测试 | done | 构建、真实 HTTP 与 managed 回归通过 |
| 07 交付 | done | 阶段性交付说明已更新 |

## 操作说明书

### 启动

1. 前端：
   - `cd /home/lst/ling-shu-tai`
   - `npm run dev`
2. 后端：
   - `cd /home/lst/ling-shu-tai`
   - `backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000`

### 配置

1. 前端默认通过 `/api` 访问后端。
2. Codex 外部 Skill 默认从以下候选根目录发现：
   - `$LINGSHU_CODEX_ROOT`
   - `~/.codex`
   - `~/.config/codex`
3. 本轮验证使用的真实外部源位于：
   - `/root/.codex/skills/`

### 常见操作

1. 打开 `Skills` 页面查看列表。
2. 使用“来源”列区分 `managed` 与 `discovered`。
3. 点击 discovered skill 查看详情、来源路径和正文内容。
4. 对 discovered skill 不能编辑或删除；对应操作会被后端拒绝。
5. 对 managed skill 仍可正常新建、编辑、删除。

### 验证方式

1. 执行 `npm run build`
2. 通过 `http://127.0.0.1:5173/api/skills` 验证 discovered skills 列表与详情
3. 通过 `http://127.0.0.1:5173/api/dashboard` 与 `http://127.0.0.1:5173/api/discovery` 验证统计
4. 通过 `PUT` / `DELETE /api/skills/{discovered_id}` 验证 `403 skill_read_only`

### 已知限制

1. 当前只支持 Codex `SKILL.md` 发现，未扩展到其他工具。
2. front matter 解析是轻量实现，只支持简单单行 `key: value`。
3. discovered skill 的时间戳基于文件 `mtime`。
4. `Monaco`、其他工具外部解析、外部 MCP 解析和自动化测试仍未补齐。
5. 当前目录仍不是 Git 仓库，本轮未执行提交和推送。

## 风险与待确认项

1. 当前交付仍是阶段性成品，不是最终完整成品。
2. 下一轮应优先扩展其他工具外部解析或补齐编辑体验与自动化测试，否则平台的“统一管理”能力仍不完整。

## 交接输出

1. 用户当前可在平台中看到真实 Codex discovered skills，并安全地区分只读与可写资源。
2. 后续若继续沿用 `docx/` 流程，应以本交付文档作为最新已批准的增强切片基线。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-154652
- 备注：Codex 外部 Skill 发现切片已闭环，整项目继续保持阶段性交付状态。
