# Monaco Editor 集成需求基线

- 阶段：01-requirements
- 提交时间：20260321-090750
- 责任角色：requirements_analyst
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/00-governance/20260321-090750-monaco-editor-integration-run-ledger.md

## 目标

1. 为脚本、JSON 和 Prompt 提供更适合长文本编辑的 Monaco 编辑体验。
2. 在不改动现有表单提交流程的前提下，提升可读性、缩进与格式编辑能力。
3. 保持当前 CRUD 流程、校验和数据模型不变。

## 核心内容

## 功能模型

1. `Skills`
   - “脚本内容”输入区升级为 Monaco
   - 根据 `scriptLanguage` 切换语言模式
2. `MCPs`
   - “扩展参数 JSON” 输入区升级为 Monaco
   - 语言模式固定为 JSON
3. `Agents`
   - “System Prompt” 输入区升级为 Monaco
   - 语言模式固定为 Markdown 或 Plain Text 风格
4. 通用编辑能力
   - 支持长文本滚动、行号、基础语法高亮和自动布局
   - 支持 `v-model` 风格双向绑定，兼容现有表单模型

## 行为模型

1. 打开新建/编辑弹窗时，Monaco 应根据已有值初始化内容
2. 用户修改内容后，表单模型应实时更新
3. 切换 `scriptLanguage` 时，`Skills` 编辑器语言应同步切换
4. 关闭弹窗后重新打开，不应残留旧实例导致错位或空白

## 数据模型

1. 前端表单字段保持不变：
   - `formModel.scriptContent`
   - `formModel.extraParamsText`
   - `formModel.systemPrompt`
2. 后端 payload 和 API 协议保持不变

## 约束

1. 不引入复杂包装库，优先控制依赖数量。
2. 不改变后端接口或表单数据结构。
3. Monaco 集成应尽量通用，避免在页面内复制大量初始化逻辑。

## 验收标准

1. 三个页面都完成 Monaco 接入。
2. `Skills` 页面脚本语言切换会同步影响编辑器语言模式。
3. 现有保存链路不回归。
4. `npm run build` 通过。

## 风险与待确认项

1. 若 Monaco worker 接入不完整，某些语言能力可能退化。
2. 大型编辑器在弹窗中首次渲染时可能需要显式布局刷新。

## 交接输出

1. 允许架构阶段采用通用 Monaco 组件方案。
2. 要求计划阶段明确组件文件与页面写边界。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-090840
- 备注：需求锁定为 Skills/MCPs/Agents 三处 Monaco 集成。
