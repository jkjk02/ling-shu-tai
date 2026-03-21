# MCPs纵向切片交付

- 阶段：07-delivery
- 提交时间：20260320-142911
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/06-test/20260320-142911-mcps-vertical-slice-test.md
  - docx/05-review/20260320-142911-mcps-vertical-slice-review.md

## 目标

1. 输出本轮 `MCPs` 纵向切片交付总结。
2. 给出本地可执行的操作说明书。

## 核心内容

# 交付摘要

- 最终状态：partial
- 交付时间：20260320-142911
- 目标达成情况：`MCPs` 纵向切片已完成并通过本轮验证；整项目仍未达到最终完整版目标。

## 阶段完成情况

| 阶段 | 状态 | 关键输出 |
| --- | --- | --- |
| 01 需求 | done | 历史需求基线已导入并批准 |
| 02 架构 | done | 历史架构方案已导入并批准 |
| 03 计划 | done | `MCPs` 纵向切片实施计划已批准 |
| 04 开发 | done | `MCPs` CRUD 闭环已完成 |
| 05 评审 | done | 本轮实现评审通过 |
| 06 测试 | done | 构建与进程内冒烟通过 |
| 07 交付 | done | 本地成品已更新 |

## 操作说明书

### 启动

1. 前端：
   - `cd /home/lst/ling-shu-tai`
   - `npm run dev`
2. 后端：
   - `cd /home/lst/ling-shu-tai`
   - `backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --reload`

### 配置

1. 前端默认通过 `/api` 访问后端。
2. 后端数据文件位于：
   - `backend/data/skills.json`
   - `backend/data/mcps.json`
   - `backend/data/agents/agents.json`
   - `backend/data/workflows/workflows.json`

### 常见操作

1. 打开 `MCPs` 页面查看列表。
2. 点击“新建 MCP”创建模型配置。
3. 在详情区查看来源路径、专属参数和扩展参数 JSON。
4. 对可写记录执行编辑或删除。

### 验证方式

1. 执行 `npm run build`
2. 使用 `PYTHONPATH=backend backend/.venv/bin/python` 直接调用 `app.routers.mcps` 相关函数做进程内冒烟

### 已知限制

1. 当前未完成真实 HTTP 黑盒验证。
2. 当前未完成浏览器级手工验证记录。
3. `Agents`、`Workflows`、外部资源解析回写仍未补齐。
4. 本轮按用户要求未执行 Git 提交和推送。

## 风险与待确认项

1. 当前交付是阶段性成品，不是最终完整成品。
2. 下一轮若继续推进，优先建议补 `Agents` 或 `Workflow`。

## 交接输出

1. 用户可以直接使用当前本地成品继续体验 `Skills` 和 `MCPs` 两个已闭环页面。
2. 后续阶段建议继续沿用 `docx/` 工作流，而不是回退到无阶段留痕模式。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-142911
- 备注：按用户要求仅做本地交付，不做 GitLab 推送。
