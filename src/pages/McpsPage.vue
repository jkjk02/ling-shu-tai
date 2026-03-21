<script setup lang="ts">
import { computed, defineAsyncComponent, reactive, ref, watch } from 'vue';
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus';

import { getErrorMessage } from '@/api/http';
import { mapMcpPayload } from '@/api/contracts';
import { mcpsApi } from '@/api/resources';
import AppSectionHeader from '@/components/AppSectionHeader.vue';
import { mockMcps } from '@/data/mock';
import type { CliTool, Mcp, McpDraft } from '@/types/resources';

const MonacoCodeEditor = defineAsyncComponent(() => import('@/components/MonacoCodeEditor.vue'));

type FilterTool = 'all' | CliTool;
type DialogMode = 'create' | 'edit';

interface McpFormModel {
  name: string;
  description: string;
  cliTool: CliTool;
  installTarget: 'managed' | 'discovered';
  modelName: string;
  temperature: number;
  maxTokens: number;
  topP: number;
  presencePenalty: number;
  frequencyPenalty: number;
  extraParamsText: string;
}

const cliToolOptions: CliTool[] = ['codex', 'cludea', 'opencode'];

const mcps = ref<Mcp[]>([]);
const loading = ref(false);
const saving = ref(false);
const warningMessage = ref('');
const usingMockData = ref(false);
const filterTool = ref<FilterTool>('all');
const selectedMcpId = ref('');
const dialogVisible = ref(false);
const dialogMode = ref<DialogMode>('create');
const editingMcpId = ref('');
const formRef = ref<FormInstance>();

const formModel = reactive<McpFormModel>({
  name: '',
  description: '',
  cliTool: 'codex',
  installTarget: 'managed',
  modelName: '',
  temperature: 0.2,
  maxTokens: 4096,
  topP: 1,
  presencePenalty: 0,
  frequencyPenalty: 0,
  extraParamsText: '{}',
});

const formRules: FormRules<McpFormModel> = {
  name: [{ required: true, message: '请输入 MCP 名称', trigger: ['blur', 'change'] }],
  cliTool: [{ required: true, message: '请选择所属 CLI 工具', trigger: 'change' }],
  modelName: [{ required: true, message: '请输入模型名称', trigger: 'blur' }],
  extraParamsText: [
    {
      validator: (_rule, value: string, callback) => {
        try {
          const parsed = JSON.parse(value || '{}') as unknown;
          if (parsed === null || Array.isArray(parsed) || typeof parsed !== 'object') {
            callback(new Error('扩展参数必须是 JSON 对象'));
            return;
          }
          callback();
        } catch {
          callback(new Error('扩展参数必须是合法 JSON'));
        }
      },
      trigger: 'blur',
    },
  ],
};

const filteredMcps = computed(() =>
  filterTool.value === 'all' ? mcps.value : mcps.value.filter((item) => item.cliTool === filterTool.value),
);

const selectedMcp = computed(
  () => filteredMcps.value.find((item) => item.id === selectedMcpId.value) ?? filteredMcps.value[0] ?? null,
);

const dialogTitle = computed(() => (dialogMode.value === 'create' ? '新建 MCP' : '编辑 MCP'));
const hasRealBackend = computed(() => !usingMockData.value);

function formatJson(value: Record<string, unknown>) {
  return JSON.stringify(value, null, 2);
}

function resetForm() {
  formModel.name = '';
  formModel.description = '';
  formModel.cliTool = 'codex';
  formModel.installTarget = 'managed';
  formModel.modelName = '';
  formModel.temperature = 0.2;
  formModel.maxTokens = 4096;
  formModel.topP = 1;
  formModel.presencePenalty = 0;
  formModel.frequencyPenalty = 0;
  formModel.extraParamsText = '{}';
}

function populateForm(mcp?: Mcp) {
  if (!mcp) {
    resetForm();
    return;
  }

  formModel.name = mcp.name;
  formModel.description = mcp.description;
  formModel.cliTool = mcp.cliTool;
  formModel.installTarget = mcp.sourceKind;
  formModel.modelName = mcp.modelName;
  formModel.temperature = mcp.temperature;
  formModel.maxTokens = mcp.maxTokens;
  formModel.topP = mcp.topP;
  formModel.presencePenalty = mcp.presencePenalty;
  formModel.frequencyPenalty = mcp.frequencyPenalty;
  formModel.extraParamsText = formatJson(mcp.extraParams);
}

function syncSelection(preferredId?: string) {
  if (preferredId && filteredMcps.value.some((item) => item.id === preferredId)) {
    selectedMcpId.value = preferredId;
    return;
  }

  if (filteredMcps.value.some((item) => item.id === selectedMcpId.value)) {
    return;
  }

  selectedMcpId.value = filteredMcps.value[0]?.id ?? '';
}

async function loadMcps(preferredId?: string) {
  loading.value = true;
  warningMessage.value = '';

  try {
    mcps.value = await mcpsApi.list();
    usingMockData.value = false;
  } catch (error) {
    mcps.value = mockMcps;
    usingMockData.value = true;
    warningMessage.value = getErrorMessage(
      error,
      'MCP 接口暂不可用，当前显示本地示例数据，已禁用新增、编辑和删除操作。',
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
  editingMcpId.value = '';
  resetForm();
  dialogVisible.value = true;
}

function openEditDialog(mcp: Mcp) {
  if (!hasRealBackend.value || !mcp.isWritable) {
    return;
  }

  dialogMode.value = 'edit';
  editingMcpId.value = mcp.id;
  populateForm(mcp);
  dialogVisible.value = true;
}

function buildDraft(): McpDraft {
  return {
    name: formModel.name.trim(),
    description: formModel.description.trim(),
    cliTool: formModel.cliTool,
    modelName: formModel.modelName.trim(),
    temperature: Number(formModel.temperature),
    maxTokens: Number(formModel.maxTokens),
    topP: Number(formModel.topP),
    presencePenalty: Number(formModel.presencePenalty),
    frequencyPenalty: Number(formModel.frequencyPenalty),
    extraParams: JSON.parse(formModel.extraParamsText || '{}') as Record<string, unknown>,
  };
}

async function submitMcp() {
  if (!formRef.value) {
    return;
  }

  await formRef.value.validate();
  saving.value = true;

  try {
    const draft = buildDraft();
    const current = mcps.value.find((item) => item.id === editingMcpId.value);
    const payload = mapMcpPayload(draft);
    payload.source_kind = dialogMode.value === 'create' ? formModel.installTarget : current?.sourceKind ?? 'managed';
    payload.source_path = current?.sourcePath ?? '';
    payload.is_writable = current?.isWritable ?? true;

    if (dialogMode.value === 'create') {
      const created = await mcpsApi.create(payload);
      filterTool.value = created.cliTool;
      await loadMcps(created.id);
      ElMessage.success(`MCP ${created.name} 已创建`);
    } else {
      const updated = await mcpsApi.update(editingMcpId.value, payload);
      filterTool.value = updated.cliTool;
      await loadMcps(updated.id);
      ElMessage.success(`MCP ${updated.name} 已保存`);
    }

    dialogVisible.value = false;
  } catch (error) {
    ElMessage.error(getErrorMessage(error, 'MCP 保存失败，请检查输入后重试。'));
  } finally {
    saving.value = false;
  }
}

async function removeMcp(mcp: Mcp) {
  if (!hasRealBackend.value || !mcp.isWritable) {
    return;
  }

  try {
    await ElMessageBox.confirm(`将删除 MCP「${mcp.name}」，此操作无法撤销。`, '删除确认', {
      type: 'warning',
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
    });
  } catch {
    return;
  }

  try {
    await mcpsApi.remove(mcp.id);
    ElMessage.success(`MCP ${mcp.name} 已删除`);
    await loadMcps();
  } catch (error) {
    ElMessage.error(getErrorMessage(error, 'MCP 删除失败，请稍后重试。'));
  }
}

function handleRowClick(mcp: Mcp) {
  selectedMcpId.value = mcp.id;
}

watch(filterTool, () => {
  syncSelection();
});

loadMcps();
</script>

<template>
  <div class="page-stack">
    <AppSectionHeader
      title="MCPs 管理"
      description="统一查看 managed 与外部发现的 MCPs；受支持的外部 JSON MCP 可直接回写到原始目录。"
    >
      <div class="skills-toolbar">
        <el-select v-model="filterTool" style="width: 160px">
          <el-option label="全部 CLI" value="all" />
          <el-option v-for="tool in cliToolOptions" :key="tool" :label="tool" :value="tool" />
        </el-select>
        <el-button data-testid="mcp-create-button" type="primary" :disabled="!hasRealBackend" @click="openCreateDialog">新建 MCP</el-button>
      </div>
    </AppSectionHeader>

    <el-alert v-if="warningMessage" :title="warningMessage" type="warning" show-icon :closable="false" />

    <div class="split-grid">
      <el-card shadow="never">
        <template #header>
          <div class="card-header">
            <strong>MCP 列表</strong>
            <span>{{ filteredMcps.length }} 条</span>
          </div>
        </template>

        <el-table
          v-loading="loading"
          :data="filteredMcps"
          row-key="id"
          empty-text="当前筛选条件下暂无 MCP"
          @row-click="handleRowClick"
        >
          <el-table-column prop="name" label="名称" min-width="180" />
          <el-table-column prop="modelName" label="模型" min-width="160" />
          <el-table-column label="CLI" width="120">
            <template #default="{ row }">
              <el-tag size="small" effect="plain">{{ row.cliTool }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="来源" width="120">
            <template #default="{ row }">
              <el-tag size="small" :type="row.isWritable ? 'success' : 'info'" effect="plain">
                {{ row.sourceKind === 'managed' ? 'managed' : 'discovered' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="temperature" label="温度" width="100" />
          <el-table-column prop="maxTokens" label="Max Tokens" width="120" />
          <el-table-column prop="updatedAt" label="更新时间" min-width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button text type="primary" @click.stop="handleRowClick(row)">详情</el-button>
                <el-button text type="primary" :disabled="!row.isWritable || !hasRealBackend" @click.stop="openEditDialog(row)">
                  编辑
                </el-button>
                <el-button text type="danger" :disabled="!row.isWritable || !hasRealBackend" @click.stop="removeMcp(row)">
                  删除
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <el-card shadow="never">
        <template #header>
          <div class="card-header">
            <strong>MCP 详情</strong>
            <el-tag v-if="selectedMcp" :type="selectedMcp.isWritable ? 'success' : 'info'" size="small">
              {{ selectedMcp.isWritable ? '可写' : '只读' }}
            </el-tag>
          </div>
        </template>

        <div v-if="selectedMcp" class="page-stack">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="名称">{{ selectedMcp.name }}</el-descriptions-item>
            <el-descriptions-item label="所属 CLI">{{ selectedMcp.cliTool }}</el-descriptions-item>
            <el-descriptions-item label="模型名称">{{ selectedMcp.modelName }}</el-descriptions-item>
            <el-descriptions-item label="温度">{{ selectedMcp.temperature }}</el-descriptions-item>
            <el-descriptions-item label="Max Tokens">{{ selectedMcp.maxTokens }}</el-descriptions-item>
            <el-descriptions-item label="Top P">{{ selectedMcp.topP }}</el-descriptions-item>
            <el-descriptions-item label="Presence Penalty">{{ selectedMcp.presencePenalty }}</el-descriptions-item>
            <el-descriptions-item label="Frequency Penalty">{{ selectedMcp.frequencyPenalty }}</el-descriptions-item>
            <el-descriptions-item label="来源类型">{{ selectedMcp.sourceKind }}</el-descriptions-item>
            <el-descriptions-item label="来源路径">{{ selectedMcp.sourcePath || '未设置' }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ selectedMcp.createdAt || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="更新时间">{{ selectedMcp.updatedAt }}</el-descriptions-item>
            <el-descriptions-item label="描述">{{ selectedMcp.description || '暂无描述' }}</el-descriptions-item>
          </el-descriptions>

          <div class="card-header">
            <strong>扩展参数</strong>
            <div class="table-actions">
              <el-button text type="primary" :disabled="!selectedMcp.isWritable || !hasRealBackend" @click="openEditDialog(selectedMcp)">
                编辑
              </el-button>
              <el-button text type="danger" :disabled="!selectedMcp.isWritable || !hasRealBackend" @click="removeMcp(selectedMcp)">
                删除
              </el-button>
            </div>
          </div>

          <pre class="code-surface">{{ formatJson(selectedMcp.extraParams) }}</pre>
        </div>

        <el-empty v-else description="请选择一个 MCP 查看详情" />
      </el-card>
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="760px" destroy-on-close>
      <el-form ref="formRef" :model="formModel" :rules="formRules" label-position="top" class="page-stack">
        <div class="split-grid">
          <el-form-item label="名称" prop="name">
            <el-input v-model="formModel.name" placeholder="例如：GPT-5.4 稳定配置" />
          </el-form-item>

          <el-form-item label="所属 CLI 工具" prop="cliTool">
            <el-select v-model="formModel.cliTool">
              <el-option v-for="tool in cliToolOptions" :key="tool" :label="tool" :value="tool" />
            </el-select>
          </el-form-item>
        </div>

        <el-form-item label="写入目标">
          <el-segmented
            v-model="formModel.installTarget"
            :options="[
              { label: 'managed', value: 'managed' },
              { label: 'external', value: 'discovered' },
            ]"
            :disabled="dialogMode === 'edit'"
          />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input v-model="formModel.description" type="textarea" :rows="3" placeholder="说明这个 MCP 的用途与适用场景" />
        </el-form-item>

        <div class="split-grid">
          <el-form-item label="模型名称" prop="modelName">
            <el-input v-model="formModel.modelName" placeholder="例如：gpt-5.4" />
          </el-form-item>

          <el-form-item label="温度" prop="temperature">
            <el-input-number v-model="formModel.temperature" :min="0" :max="2" :step="0.1" />
          </el-form-item>
        </div>

        <div class="split-grid">
          <el-form-item label="Max Tokens" prop="maxTokens">
            <el-input-number v-model="formModel.maxTokens" :min="1" :step="256" />
          </el-form-item>

          <el-form-item label="Top P" prop="topP">
            <el-input-number v-model="formModel.topP" :min="0" :max="1" :step="0.05" />
          </el-form-item>
        </div>

        <div class="split-grid">
          <el-form-item label="Presence Penalty" prop="presencePenalty">
            <el-input-number v-model="formModel.presencePenalty" :min="-2" :max="2" :step="0.1" />
          </el-form-item>

          <el-form-item label="Frequency Penalty" prop="frequencyPenalty">
            <el-input-number v-model="formModel.frequencyPenalty" :min="-2" :max="2" :step="0.1" />
          </el-form-item>
        </div>

        <el-form-item label="扩展参数 JSON" prop="extraParamsText">
          <MonacoCodeEditor
            v-model="formModel.extraParamsText"
            language="json"
            :height="280"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="table-actions">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="saving" @click="submitMcp">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>
