# Monaco Editor 集成运行台账

- 阶段：00-governance
- 提交时间：20260321-090750
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/07-delivery/20260321-085619-current-product-handoff.md

## 目标

1. 为“Monaco Editor 集成”切片建立独立运行台账。
2. 在不改动后端协议的前提下，升级前端大文本与 JSON 编辑体验。
3. 固定本轮范围、依赖、验证门槛和交付链，方便后续会话继续扩展。

## 核心内容

1. 当前项目状态：
   - 已具备后端自动化回归、统一验证入口与 CI 骨架。
   - `Skills`、`MCPs`、`Agents` 页面的大文本编辑仍使用普通 `textarea`。
2. 本轮优先级判断：
   - 用户明确表示不继续自动化与冒烟方向。
   - 当前最直接的产品能力增量是提高脚本、JSON 与 Prompt 的编辑体验。
3. 本轮范围：
   - 引入 Monaco Editor 依赖
   - 产出通用代码编辑器组件
   - 覆盖 `Skills` 脚本内容、`MCPs` 扩展参数 JSON、`Agents` System Prompt
   - README 与 `docx` 同步更新
4. 本轮非范围：
   - 不重做 Workflows 画布
   - 不新增执行引擎
   - 不做完整主题系统
5. 验证门槛：
   - `npm run build` 通过
   - Monaco 组件能在三个页面被正常引用
   - README 明确说明 Monaco 已接入的位置

## 风险与待确认项

1. Monaco 引入后会增加前端包体积。
2. 若不配置 worker，JSON 语言能力与体验会受限；架构阶段需明确最小可行方案。
3. 需要避免 Monaco 与 Element Plus 弹窗尺寸、滚动和校验交互冲突。

## 交接输出

1. 允许需求阶段围绕三处高价值编辑位建立需求基线。
2. 要求架构阶段比较“仅替换 textarea”与“通用 Monaco 组件复用”两种路径，推荐后者。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-090820
- 备注：本轮锁定为 Monaco Editor 集成，停止自动化与冒烟分支。
