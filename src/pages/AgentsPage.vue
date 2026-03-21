<script setup lang="ts">
import { computed, defineAsyncComponent, reactive, ref, watch } from 'vue';
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus';

import { agentsApi, mcpsApi, skillsApi } from '@/api/resources';
import { getErrorMessage } from '@/api/http';
import AppSectionHeader from '@/components/AppSectionHeader.vue';
import { mockAgents, mockMcps, mockSkills } from '@/data/mock';
import type { Agent, CliTool, Mcp, Skill } from '@/types/resources';

const MonacoCodeEditor = defineAsyncComponent(() => import('@/components/MonacoCodeEditor.vue'));

type FilterTool = 'all' | CliTool;
type DialogMode = 'create' | 'edit';

interface AgentFormModel {
  name: string;
  description: string;
  cliTool: CliTool;
  systemPrompt: string;
  skillIds: string[];
  mcpId: string | null;
  toolScope: CliTool[];
}

const cliToolOptions: CliTool[] = ['codex', 'cludea', 'opencode'];

const agents = ref<Agent[]>([]);
const skills = ref<Skill[]>([]);
const mcps = ref<Mcp[]>([]);
const loading = ref(false);
const saving = ref(false);
const warningMessage = ref('');
const usingMockData = ref(false);
const filterTool = ref<FilterTool>('all');
const selectedAgentId = ref('');
const dialogVisible = ref(false);
const dialogMode = ref<DialogMode>('create');
const editingAgentId = ref('');
const formRef = ref<FormInstance>();

const formModel = reactive<AgentFormModel>({
  name: '',
  description: '',
  cliTool: 'codex',
  systemPrompt: '',
  skillIds: [],
  mcpId: null,
  toolScope: ['codex'],
});

const formRules: FormRules<AgentFormModel> = {
  name: [{ required: true, message: '请输入 Agent 名称', trigger: ['blur', 'change'] }],
  cliTool: [{ required: true, message: '请选择主 CLI 工具', trigger: 'change' }],
  systemPrompt: [{ required: true, message: '请输入 System Prompt', trigger: 'blur' }],
  toolScope: [
    {
      validator: (_rule, value: CliTool[], callback) => {
        if (!value?.length) {
          callback(new Error('请至少选择一个 Tool Scope'));
          return;
        }
        callback();
      },
      trigger: 'change',
    },
  ],
};

const filteredAgents = computed(() =>
  filterTool.value === 'all' ? agents.value : agents.value.filter((item) => item.cliTool === filterTool.value),
);

const selectedAgent = computed(
  () => filteredAgents.value.find((item) => item.id === selectedAgentId.value) ?? filteredAgents.value[0] ?? null,
);

const dialogTitle = computed(() => (dialogMode.value === 'create' ? '新建 Agent' : '编辑 Agent'));
const hasRealBackend = computed(() => !usingMockData.value);

const skillNameMap = computed(() => new Map(skills.value.map((item) => [item.id, item.name])));
const mcpNameMap = computed(() => new Map(mcps.value.map((item) => [item.id, item.name])));

function resetForm() {
  formModel.name = '';
  formModel.description = '';
  formModel.cliTool = 'codex';
  formModel.systemPrompt = '';
  formModel.skillIds = [];
  formModel.mcpId = null;
  formModel.toolScope = ['codex'];
}

function populateForm(agent?: Agent) {
  if (!agent) {
    resetForm();
    return;
  }

  formModel.name = agent.name;
  formModel.description = agent.description;
  formModel.cliTool = agent.cliTool;
  formModel.systemPrompt = agent.systemPrompt;
  formModel.skillIds = [...agent.skillIds];
  formModel.mcpId = agent.mcpId;
  formModel.toolScope = [...agent.toolScope];
}

function syncSelection(preferredId?: string) {
  if (preferredId && filteredAgents.value.some((item) => item.id === preferredId)) {
    selectedAgentId.value = preferredId;
    return;
  }

  if (filteredAgents.value.some((item) => item.id === selectedAgentId.value)) {
    return;
  }

  selectedAgentId.value = filteredAgents.value[0]?.id ?? '';
}

async function loadPageData(preferredId?: string) {
  loading.value = true;
  warningMessage.value = '';

  try {
    const [agentItems, skillItems, mcpItems] = await Promise.all([agentsApi.list(), skillsApi.list(), mcpsApi.list()]);
    agents.value = agentItems;
    skills.value = skillItems;
    mcps.value = mcpItems;
    usingMockData.value = false;
  } catch (error) {
    agents.value = mockAgents;
    skills.value = mockSkills;
    mcps.value = mockMcps;
    usingMockData.value = true;
    warningMessage.value = getErrorMessage(
      error,
      'Agents 接口暂不可用，当前显示本地示例数据，已禁用新增、编辑和删除操作。',
    );
  } finally {
    syncSelection(preferredId);
    loading.value = false;
  }
}

function openCreateDialog() {
  if (!hasRealBackend.value) {
    return;
  }

  dialogMode.value = 'create';
  editingAgentId.value = '';
  resetForm();
  dialogVisible.value = true;
}

function openEditDialog(agent: Agent) {
  if (!hasRealBackend.value) {
    return;
  }

  dialogMode.value = 'edit';
  editingAgentId.value = agent.id;
  populateForm(agent);
  dialogVisible.value = true;
}

function buildPayload() {
  return {
    name: formModel.name.trim(),
    description: formModel.description.trim(),
    system_prompt: formModel.systemPrompt.trim(),
    skill_ids: [...formModel.skillIds],
    mcp_id: formModel.mcpId,
    cli_tool: formModel.cliTool,
    tool_scope: [...formModel.toolScope],
  };
}

async function submitAgent() {
  if (!formRef.value) {
    return;
  }

  await formRef.value.validate();
  saving.value = true;

  try {
    const payload = buildPayload();

    if (dialogMode.value === 'create') {
      const created = await agentsApi.create(payload);
      filterTool.value = created.cliTool;
      await loadPageData(created.id);
      ElMessage.success(`Agent ${created.name} 已创建`);
    } else {
      const updated = await agentsApi.update(editingAgentId.value, payload);
      filterTool.value = updated.cliTool;
      await loadPageData(updated.id);
      ElMessage.success(`Agent ${updated.name} 已保存`);
    }

    dialogVisible.value = false;
  } catch (error) {
    ElMessage.error(getErrorMessage(error, 'Agent 保存失败，请检查输入后重试。'));
  } finally {
    saving.value = false;
  }
}

async function removeAgent(agent: Agent) {
  if (!hasRealBackend.value) {
    return;
  }

  try {
    await ElMessageBox.confirm(`将删除 Agent「${agent.name}」，此操作无法撤销。`, '删除确认', {
      type: 'warning',
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
    });
  } catch {
    return;
  }

  try {
    await agentsApi.remove(agent.id);
    ElMessage.success(`Agent ${agent.name} 已删除`);
    await loadPageData();
  } catch (error) {
    ElMessage.error(getErrorMessage(error, 'Agent 删除失败，请稍后重试。'));
  }
}

function handleRowClick(agent: Agent) {
  selectedAgentId.value = agent.id;
}

function getSkillLabels(agent: Agent) {
  return agent.skillIds.map((id) => skillNameMap.value.get(id) ?? id);
}

function getMcpLabel(agent: Agent) {
  if (!agent.mcpId) {
    return '未关联 MCP';
  }
  return mcpNameMap.value.get(agent.mcpId) ?? agent.mcpId;
}

watch(filterTool, () => {
  syncSelection();
});

loadPageData();
</script>

<template>
  <div class="page-stack">
    <AppSectionHeader
      title="Agents 管理"
      description="补通 Agent 的列表、详情、System Prompt、Skill 授权与 MCP 关联闭环。"
    >
      <div class="skills-toolbar">
        <el-select v-model="filterTool" style="width: 160px">
          <el-option label="全部 CLI" value="all" />
          <el-option v-for="tool in cliToolOptions" :key="tool" :label="tool" :value="tool" />
        </el-select>
        <el-button type="primary" :disabled="!hasRealBackend" @click="openCreateDialog">新建 Agent</el-button>
      </div>
    </AppSectionHeader>

    <el-alert v-if="warningMessage" :title="warningMessage" type="warning" show-icon :closable="false" />

    <div class="split-grid">
      <el-card shadow="never">
        <template #header>
          <div class="card-header">
            <strong>Agents 列表</strong>
            <span>{{ filteredAgents.length }} 条</span>
          </div>
        </template>

        <el-table
          v-loading="loading"
          :data="filteredAgents"
          row-key="id"
          empty-text="当前筛选条件下暂无 Agent"
          @row-click="handleRowClick"
        >
          <el-table-column prop="name" label="名称" min-width="170" />
          <el-table-column prop="id" label="ID" min-width="170" />
          <el-table-column label="主 CLI" width="120">
            <template #default="{ row }">
              <el-tag size="small" effect="plain">{{ row.cliTool }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="Skills" width="100">
            <template #default="{ row }">{{ row.skillIds.length }}</template>
          </el-table-column>
          <el-table-column label="MCP" min-width="160" show-overflow-tooltip>
            <template #default="{ row }">{{ getMcpLabel(row) }}</template>
          </el-table-column>
          <el-table-column prop="updatedAt" label="更新时间" min-width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button text type="primary" @click.stop="handleRowClick(row)">详情</el-button>
                <el-button text type="primary" :disabled="!hasRealBackend" @click.stop="openEditDialog(row)">编辑</el-button>
                <el-button text type="danger" :disabled="!hasRealBackend" @click.stop="removeAgent(row)">删除</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <el-card shadow="never">
        <template #header>
          <div class="card-header">
            <strong>Agent 详情</strong>
            <el-tag v-if="selectedAgent" size="small" type="success">{{ selectedAgent.cliTool }}</el-tag>
          </div>
        </template>

        <div v-if="selectedAgent" class="page-stack">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="名称">{{ selectedAgent.name }}</el-descriptions-item>
            <el-descriptions-item label="ID">{{ selectedAgent.id }}</el-descriptions-item>
            <el-descriptions-item label="主 CLI">{{ selectedAgent.cliTool }}</el-descriptions-item>
            <el-descriptions-item label="关联 MCP">{{ getMcpLabel(selectedAgent) }}</el-descriptions-item>
            <el-descriptions-item label="Tool Scope">{{ selectedAgent.toolScope.join(' / ') }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ selectedAgent.createdAt || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="更新时间">{{ selectedAgent.updatedAt }}</el-descriptions-item>
            <el-descriptions-item label="描述">{{ selectedAgent.description || '暂无描述' }}</el-descriptions-item>
            <el-descriptions-item label="授权 Skills">
              <div class="tag-row">
                <el-tag v-for="skillLabel in getSkillLabels(selectedAgent)" :key="skillLabel" size="small" type="info">
                  {{ skillLabel }}
                </el-tag>
                <span v-if="selectedAgent.skillIds.length === 0" class="muted-text">未分配 Skill</span>
              </div>
            </el-descriptions-item>
          </el-descriptions>

          <div class="card-header">
            <strong>System Prompt</strong>
            <div class="table-actions">
              <el-button text type="primary" :disabled="!hasRealBackend" @click="openEditDialog(selectedAgent)">编辑</el-button>
              <el-button text type="danger" :disabled="!hasRealBackend" @click="removeAgent(selectedAgent)">删除</el-button>
            </div>
          </div>

          <pre class="code-surface">{{ selectedAgent.systemPrompt }}</pre>
        </div>

        <el-empty v-else description="请选择一个 Agent 查看详情" />
      </el-card>
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="780px" destroy-on-close>
      <el-form ref="formRef" :model="formModel" :rules="formRules" label-position="top" class="page-stack">
        <div class="split-grid">
          <el-form-item label="名称" prop="name">
            <el-input v-model="formModel.name" placeholder="例如：Planner Agent" />
          </el-form-item>

          <el-form-item label="主 CLI 工具" prop="cliTool">
            <el-select v-model="formModel.cliTool">
              <el-option v-for="tool in cliToolOptions" :key="tool" :label="tool" :value="tool" />
            </el-select>
          </el-form-item>
        </div>

        <el-form-item label="描述" prop="description">
          <el-input v-model="formModel.description" type="textarea" :rows="3" placeholder="描述这个 Agent 的职责定位" />
        </el-form-item>

        <el-form-item label="System Prompt" prop="systemPrompt">
          <MonacoCodeEditor
            v-model="formModel.systemPrompt"
            language="markdown"
            :height="260"
          />
        </el-form-item>

        <div class="split-grid">
          <el-form-item label="授权 Skills" prop="skillIds">
            <el-select v-model="formModel.skillIds" multiple filterable collapse-tags>
              <el-option v-for="skill in skills" :key="skill.id" :label="skill.name" :value="skill.id" />
            </el-select>
          </el-form-item>

          <el-form-item label="关联 MCP" prop="mcpId">
            <el-select v-model="formModel.mcpId" clearable placeholder="可为空">
              <el-option v-for="mcp in mcps" :key="mcp.id" :label="mcp.name" :value="mcp.id" />
            </el-select>
          </el-form-item>
        </div>

        <el-form-item label="Tool Scope" prop="toolScope">
          <el-select v-model="formModel.toolScope" multiple collapse-tags>
            <el-option v-for="tool in cliToolOptions" :key="tool" :label="tool" :value="tool" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="table-actions">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="saving" @click="submitAgent">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>
