# 实现记录

- 提交时间：2026-03-24 14:14:49 +0800
- 关联台账：`docx/00-governance/20260324-141449-main-branch-linux-web-run-ledger.md`

## 实施内容

1. 重写 `README.md`，改为 Linux Web 版本的项目介绍、启动方式、验证命令和 `main` 单分支约定。
2. 从 `package.json` 移除 `build:exe` 与 `build:windows-installers` 入口，避免继续暴露 Windows 打包链。
3. 调整 `.github/workflows/ci.yml`，只保留 `main` 的 `push` 和手动触发。
4. 删除未跟踪的 Windows 构建文件：
   - `.github/workflows/windows-exe.yml`
   - `launcher.py`
   - `scripts/` 下的打包脚本和缓存
   - `installer/windows/` 下的安装器定义文件
5. 补强 `README.md` 首屏内容，增加 GitHub 首页可直接阅读的拉取、初始化与启动说明。

## 验证计划

1. 运行 `npm run build`
2. 检查 Git 分支清理结果
3. 如可访问远端，则尝试删除额外 GitHub 分支，仅保留 `main`

## 实际验证结果

1. `npm run build`：通过
2. 本地分支：仅剩 `main`
3. 远端分支：已删除
   - `codex/windows-exe-linux-web`
   - `codex/windows-installers-20260324`
   - `codex/windows-installers-artifacts`
4. GitHub 仓库 `About`：已同步为 `Linux Web 控制台，用于统一管理本地 MCP、Agent、Skill 和 Workflow`
