# 灵枢台

灵枢台是一个面向 Linux 的本地 Web 管理台，用来统一查看和维护 `codex`、`cludea`、`opencode` 等 CLI 工具的 Skills、MCPs、Agents 和 Workflows。

## 环境要求

1. Linux
2. Node.js 22+
3. npm
4. Python 3.12+
5. `python3-venv`

## 拉取代码

首次拉取：

```bash
git clone -b main git@github.com:jkjk02/ling-shu-tai.git
cd ling-shu-tai
```

已有仓库就更新：

```bash
git checkout main
git pull --ff-only origin main
```

## 安装依赖

```bash
npm ci
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install --upgrade pip
backend/.venv/bin/pip install -r backend/requirements.txt
```

## 启动

先启动后端：

```bash
backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --reload
```

再开一个终端启动前端：

```bash
npm run dev
```

浏览器访问：

```text
http://127.0.0.1:5173
```

## 更新后重新启动

```bash
git checkout main
git pull --ff-only origin main
npm ci
backend/.venv/bin/pip install -r backend/requirements.txt
```

然后重启后端和前端。
