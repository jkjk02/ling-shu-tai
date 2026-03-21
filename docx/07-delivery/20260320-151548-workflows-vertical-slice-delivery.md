# Workflows纵向切片交付

- 阶段：07-delivery
- 提交时间：20260320-151548
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/06-test/20260320-151548-workflows-vertical-slice-test.md
  - docx/05-review/20260320-151548-workflows-vertical-slice-review.md

## 目标

1. 输出本轮 `Workflows` 纵向切片交付总结。
2. 给出当前本地成品的操作说明和剩余限制说明。

## 核心内容

# 交付摘要

- 最终状态：partial
- 交付时间：20260320-152728
- 目标达成情况：`Workflows` 纵向切片已完成并通过本轮验证；当前项目已补齐 `Skills`、`MCPs`、`Agents`、`Workflows` 四类资源的可视化管理与最小工作流编排能力，但仍未达到最终完整版目标。

## 阶段完成情况

| 阶段 | 状态 | 关键输出 |
| --- | --- | --- |
| 01 需求 | done | 历史需求基线已导入并批准 |
| 02 架构 | done | 历史架构方案已导入并批准 |
| 03 计划 | done | `Workflows` 纵向切片实施计划已批准 |
| 04 开发 | done | `Workflows` CRUD 与最小编排闭环已完成 |
| 05 评审 | done | 本轮实现评审通过 |
| 06 测试 | done | 构建与真实 HTTP 联调通过 |
| 07 交付 | done | 本地成品与交付说明已更新 |

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
   - `backend/data/workflows/workflows.json`

### 常见操作

1. 打开 `Workflows` 页面查看已有流程。
2. 点击“新建 Workflow”创建新的编排草稿。
3. 在“流程元数据”中填写名称、描述和缩放。
4. 在画布区新增节点，拖拽节点位置，并在节点编辑区绑定 `Agent`。
5. 在连线编辑区新增或删除边，填写连线标签。
6. 点击“保存 Workflow”持久化；点击“删除当前”删除当前流程。

### 验证方式

1. 执行 `npm run build`
2. 通过 `http://127.0.0.1:5173/api/workflows` 执行真实 HTTP CRUD 冒烟

### 已知限制

1. 当前工作流画布是最小实现，未接入完整 `Vue Flow` 体验。
2. 当前未覆盖浏览器级手工拖拽与复杂交互的自动化测试。
3. 后端未对节点引用的 `agent_id` 做一致性校验。
4. `Monaco` 编辑器、真实外部文件格式解析与自动化测试仍未补齐。
5. 当前目录仍不是 Git 仓库，本轮未执行提交和推送。

## 风险与待确认项

1. 当前交付仍是阶段性成品，不是最终完整成品。
2. 下一轮优先级应转向补齐 `Monaco`、真实外部文件解析与自动化测试，否则产品完成度仍受限。

## 交接输出

1. 用户当前可直接使用 `Skills`、`MCPs`、`Agents`、`Workflows` 四个已闭环页面。
2. 后续若继续沿用 `docx/` 流程，应以本交付文档作为最新已批准交付基线。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-152728
- 备注：`Workflows` 纵向切片已闭环，整项目进入增强项收尾阶段。
