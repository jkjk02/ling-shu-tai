# 统一验证命令与 CI 接入交付摘要

- 阶段：07-delivery
- 提交时间：20260321-085515
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/06-test/20260321-085515-unified-verification-and-ci-test.md
  - docx/05-review/20260321-085515-unified-verification-and-ci-review.md

## 目标

1. 固化“统一验证命令与 CI 接入”切片的交付结果。
2. 给后续会话提供新的自动化与 CI 基线。

## 核心内容

## 交付结果

1. 本地统一验证入口已完成：
   - `npm run check:backend`
   - `npm run test:backend`
   - `npm run verify`
2. 仓库已新增 GitHub Actions 骨架：
   - `.github/workflows/ci.yml`
3. 统一入口已实测通过：
   - `npm run verify`
   - 内含 `backend` 语法校验、后端回归、前端构建

## 阶段完成情况

| 阶段 | 状态 | 关键输出 |
| --- | --- | --- |
| 00 治理 | done | CI 接入切片运行台账 |
| 01 需求 | done | 统一验证命令与 CI 需求基线已批准 |
| 02 架构 | done | 采用“本地脚本 + GitHub Actions 骨架”方案 |
| 03 计划 | done | 写边界与验证计划已批准 |
| 04 开发 | done | `package.json`、CI 文件、README 已更新 |
| 05 评审 | done | 实现通过评审 |
| 06 测试 | done | `npm run verify` 通过 |
| 07 交付 | done | 本摘要与新 handoff 可交付 |

## 操作说明书

### 启动

1. 前端：`npm run dev`
2. 后端：`backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --reload`

### 配置

1. 使用统一验证入口前，需先按 README 初始化 `backend/.venv`
2. 远端 CI 若在 GitHub 上启用，将自动创建项目内 `backend/.venv`

### 常见操作

1. 仅后端语法校验：`npm run check:backend`
2. 仅后端回归：`npm run test:backend`
3. 完整验证：`npm run verify`

### 验证方式

1. 观察 `npm run verify` 是否依次完成：
   - `check:backend`
   - `test:backend`
   - `build`
2. 观察 `test:backend` 是否输出 `Ran 6 tests` 与 `OK`

### 已知限制

1. GitHub Actions 目前只是仓库内骨架，未在真实远端仓库触发
2. 当前统一验证仍未覆盖浏览器交互自动化
3. 当前目录仍不是 Git 仓库

## 风险与待确认项

1. 当前项目已从“有自动化测试但无统一入口”提升到“有统一入口和 CI 骨架”，但仍未达到真实远端 CI 上线状态。
2. 后续若继续推进，优先级应转向浏览器冒烟自动化或把 CI 真正接入远端仓库。

## 交接输出

1. 本轮切片已完成交付。
2. 应生成新的 current handoff，作为下一会话入口。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-085650
- 备注：统一验证命令与 CI 接入切片已完成交付。
