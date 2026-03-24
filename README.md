# 灵枢台

灵枢台是一个面向 Linux 的本地 Web 管理台，用来统一查看和维护 `codex`、`cludea`、`opencode` 等 CLI 工具的 Skills、MCPs、Agents 和 Workflows。

这个仓库现在只保留一条可用主线：

1. Git 只保留 `main`
2. 交付形态只保留 Linux Web
3. 不再提供 Windows 安装器、便携包和相关说明

## GitHub 首页先看这里

如果你只是想先把项目跑起来，按这 3 步做：

```bash
git clone -b main git@github.com:jkjk02/ling-shu-tai.git
cd ling-shu-tai
npm ci
python3 -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --reload
```

再开一个终端执行：

```bash
npm run dev
```

浏览器打开：

```text
http://127.0.0.1:5173
```

如果你是部署到 Linux 机器上，不做开发，就看下面的“方式 2：构建后运行”。

## 这个项目能做什么

1. 管理 `Skills`、`MCPs`、`Agents`、`Workflows`
2. 自动发现本机已有的 CLI 配置资源
3. 区分可写资源和只读资源
4. 通过 Web 画布编排多 Agent 工作流

## 仓库结构

- `backend/`：FastAPI 后端
- `src/`：Vue 3 前端
- `public/`：静态资源
- `tests/`：回归测试和浏览器冒烟测试
- `docx/`：交付记录

## 环境要求

必须满足：

1. Linux
2. Node.js 22 或更高版本
3. npm
4. Python 3.12 或更高版本
5. `python3-venv`

如果要跑浏览器测试，还需要：

1. Chromium
2. Playwright 依赖

## 先拉代码

首次获取项目：

```bash
git clone -b main git@github.com:jkjk02/ling-shu-tai.git
cd ling-shu-tai
```

如果你已经有仓库，只需要更新到最新 `main`：

```bash
git checkout main
git pull --ff-only origin main
```

## 第一次初始化

第一次在机器上运行，按下面顺序做：

```bash
npm ci
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install --upgrade pip
backend/.venv/bin/pip install -r backend/requirements.txt
```

完成后，前端依赖和后端虚拟环境就准备好了。

## 使用方式

### 方式 1：开发环境

适合改代码、看实时刷新、联调前后端。

1. 启动后端：

```bash
backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --reload
```

2. 另开一个终端，启动前端：

```bash
npm run dev
```

3. 打开浏览器：

```text
http://127.0.0.1:5173
```

说明：

1. Vite 会把 `/api` 代理到 `http://127.0.0.1:8000`
2. 前端热更新只在这个模式下可用
3. 后端没启动时，前端会退回到本地示例数据

### 方式 2：构建后运行

适合 Linux 本机直接作为 Web 服务使用，不需要前端开发服务器。

1. 先构建前端：

```bash
npm run build
```

2. 启动后端：

```bash
backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```

3. 浏览器访问：

```text
http://127.0.0.1:8000
```

说明：

1. 只要根目录有 `dist/`，FastAPI 就会直接托管前端静态资源
2. 如果你只在本机访问，也可以把 `--host 0.0.0.0` 换成默认值

### 方式 3：更新后重新启动

服务器或本地环境更新代码时，推荐这样做：

```bash
git checkout main
git pull --ff-only origin main
npm ci
backend/.venv/bin/pip install -r backend/requirements.txt
npm run build
```

然后重启后端进程即可。

## 常用命令

启动开发前端：

```bash
npm run dev
```

构建前端：

```bash
npm run build
```

后端语法检查：

```bash
npm run check:backend
```

后端回归：

```bash
npm run test:backend
```

浏览器冒烟：

```bash
npm run test:browser
```

完整验证：

```bash
npm run verify
```

`npm run verify` 会顺序执行：

1. `npm run check:backend`
2. `npm run test:backend`
3. `npm run build`
4. `npm run test:browser`

## 不同场景怎么用

日常开发：

1. 用“方式 1：开发环境”
2. 一个终端跑后端，一个终端跑前端

本机交付或内网部署：

1. 用“方式 2：构建后运行”
2. 只启动 FastAPI
3. 由 FastAPI 直接提供 Web 页面

代码更新：

1. 用“方式 3：更新后重新启动”
2. 永远以 `main` 为准

## Git 约定

1. 默认只使用 `main`
2. 提交、发布、CI 都以 `main` 为准
3. `.github/workflows/ci.yml` 当前只在 `main` 的 `push` 和手动触发时运行

## 适用场景

当你需要用一个 Linux Web 界面集中管理多套 AI CLI 配置和工作流时，使用灵枢台。

如果你只是手工编辑单个配置文件，不需要可视化界面和流程编排，就没必要用这个项目。
