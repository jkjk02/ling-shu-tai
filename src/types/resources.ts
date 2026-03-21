export type CliTool = 'codex' | 'cludea' | 'opencode';

export interface ResourceBase {
  id: string;
  name: string;
  description: string;
  cliTool: CliTool;
  sourceKind: 'discovered' | 'managed';
  sourcePath: string;
  isWritable: boolean;
  updatedAt: string;
  createdAt?: string;
}

export interface Skill extends ResourceBase {
  triggerCommand: string;
  scriptLanguage: string;
  scriptContent: string;
  tags: string[];
}

export interface SkillDraft {
  id?: string;
  name: string;
  description: string;
  cliTool: CliTool;
  triggerCommand: string;
  scriptLanguage: string;
  scriptContent: string;
  tags: string[];
}

export interface Mcp extends ResourceBase {
  modelName: string;
  temperature: number;
  maxTokens: number;
  topP: number;
  presencePenalty: number;
  frequencyPenalty: number;
  extraParams: Record<string, unknown>;
}

export interface McpDraft {
  id?: string;
  name: string;
  description: string;
  cliTool: CliTool;
  modelName: string;
  temperature: number;
  maxTokens: number;
  topP: number;
  presencePenalty: number;
  frequencyPenalty: number;
  extraParams: Record<string, unknown>;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  systemPrompt: string;
  skillIds: string[];
  mcpId: string | null;
  cliTool: CliTool;
  toolScope: CliTool[];
  updatedAt: string;
  createdAt?: string;
}

export interface AgentDraft {
  id?: string;
  name: string;
  description: string;
  systemPrompt: string;
  skillIds: string[];
  mcpId: string | null;
  cliTool: CliTool;
  toolScope: CliTool[];
}

export interface WorkflowNode {
  id: string;
  label: string;
  agentId: string | null;
  x: number;
  y: number;
  config: Record<string, unknown>;
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  condition?: string | null;
}

export interface Workflow {
  id: string;
  name: string;
  description: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  viewport: {
    x: number;
    y: number;
    zoom: number;
  };
  updatedAt: string;
  createdAt?: string;
}

export interface WorkflowDraft {
  id?: string;
  name: string;
  description: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  viewport: {
    x: number;
    y: number;
    zoom: number;
  };
}

export interface DashboardSummary {
  cliTool: CliTool;
  skillCount: number;
  mcpCount: number;
  lastScanAt: string;
  status: 'ready' | 'warning' | 'missing';
}

export interface DashboardResponse {
  summaries: DashboardSummary[];
  agentCount: number;
  workflowCount: number;
  lastUpdatedAt: string;
}
