import type { Agent, DashboardResponse, Mcp, Skill, Workflow } from '@/types/resources';

export const mockDashboard: DashboardResponse = {
  summaries: [
    { cliTool: 'codex', skillCount: 12, mcpCount: 4, lastScanAt: '2026-03-19 14:05', status: 'ready' },
    { cliTool: 'cludea', skillCount: 9, mcpCount: 3, lastScanAt: '2026-03-19 14:01', status: 'warning' },
    { cliTool: 'opencode', skillCount: 7, mcpCount: 2, lastScanAt: '2026-03-19 13:56', status: 'missing' },
  ],
  agentCount: 18,
  workflowCount: 6,
  lastUpdatedAt: '2026-03-19 14:06',
};

export const mockSkills: Skill[] = [
  {
    id: 'skill_codex_review',
    name: '代码审查',
    description: '面向 codex 的实现审查技能。',
    cliTool: 'codex',
    sourceKind: 'managed',
    sourcePath: 'backend/data/managed/skills/codex/review.md',
    isWritable: true,
    updatedAt: '2026-03-19 13:48',
    triggerCommand: '/review',
    scriptLanguage: 'markdown',
    scriptContent: 'Review implementation changes',
    tags: ['review', 'quality'],
  },
  {
    id: 'skill_cludea_design',
    name: '设计校对',
    description: '检查设计约束与组件结构。',
    cliTool: 'cludea',
    sourceKind: 'discovered',
    sourcePath: '~/.cludea/skills/design.md',
    isWritable: false,
    updatedAt: '2026-03-19 12:21',
    triggerCommand: '/design-check',
    scriptLanguage: 'markdown',
    scriptContent: 'Validate design constraints',
    tags: ['design'],
  },
];

export const mockMcps: Mcp[] = [
  {
    id: 'mcp_gpt_5_4',
    name: 'GPT-5.4 稳定配置',
    description: '通用高质量执行配置。',
    cliTool: 'codex',
    sourceKind: 'managed',
    sourcePath: 'backend/data/managed/mcps/codex/gpt-5.4.json',
    isWritable: true,
    updatedAt: '2026-03-19 12:55',
    modelName: 'gpt-5.4',
    temperature: 0.2,
    maxTokens: 8192,
    topP: 0.95,
    presencePenalty: 0,
    frequencyPenalty: 0,
    extraParams: { top_p: 0.95 },
  },
  {
    id: 'mcp_claude_sonnet',
    name: 'Claude Sonnet 任务配置',
    description: '偏探索型任务配置。',
    cliTool: 'cludea',
    sourceKind: 'discovered',
    sourcePath: '~/.claude/mcps/sonnet.json',
    isWritable: false,
    updatedAt: '2026-03-18 22:11',
    modelName: 'claude-sonnet',
    temperature: 0.5,
    maxTokens: 4096,
    topP: 1,
    presencePenalty: 0.1,
    frequencyPenalty: 0,
    extraParams: { presence_penalty: 0.1 },
  },
];

export const mockAgents: Agent[] = [
  {
    id: 'agent_requirements_analyst',
    name: '需求分析师',
    description: '负责梳理目标、范围、验收标准和需求约束。',
    systemPrompt: '负责澄清目标、范围与验收标准。',
    skillIds: ['skill_codex_review'],
    mcpId: 'mcp_gpt_5_4',
    cliTool: 'codex',
    toolScope: ['codex', 'cludea'],
    updatedAt: '2026-03-19 13:20',
    createdAt: '2026-03-19 12:40',
  },
  {
    id: 'agent_workflow_designer',
    name: '流程编排师',
    description: '面向多 Agent 任务流设计的流程负责人。',
    systemPrompt: '负责多 Agent 流程设计。',
    skillIds: ['skill_cludea_design'],
    mcpId: 'mcp_claude_sonnet',
    cliTool: 'cludea',
    toolScope: ['cludea', 'opencode'],
    updatedAt: '2026-03-19 13:12',
    createdAt: '2026-03-19 12:18',
  },
];

export const mockWorkflows: Workflow[] = [
  {
    id: 'workflow_delivery_flow',
    name: '交付流水线',
    description: '需求 -> 架构 -> 实现 -> 审查 -> 测试',
    createdAt: '2026-03-19 12:45',
    updatedAt: '2026-03-19 13:40',
    viewport: { x: 0, y: 0, zoom: 1 },
    nodes: [
      {
        id: 'n1',
        label: '需求',
        agentId: 'agent_requirements_analyst',
        x: 40,
        y: 80,
        config: { kind: 'start', stage: 'requirements', notes: '梳理目标与验收标准' },
      },
      {
        id: 'n2',
        label: '实现',
        agentId: 'agent_workflow_designer',
        x: 280,
        y: 80,
        config: { kind: 'task', stage: 'implementation', notes: '进入实现与交付阶段' },
      },
    ],
    edges: [{ id: 'e1', source: 'n1', target: 'n2', label: '交接', condition: '需求已批准' }],
  },
];
