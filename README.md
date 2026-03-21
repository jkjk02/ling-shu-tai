# 灵枢台

灵枢台是一个面向 `codex`、`cludea`、`opencode` 的 AI Agent 与 CLI 工具链管理平台。

它提供：

1. Skills、MCPs、Agents、Workflows 的可视化管理界面
2. 本地 CLI 配置资源的自动发现与统一维护
3. Multi-Agent 协作流程的画布式编排能力

## 目录结构

- `doc/`：历史阶段文档
- `docx/`：当前多阶段交付文档与审批记录
- `backend/`：FastAPI 后端服务
- `src/`：Vue 3 前端源码
- `public/`：静态资源

## 本地启动

### 前端

1. 安装依赖：`npm install`
2. 启动开发服务器：`npm run dev`
3. 默认地址：`http://127.0.0.1:5173`

说明：

- Vite 已将 `/api` 代理到 `http://127.0.0.1:8000`
- 后端未启动时，前端会回退到本地示例数据并给出提示

### 后端

1. 若系统未启用 venv，请先安装 `python3.12-venv`
2. 创建项目内虚拟环境：`python3 -m venv backend/.venv`
3. 安装依赖：`backend/.venv/bin/pip install -r backend/requirements.txt`
4. 启动服务：`backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --reload`
5. 默认地址：`http://127.0.0.1:8000`

### 后端 API 自动化回归

1. 运行命令：`backend/.venv/bin/python -m unittest discover -s backend/tests`
2. 当前测试会自动：
   - 启动真实 `uvicorn` 服务
   - 使用临时数据目录，不污染仓库内 `backend/data`
   - 复制外部 Skill / MCP fixture 到临时目录，验证 discovered 发现与外部 MCP 回写链路
3. 当前覆盖边界：
   - `health`
   - `skills` / `mcps` / `agents` / `workflows`
   - `dashboard` / `discovery`
4. 当前未覆盖项：
   - 浏览器级交互与前端画布行为
   - CI 平台集成

### 浏览器级冒烟自动化

1. 运行命令：`npm run test:browser`
2. 当前测试会自动：
   - 启动真实后端 `uvicorn`
   - 启动前端 Vite 开发服务器，并通过 `/api` 代理访问后端
   - 打开 Chromium，验证 `Dashboard`、`Skills`、`Agents`、`Workflows` 页面可打开
   - 验证 `MCPs` 页面可见 discovered MCP 状态，并能打开“新建 MCP”对话框
3. 本机若已存在 Playwright Chromium 缓存，会直接复用；CI 需先执行 `npx playwright install chromium`
4. 当前覆盖边界：
   - 页面导航与主区域渲染
   - MCP 页面受支持 / 只读 discovered 资源状态展示
   - MCP 新建对话框基础可见性
5. 当前未覆盖项：
   - 复杂 CRUD 提交
   - 浏览器级 Workflow 画布拖拽
   - 视觉回归

### 统一验证入口

1. 后端语法校验：`npm run check:backend`
2. 后端自动化回归：`npm run test:backend`
3. 一体化验证：`npm run verify`
4. `npm run verify` 会顺序执行：
   - `npm run check:backend`
   - `npm run test:backend`
   - `npm run build`
   - `npm run test:browser`
5. 这些命令依赖项目内 `backend/.venv` 已按前文完成初始化

### CI 骨架

1. 仓库已提供 GitHub Actions 骨架：`.github/workflows/ci.yml`
2. 当前 CI 骨架覆盖：
   - `npm ci`
   - Python 3.12 环境准备
   - `backend/.venv` 创建与后端依赖安装
   - `npx playwright install chromium`
   - `npm run verify`
3. 当前目录不是 Git 仓库，且未连接真实 GitHub 远端，因此这里只是预置工作流文件，不代表已在线上流水线中实际触发

### Monaco Editor

1. `Skills` 的“脚本内容”已接入 Monaco，并会跟随脚本语言切换语言模式
2. `MCPs` 的“扩展参数 JSON”已接入 Monaco
3. `Agents` 的“System Prompt”已接入 Monaco
4. Monaco 当前主要提升长文本与 JSON 编辑体验，不改变现有保存接口和数据结构
5. 当前已按真实使用场景裁掉未使用的 `css/html/typescript` Monaco worker，减少无效构建负担

### 当前实现范围

1. 已完成前端管理台骨架、路由、页面占位与 API 接入层
2. 已补通 `Skills`、`MCPs`、`Agents`、`Workflows` 的列表、详情、新建、编辑、删除闭环
3. 已完成 FastAPI 应用工厂、健康检查、Dashboard/Discovery/四类资源基础 CRUD 路由
4. `Skills`、`MCPs` 写操作已具备重复创建冲突保护；不支持回写的外部资源继续保留只读保护
5. `Agents` 写操作已具备重复创建冲突保护，前端已支持 Skill 多选分配、MCP 关联与 Tool Scope 配置
6. `Workflows` 已支持更完整的编排体验，包括节点模板、缩放平移、自动布局、结构化节点配置、连线条件编辑、画布校验提示、保存与加载
7. 已支持从真实 Codex `SKILL.md` 以及 `cludea` / `opencode` 候选目录中的文本型 Skill 文件发现外部 Skills，并以只读资源方式展示到 `Skills`、`Dashboard`、`Discovery`
8. 已支持从 `cludea` / `opencode` 候选目录中的 JSON MCP 文件发现外部 MCPs，并对受支持的 JSON 对象文件提供创建、回写、删除闭环
9. 已完成项目内 JSON 示例数据与 managed 目录初始化
10. 已完成后端 API 自动化回归入口、浏览器级页面冒烟自动化、统一验证命令、GitHub Actions CI 骨架、Monaco 编辑体验升级与受限范围内的外部 MCP 回写；真实远端 CI 落地和更复杂外部 MCP 方言适配仍未完成

## 何时使用

当你需要集中管理多个 CLI 工具的技能、模型配置和多智能体工作流时，使用灵枢台。

## 何时不使用

如果你只需要编辑单个工具的本地配置文件，且不需要可视化管理与工作流编排，则没有必要引入灵枢台。
