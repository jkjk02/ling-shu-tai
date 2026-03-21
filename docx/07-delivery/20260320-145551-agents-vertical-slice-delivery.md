# Agents纵向切片交付

- 阶段：07-delivery
- 提交时间：20260320-145551
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/06-test/20260320-145551-agents-vertical-slice-test.md
  - docx/05-review/20260320-145551-agents-vertical-slice-review.md

## 目标

1. 输出本轮 `Agents` 纵向切片交付总结。
2. 给出当前本地成品的操作说明和剩余范围说明。

## 核心内容

# 交付摘要

- 最终状态：partial
- 交付时间：20260320-145551
- 目标达成情况：`Agents` 纵向切片已完成并通过本轮验证；整项目仍未达到最终完整版目标。

## 阶段完成情况

| 阶段 | 状态 | 关键输出 |
| --- | --- | --- |
| 01 需求 | done | 历史需求基线已导入并批准 |
| 02 架构 | done | 历史架构方案已导入并批准 |
| 03 计划 | done | `Agents` 纵向切片实施计划已批准 |
| 04 开发 | done | `Agents` CRUD 闭环已完成 |
| 05 评审 | done | 本轮实现评审通过 |
| 06 测试 | done | 构建与真实 HTTP 联调通过 |
| 07 交付 | done | 本地成品已更新 |

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
2. 当前可联调的数据文件位于：
   - `backend/data/skills.json`
   - `backend/data/mcps.json`
   - `backend/data/agents/agents.json`

### 常见操作

1. 打开 `Agents` 页面查看列表。
2. 点击“新建 Agent”创建代理配置。
3. 在表单中填写：
   - 名称
   - 描述
   - 主 CLI
   - System Prompt
   - 授权 Skills
   - 关联 MCP
   - Tool Scope
4. 在详情区查看已分配 Skill、关联 MCP 和系统提示词。

### 验证方式

1. 执行 `npm run build`
2. 通过 `http://127.0.0.1:5173/api/agents` 执行真实 HTTP CRUD 冒烟

### 已知限制

1. 当前未覆盖浏览器级手工交互记录。
2. 后端尚未对 `skill_ids`、`mcp_id` 做引用一致性校验。
3. `Workflows`、外部资源解析回写仍未补齐。
4. 本轮按用户要求未执行 Git 提交和推送。

## 风险与待确认项

1. 当前交付仍是阶段性成品，不是最终完整成品。
2. 下一轮优先级应转向 `Workflows`，否则平台的核心编排能力仍缺口较大。

## 交接输出

1. 用户当前可直接使用 `Skills`、`MCPs`、`Agents` 三个已闭环页面。
2. 下一轮应继续沿用 `docx/` 工作流推进 `Workflows` 与剩余未完成范围。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-145551
- 备注：本轮 `Agents` 已闭环，但整项目仍未最终完成。
