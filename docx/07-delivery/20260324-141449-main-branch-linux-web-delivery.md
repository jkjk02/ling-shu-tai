# 交付摘要

- 提交时间：2026-03-24 14:14:49 +0800
- 关联实现：`docx/04-implementation/20260324-141449-main-branch-linux-web-implementation.md`

## 本轮结果

1. 仓库说明已收敛为 Linux Web 使用方式。
2. Windows 打包相关入口与未跟踪文件已移除。
3. CI 触发策略已对齐 `main` 单主线。
4. GitHub 与本地仓库的额外分支已清理，当前仅保留 `main`。
5. GitHub 首页 README 已补齐拉取、初始化、开发运行和部署运行说明。
6. GitHub 仓库右侧 `About` 简介已更新为 Linux Web 版本描述。

## 使用入口

1. 开发：`npm run dev` + `backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --reload`
2. 构建后运行：`npm run build` + `backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend`

## 已知限制

1. `npm run build` 虽已通过，但 Vite 仍提示 Monaco 相关产物体积较大；这属于现有前端打包体积问题，不影响本轮 Linux Web 交付。
