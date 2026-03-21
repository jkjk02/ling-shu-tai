# Monaco Editor 集成架构方案

- 阶段：02-architecture
- 提交时间：20260321-090750
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/01-requirements/20260321-090750-monaco-editor-integration-requirements.md

## 目标

1. 为 Monaco 集成选择最低风险、可复用的前端方案。
2. 明确组件边界、依赖和页面接入方式。

## 核心内容

## 方案比较

### 方案 A：每个页面各自直接初始化 Monaco

1. 做法
   - 在 `Skills`、`MCPs`、`Agents` 页面内分别写 `onMounted` / `watch`
2. 优点
   - 初期接入快
3. 缺点
   - 生命周期代码重复
   - worker、布局刷新和 `v-model` 逻辑分散，后续难维护

### 方案 B：抽取通用 `MonacoCodeEditor` 组件

1. 做法
   - 新增共享组件，封装：
     - editor 创建与销毁
     - `v-model` 同步
     - language 切换
     - 自动布局
     - readOnly / height 等基础选项
   - 页面只传值、语言和高度
2. 优点
   - 可复用、可控、后续更容易扩展到 Workflows 或其它编辑位
   - 页面改动量更小
3. 缺点
   - 需要先处理 Monaco worker 与组件封装

## 推荐方案

1. 采用方案 B。
2. 理由：
   - 当前有至少三个接入点，组件化收益已经大于一次性页面硬写。
   - 后续若继续把只读预览也升级为编辑器，可直接复用。

## 目标架构

1. 依赖层
   - 安装 `monaco-editor`
2. 组件层
   - 新增 `src/components/MonacoCodeEditor.vue`
   - 在组件内定义 Monaco worker 映射
   - 提供 `modelValue`、`language`、`height`、`readonly`、`minimap` 等基础 props
3. 页面层
   - `SkillsPage.vue`
   - `McpsPage.vue`
   - `AgentsPage.vue`

## 质量属性与取舍

1. 一致性：三处编辑体验统一。
2. 可维护性：Monaco 初始化逻辑收敛到一个组件。
3. 包体：接受一定增加，换取长文本编辑体验明显提升。

## 风险与待确认项

1. 如果 worker 配置不全，JSON 体验可能退化；优先保证 `json` 与基础编辑器 worker。
2. 弹窗首次打开时可能需要 `automaticLayout` 与 `nextTick` 共同保证尺寸正确。

## 交接输出

1. 允许计划阶段按“依赖 + 组件 + 三页接入”组织实施。
2. 要求实现阶段尽量不改动业务 API 和表单校验逻辑。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-090900
- 备注：采用共享 `MonacoCodeEditor` 组件方案。
