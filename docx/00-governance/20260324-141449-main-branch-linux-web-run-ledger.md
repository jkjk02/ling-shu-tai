# 运行台账

- 提交时间：2026-03-24 14:14:49 +0800
- 模式：Lite Path
- 负责人：主代理 Codex
- 任务：收敛仓库为 `main` 单主线，移除 Windows 打包链，并重写 `README.md` 为 Linux Web 使用说明

## 关键决策

1. 不升级为 Full Path，本轮属于仓库整理与文档修订。
2. 保留当前 Linux Web 运行形态，不再保留 Windows 安装器和可执行包入口。
3. GitHub 分支目标状态为仅保留 `main`，本地与远端分支分别清理。

## 执行边界

1. 更新 `README.md`、`package.json`、`.github/workflows/ci.yml`
2. 删除未纳入版本管理的 Windows 打包脚本、工作流和安装器文件
3. 补充最小实现记录和交付摘要
