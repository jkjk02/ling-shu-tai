import type { Agent, AgentDraft, CliTool, DashboardResponse, Mcp, McpDraft, Skill, SkillDraft, Workflow, WorkflowDraft } from '@/types/resources';

export interface ApiListResponse<T> {
  items: T[];
  total: number;
}

export interface ApiDeleteResponse {
  deleted: boolean;
  id: string;
}

interface ApiResourceBase {
  id: string;
  name: string;
  description: string;
  cli_tool: CliTool;
  source_kind: 'discovered' | 'managed';
  source_path: string;
  is_writable: boolean;
  updated_at: string;
  created_at?: string;
}

export interface ApiSkill extends ApiResourceBase {
  trigger_command: string;
  script_language: string;
  script_content: string;
  tags: string[];
}

export interface ApiSkillUpsert {
  id?: string;
  name: string;
  description: string;
  cli_tool: CliTool;
  trigger_command: string;
  script_language: string;
  script_content: string;
  tags: string[];
  source_kind: 'managed' | 'discovered';
  source_path: string;
  is_writable: boolean;
}

export interface ApiMcp extends ApiResourceBase {
  model_name: string;
  temperature: number;
  max_tokens: number;
  top_p: number;
  presence_penalty: number;
  frequency_penalty: number;
  extra_params: Record<string, unknown>;
}

export interface ApiMcpUpsert {
  id?: string;
  name: string;
  description: string;
  cli_tool: CliTool;
  model_name: string;
  temperature: number;
  max_tokens: number;
  top_p: number;
  presence_penalty: number;
  frequency_penalty: number;
  extra_params: Record<string, unknown>;
  source_kind: 'managed' | 'discovered';
  source_path: string;
  is_writable: boolean;
}

export interface ApiAgent {
  id: string;
  name: string;
  description: string;
  system_prompt: string;
  skill_ids: string[];
  mcp_id: string | null;
  cli_tool: CliTool;
  tool_scope: CliTool[];
  updated_at: string;
  created_at?: string;
}

export interface ApiAgentUpsert {
  id?: string;
  name: string;
  description: string;
  system_prompt: string;
  skill_ids: string[];
  mcp_id: string | null;
  cli_tool: CliTool;
  tool_scope: CliTool[];
}

interface ApiWorkflowNode {
  id: string;
  label: string;
  agent_id: string | null;
  position: {
    x?: number;
    y?: number;
  };
  config?: Record<string, unknown>;
}

interface ApiWorkflowEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  condition?: string | null;
}

export interface ApiWorkflow {
  id: string;
  name: string;
  description: string;
  nodes: ApiWorkflowNode[];
  edges: ApiWorkflowEdge[];
  viewport: {
    x?: number;
    y?: number;
    zoom?: number;
  };
  updated_at: string;
  created_at?: string;
}

export interface ApiWorkflowUpsert {
  id?: string;
  name: string;
  description: string;
  nodes: ApiWorkflowNode[];
  edges: ApiWorkflowEdge[];
  viewport: {
    x: number;
    y: number;
    zoom: number;
  };
}

interface ApiResourceSummary {
  tool: CliTool;
  skills: number;
  mcps: number;
}

interface ApiDiscoveryStatus {
  tool: CliTool;
  status: 'available' | 'missing' | 'error';
}

export interface ApiDashboardResponse {
  updated_at: string;
  total_agents: number;
  total_workflows: number;
  tool_summaries: ApiResourceSummary[];
  discovery_summary: ApiDiscoveryStatus[];
}

function mapStatus(status?: ApiDiscoveryStatus['status']): 'ready' | 'warning' | 'missing' {
  if (status === 'available') {
    return 'ready';
  }
  if (status === 'error') {
    return 'warning';
  }
  return 'missing';
}

export function mapDashboard(data: ApiDashboardResponse): DashboardResponse {
  const discoveryByTool = new Map(data.discovery_summary.map((item) => [item.tool, item.status]));

  return {
    summaries: data.tool_summaries.map((summary) => ({
      cliTool: summary.tool,
      skillCount: summary.skills,
      mcpCount: summary.mcps,
      lastScanAt: data.updated_at,
      status: mapStatus(discoveryByTool.get(summary.tool)),
    })),
    agentCount: data.total_agents,
    workflowCount: data.total_workflows,
    lastUpdatedAt: data.updated_at,
  };
}

export function mapSkill(data: ApiSkill): Skill {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    cliTool: data.cli_tool,
    sourceKind: data.source_kind,
    sourcePath: data.source_path,
    isWritable: data.is_writable,
    updatedAt: data.updated_at,
    createdAt: data.created_at,
    triggerCommand: data.trigger_command,
    scriptLanguage: data.script_language,
    scriptContent: data.script_content,
    tags: data.tags,
  };
}

export function mapSkillPayload(data: SkillDraft): ApiSkillUpsert {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    cli_tool: data.cliTool,
    trigger_command: data.triggerCommand,
    script_language: data.scriptLanguage,
    script_content: data.scriptContent,
    tags: data.tags,
    source_kind: 'managed',
    source_path: '',
    is_writable: true,
  };
}

export function mapMcp(data: ApiMcp): Mcp {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    cliTool: data.cli_tool,
    sourceKind: data.source_kind,
    sourcePath: data.source_path,
    isWritable: data.is_writable,
    updatedAt: data.updated_at,
    createdAt: data.created_at,
    modelName: data.model_name,
    temperature: data.temperature,
    maxTokens: data.max_tokens,
    topP: data.top_p,
    presencePenalty: data.presence_penalty,
    frequencyPenalty: data.frequency_penalty,
    extraParams: data.extra_params,
  };
}

export function mapMcpPayload(data: McpDraft): ApiMcpUpsert {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    cli_tool: data.cliTool,
    model_name: data.modelName,
    temperature: data.temperature,
    max_tokens: data.maxTokens,
    top_p: data.topP,
    presence_penalty: data.presencePenalty,
    frequency_penalty: data.frequencyPenalty,
    extra_params: data.extraParams,
    source_kind: 'managed',
    source_path: '',
    is_writable: true,
  };
}

export function mapAgent(data: ApiAgent): Agent {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    systemPrompt: data.system_prompt,
    skillIds: data.skill_ids,
    mcpId: data.mcp_id,
    cliTool: data.cli_tool,
    toolScope: data.tool_scope,
    updatedAt: data.updated_at,
    createdAt: data.created_at,
  };
}

export function mapAgentPayload(data: AgentDraft): ApiAgentUpsert {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    system_prompt: data.systemPrompt,
    skill_ids: data.skillIds,
    mcp_id: data.mcpId,
    cli_tool: data.cliTool,
    tool_scope: data.toolScope,
  };
}

export function mapWorkflow(data: ApiWorkflow): Workflow {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    nodes: data.nodes.map((node) => ({
      id: node.id,
      label: node.label,
      agentId: node.agent_id,
      x: node.position.x ?? 0,
      y: node.position.y ?? 0,
      config: node.config ?? {},
    })),
    edges: data.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      condition: edge.condition ?? null,
    })),
    viewport: {
      x: data.viewport?.x ?? 0,
      y: data.viewport?.y ?? 0,
      zoom: data.viewport?.zoom ?? 1,
    },
    updatedAt: data.updated_at,
    createdAt: data.created_at,
  };
}

export function mapWorkflowPayload(data: WorkflowDraft): ApiWorkflowUpsert {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    nodes: data.nodes.map((node) => ({
      id: node.id,
      label: node.label,
      agent_id: node.agentId,
      position: {
        x: node.x,
        y: node.y,
      },
      config: node.config,
    })),
    edges: data.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      condition: edge.condition ?? null,
    })),
    viewport: {
      x: data.viewport.x,
      y: data.viewport.y,
      zoom: data.viewport.zoom,
    },
  };
}
