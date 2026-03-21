import type { Agent, DashboardResponse, Mcp, Skill, Workflow } from '@/types/resources';

import {
  type ApiDeleteResponse,
  mapAgent,
  mapDashboard,
  mapMcp,
  mapSkill,
  mapWorkflow,
  type ApiAgent,
  type ApiAgentUpsert,
  type ApiDashboardResponse,
  type ApiListResponse,
  type ApiMcp,
  type ApiMcpUpsert,
  type ApiSkill,
  type ApiSkillUpsert,
  type ApiWorkflow,
  type ApiWorkflowUpsert,
} from './contracts';
import { http } from './http';

export const dashboardApi = {
  async getOverview() {
    const { data } = await http.get<ApiDashboardResponse>('/dashboard');
    return mapDashboard(data);
  },
};

export const skillsApi = {
  async list() {
    const { data } = await http.get<ApiListResponse<ApiSkill>>('/skills');
    return data.items.map(mapSkill);
  },

  async get(skillId: string) {
    const { data } = await http.get<ApiSkill>(`/skills/${skillId}`);
    return mapSkill(data);
  },

  async create(payload: ApiSkillUpsert) {
    const { data } = await http.post<ApiSkill>('/skills', payload);
    return mapSkill(data);
  },

  async update(skillId: string, payload: ApiSkillUpsert) {
    const { data } = await http.put<ApiSkill>(`/skills/${skillId}`, payload);
    return mapSkill(data);
  },

  async remove(skillId: string) {
    const { data } = await http.delete<ApiDeleteResponse>(`/skills/${skillId}`);
    return data;
  },
};

export const mcpsApi = {
  async list() {
    const { data } = await http.get<ApiListResponse<ApiMcp>>('/mcps');
    return data.items.map(mapMcp);
  },

  async get(mcpId: string) {
    const { data } = await http.get<ApiMcp>(`/mcps/${mcpId}`);
    return mapMcp(data);
  },

  async create(payload: ApiMcpUpsert) {
    const { data } = await http.post<ApiMcp>('/mcps', payload);
    return mapMcp(data);
  },

  async update(mcpId: string, payload: ApiMcpUpsert) {
    const { data } = await http.put<ApiMcp>(`/mcps/${mcpId}`, payload);
    return mapMcp(data);
  },

  async remove(mcpId: string) {
    const { data } = await http.delete<ApiDeleteResponse>(`/mcps/${mcpId}`);
    return data;
  },
};

export const agentsApi = {
  async list() {
    const { data } = await http.get<ApiListResponse<ApiAgent>>('/agents');
    return data.items.map(mapAgent);
  },

  async get(agentId: string) {
    const { data } = await http.get<ApiAgent>(`/agents/${agentId}`);
    return mapAgent(data);
  },

  async create(payload: ApiAgentUpsert) {
    const { data } = await http.post<ApiAgent>('/agents', payload);
    return mapAgent(data);
  },

  async update(agentId: string, payload: ApiAgentUpsert) {
    const { data } = await http.put<ApiAgent>(`/agents/${agentId}`, payload);
    return mapAgent(data);
  },

  async remove(agentId: string) {
    const { data } = await http.delete<ApiDeleteResponse>(`/agents/${agentId}`);
    return data;
  },
};

export const workflowsApi = {
  async list() {
    const { data } = await http.get<ApiListResponse<ApiWorkflow>>('/workflows');
    return data.items.map(mapWorkflow);
  },

  async get(workflowId: string) {
    const { data } = await http.get<ApiWorkflow>(`/workflows/${workflowId}`);
    return mapWorkflow(data);
  },

  async create(payload: ApiWorkflowUpsert) {
    const { data } = await http.post<ApiWorkflow>('/workflows', payload);
    return mapWorkflow(data);
  },

  async update(workflowId: string, payload: ApiWorkflowUpsert) {
    const { data } = await http.put<ApiWorkflow>(`/workflows/${workflowId}`, payload);
    return mapWorkflow(data);
  },

  async remove(workflowId: string) {
    const { data } = await http.delete<ApiDeleteResponse>(`/workflows/${workflowId}`);
    return data;
  },
};
