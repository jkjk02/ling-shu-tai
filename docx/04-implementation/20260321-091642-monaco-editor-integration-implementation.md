# Monaco Editor 集成实现记录

- 阶段：04-implementation
- 提交时间：20260321-091642
- 责任角色：systems_implementer
- 当前状态：done
- 评审状态：pending
- 输入依据：
  - docx/03-plan/20260321-090750-monaco-editor-integration-plan.md

## 目标

1. 引入 Monaco 依赖并实现共享编辑器组件。
2. 在 `Skills`、`MCPs`、`Agents` 三页接入 Monaco。
3. 保持现有表单模型和保存链路不变。

## 核心内容

1. 依赖与组件
   - 安装 `monaco-editor`
   - 新增 `src/components/MonacoCodeEditor.vue`
   - 在组件内封装：
     - worker 映射
     - `v-model` 同步
     - `language` 切换
     - `blur` / `change` 事件
     - 自动布局与基础样式
2. 页面接入
   - `src/pages/SkillsPage.vue`
     - 脚本内容改为 Monaco
     - `bash -> shell`、`text -> plaintext` 语言映射
   - `src/pages/McpsPage.vue`
     - 扩展参数 JSON 改为 Monaco
   - `src/pages/AgentsPage.vue`
     - System Prompt 改为 Monaco
3. 构建修正
   - 首轮构建暴露 Monaco 类型入口和 CSS 路径问题，已修正为 ESM 窄入口 + `min/vs/editor/editor.main.css`
   - 首轮使用顶层 `monaco-editor` 入口导致构建 OOM，已回退到窄入口并补类型声明
4. 文档更新
   - README 新增 Monaco 说明
   - `src/env.d.ts` 补 Monaco ESM 入口声明

## 代码归属

1. 主代理
   - `package.json`
   - `src/components/MonacoCodeEditor.vue`
   - `src/pages/SkillsPage.vue`
   - `src/pages/McpsPage.vue`
   - `src/pages/AgentsPage.vue`
   - `src/env.d.ts`
   - `README.md`
   - `docx/`

## 验证方式

1. `npm run build`

## 风险与待确认项

1. Monaco 明显增大了前端产物体积，构建产物中会新增多个 worker chunk。
2. 当前虽已解决构建 OOM，但包体警告仍存在，后续可考虑更细粒度的懒加载或 worker 优化。
3. 本轮未增加浏览器层回归验证，Monaco 的交互体验仍主要依赖人工使用确认。

## 交接输出

1. 允许进入实现评审阶段。
2. 评审阶段重点检查是否真正复用共享组件、是否三处接入、是否未改后端协议。

## 批准记录

- 评审人：待评审
- 评审结论：pending
- 批准时间：
- 备注：实现已完成，等待 Stage 5 评审。
