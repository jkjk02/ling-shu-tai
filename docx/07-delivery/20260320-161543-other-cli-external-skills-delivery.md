# 其他CLI外部Skill发现交付

- 阶段：07-delivery
- 提交时间：20260320-161543
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/06-test/20260320-161543-other-cli-external-skills-test.md
  - docx/05-review/20260320-161543-other-cli-external-skills-review.md

## 目标

1. 输出本轮“其他 CLI 外部 Skill 发现”增强切片交付总结。
2. 明确当前成品新增能力、验证方式与剩余限制。

## 核心内容

# 交付摘要

- 最终状态：partial
- 交付时间：20260320-161543
- 目标达成情况：平台已补齐 `cludea` / `opencode` 的外部 skill 发现能力，并纳入现有 `Skills`、`Dashboard`、`Discovery` 与只读保护链路；整项目仍未达到最终完整版目标。

## 阶段完成情况

| 阶段 | 状态 | 关键输出 |
| --- | --- | --- |
| 00 治理 | done | 新一轮其他 CLI 外部 Skill 发现台账已建立 |
| 03 计划 | done | 仅做 discovery 增强、禁止重复 CRUD 的实施计划已批准 |
| 04 开发 | done | `cludea` / `opencode` discovered skill 发现逻辑已接入 |
| 05 评审 | done | 范围边界与只读语义评审通过 |
| 06 测试 | done | 构建、py_compile 与真实 HTTP 通过 |
| 07 交付 | done | 切片交付与操作说明已更新 |

## 操作说明书

### 启动

1. 前端：
   - `cd /home/lst/ling-shu-tai`
   - `npm run dev`
2. 后端：
   - `cd /home/lst/ling-shu-tai`
   - `backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000`

### 配置

1. `cludea` 候选根目录：
   - `$LINGSHU_CLUDEA_ROOT`
   - `~/.cludea`
   - `~/.config/cludea`
   - `~/.claude`
   - `~/.config/claude`
2. `opencode` 候选根目录：
   - `$LINGSHU_OPENCODE_ROOT`
   - `~/.opencode`
   - `~/.config/opencode`
3. 发现逻辑会扫描：
   - `skills/`
   - `commands/`
   - `prompts/skills/`

### 常见操作

1. 打开 `Skills` 页面。
2. 通过 CLI 过滤器查看 `cludea` 或 `opencode`。
3. 点击 discovered skill 查看详情、来源路径和正文内容。
4. discovered skill 继续保持只读，不能编辑或删除。
5. 打开 Dashboard 与 Discovery 查看最新发现统计。

### 验证方式

1. 执行 `npm run build`
2. 执行 `backend/.venv/bin/python -m py_compile backend/app/main.py backend/app/config.py backend/app/services/discovery.py backend/app/routers/skills.py backend/app/routers/dashboard.py backend/app/routers/discovery.py`
3. 通过真实 HTTP 验证：
   - `GET /api/skills`
   - `GET /api/skills/{id}`
   - `PUT /api/skills/{discovered_id}`
   - `DELETE /api/skills/{discovered_id}`
   - `GET /api/dashboard`
   - `GET /api/discovery`

### 已知限制

1. 当前只补齐了 `cludea` / `opencode` 的外部 skill 发现，不包含外部 MCP 详情与回写。
2. 通用解析是最佳努力实现，真实第三方文件格式若更复杂仍需继续兼容。
3. `Monaco Editor`、完整工作流画布体验和自动化测试体系仍未完成。
4. 当前目录不是 Git 仓库，本轮未执行提交和推送。

## 风险与待确认项

1. 当前交付仍是阶段性增强切片，不是最终完整成品。
2. 下一轮优先级可在“外部 MCP 解析 / Monaco / 自动化测试”之间继续排序，但不应回头重复已完成 CRUD。

## 交接输出

1. 用户现在可以在平台中看到来自 `cludea` / `opencode` 的 discovered skills，并沿用既有只读保护。
2. 后续若继续沿用 `docx/` 工作流，应以本交付文档和 `docx/07-delivery/20260320-155331-final-product-handoff.md` 作为最近一轮增强基线输入。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-161543
- 备注：本轮交付只关闭“其他 CLI 外部 Skill 发现”切片，整项目继续保持 partial 状态。
