<script setup lang="ts">
import { computed, defineAsyncComponent, reactive, ref, watch } from 'vue';
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus';

import { getErrorMessage } from '@/api/http';
import { skillsApi } from '@/api/resources';
import AppSectionHeader from '@/components/AppSectionHeader.vue';
import { mockSkills } from '@/data/mock';
import type { CliTool, Skill } from '@/types/resources';

const MonacoCodeEditor = defineAsyncComponent(() => import('@/components/MonacoCodeEditor.vue'));

type FilterTool = 'all' | CliTool;
type DialogMode = 'create' | 'edit';

interface SkillFormModel {
  name: string;
  description: string;
  cliTool: CliTool;
  triggerCommand: string;
  scriptLanguage: string;
  scriptContent: string;
  tags: string[];
}

const cliToolOptions: CliTool[] = ['codex', 'cludea', 'opencode'];
const scriptLanguageOptions = [
  { label: 'Markdown', value: 'markdown' },
  { label: 'Shell', value: 'bash' },
  { label: 'Python', value: 'python' },
  { label: 'JSON', value: 'json' },
  { label: 'Text', value: 'text' },
];

const skills = ref<Skill[]>([]);
const loading = ref(false);
const saving = ref(false);
const warningMessage = ref('');
const usingMockData = ref(false);
const filterTool = ref<FilterTool>('all');
const selectedSkillId = ref('');
const dialogVisible = ref(false);
const dialogMode = ref<DialogMode>('create');
const editingSkillId = ref('');
const formRef = ref<FormInstance>();

const formModel = reactive<SkillFormModel>({
  name: '',
  description: '',
  cliTool: 'codex',
  triggerCommand: '',
  scriptLanguage: 'markdown',
  scriptContent: '',
  tags: [],
});

const formRules: FormRules<SkillFormModel> = {
  name: [
    {
      validator: (_rule, value: string, callback) => {
        if (!value?.trim()) {
          callback(new Error('请输入 Skill 名称'));
          return;
        }
        callback();
      },
      trigger: ['blur', 'change'],
    },
  ],
  cliTool: [{ required: true, message: '请选择所属 CLI 工具', trigger: 'change' }],
  triggerCommand: [{ required: true, message: '请输入触发命令', trigger: 'blur' }],
  scriptContent: [{ required: true, message: '请输入脚本内容', trigger: 'blur' }],
};

const filteredSkills = computed(() =>
  filterTool.value === 'all' ? skills.value : skills.value.filter((item) => item.cliTool === filterTool.value),
);

const selectedSkill = computed(
  () => filteredSkills.value.find((item) => item.id === selectedSkillId.value) ?? filteredSkills.value[0] ?? null,
);

const dialogTitle = computed(() => (dialogMode.value === 'create' ? '新建 Skill' : '编辑 Skill'));
const skillEditorLanguage = computed(() => {
  if (formModel.scriptLanguage === 'bash') {
    return 'shell';
  }
  if (formModel.scriptLanguage === 'text') {
    return 'plaintext';
  }
  return formModel.scriptLanguage;
});

const hasRealBackend = computed(() => !usingMockData.value);

function resetForm() {
  formModel.name = '';
  formModel.description = '';
  formModel.cliTool = 'codex';
  formModel.triggerCommand = '';
  formModel.scriptLanguage = 'markdown';
  formModel.scriptContent = '';
  formModel.tags = [];
}

function populateForm(skill?: Skill) {
  if (!skill) {
    resetForm();
    return;
  }

  formModel.name = skill.name;
  formModel.description = skill.description;
  formModel.cliTool = skill.cliTool;
  formModel.triggerCommand = skill.triggerCommand;
  formModel.scriptLanguage = skill.scriptLanguage;
  formModel.scriptContent = skill.scriptContent;
  formModel.tags = [...skill.tags];
}

function syncSelection(preferredId?: string) {
  if (preferredId && filteredSkills.value.some((item) => item.id === preferredId)) {
    selectedSkillId.value = preferredId;
    return;
  }

  if (filteredSkills.value.some((item) => item.id === selectedSkillId.value)) {
    return;
  }

  selectedSkillId.value = filteredSkills.value[0]?.id ?? '';
}

async function loadSkills(preferredId?: string) {
  loading.value = true;
  warningMessage.value = '';

  try {
    skills.value = await skillsApi.list();
    usingMockData.value = false;
  } catch (error) {
    skills.value = mockSkills;
    usingMockData.value = true;
    warningMessage.value = getErrorMessage(
      error,
      'Skills 接口暂不可用，当前显示本地示例数据，已禁用新增、编辑和删除操作。',
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
  editingSkillId.value = '';
  resetForm();
  dialogVisible.value = true;
}

function openEditDialog(skill: Skill) {
  if (!hasRealBackend.value || !skill.isWritable) {
    return;
  }

  dialogMode.value = 'edit';
  editingSkillId.value = skill.id;
  populateForm(skill);
  dialogVisible.value = true;
}

function buildPayload() {
  const current = skills.value.find((item) => item.id === editingSkillId.value);

  return {
    name: formModel.name.trim(),
    description: formModel.description.trim(),
    cli_tool: formModel.cliTool,
    trigger_command: formModel.triggerCommand.trim(),
    script_language: formModel.scriptLanguage.trim() || 'markdown',
    script_content: formModel.scriptContent,
    tags: formModel.tags.map((item) => item.trim()).filter(Boolean),
    source_kind: current?.sourceKind ?? 'managed',
    source_path: current?.sourcePath ?? '',
    is_writable: current?.isWritable ?? true,
  };
}

async function submitSkill() {
  if (!formRef.value) {
    return;
  }

  await formRef.value.validate();
  saving.value = true;

  try {
    const payload = buildPayload();

    if (dialogMode.value === 'create') {
      const created = await skillsApi.create(payload);
      filterTool.value = created.cliTool;
      await loadSkills(created.id);
      ElMessage.success(`Skill ${created.name} 已创建`);
    } else {
      const updated = await skillsApi.update(editingSkillId.value, payload);
      filterTool.value = updated.cliTool;
      await loadSkills(updated.id);
      ElMessage.success(`Skill ${updated.name} 已保存`);
    }

    dialogVisible.value = false;
  } catch (error) {
    ElMessage.error(getErrorMessage(error, 'Skill 保存失败，请检查输入后重试。'));
  } finally {
    saving.value = false;
  }
}

async function removeSkill(skill: Skill) {
  if (!hasRealBackend.value || !skill.isWritable) {
    return;
  }

  try {
    await ElMessageBox.confirm(`将删除 Skill「${skill.name}」，此操作无法撤销。`, '删除确认', {
      type: 'warning',
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
    });
  } catch {
    return;
  }

  try {
    await skillsApi.remove(skill.id);
    ElMessage.success(`Skill ${skill.name} 已删除`);
    await loadSkills();
  } catch (error) {
    ElMessage.error(getErrorMessage(error, 'Skill 删除失败，请稍后重试。'));
  }
}

function handleRowClick(skill: Skill) {
  selectedSkillId.value = skill.id;
}

watch(filterTool, () => {
  syncSelection();
});

loadSkills();
</script>

<template>
  <div class="page-stack">
    <AppSectionHeader
      title="Skills 管理"
      description="统一查看 managed 与外部发现的 Skills；外部来源以只读方式展示，避免误改真实配置。"
    >
      <div class="skills-toolbar">
        <el-select v-model="filterTool" style="width: 160px">
          <el-option label="全部 CLI" value="all" />
          <el-option v-for="tool in cliToolOptions" :key="tool" :label="tool" :value="tool" />
        </el-select>
        <el-button type="primary" :disabled="!hasRealBackend" @click="openCreateDialog">新建 Skill</el-button>
      </div>
    </AppSectionHeader>

    <el-alert v-if="warningMessage" :title="warningMessage" type="warning" show-icon :closable="false" />

    <div class="split-grid">
      <el-card shadow="never">
        <template #header>
          <div class="card-header">
            <strong>Skills 列表</strong>
            <span>{{ filteredSkills.length }} 条</span>
          </div>
        </template>

        <el-table
          v-loading="loading"
          :data="filteredSkills"
          row-key="id"
          empty-text="当前筛选条件下暂无 Skill"
          @row-click="handleRowClick"
        >
          <el-table-column prop="name" label="名称" min-width="180" />
          <el-table-column prop="description" label="描述" min-width="220" show-overflow-tooltip />
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
          <el-table-column prop="triggerCommand" label="触发命令" min-width="150" />
          <el-table-column label="标签" min-width="160">
            <template #default="{ row }">
              <div class="tag-row">
                <el-tag v-for="tag in row.tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
                <span v-if="row.tags.length === 0" class="muted-text">无标签</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="updatedAt" label="更新时间" min-width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button text type="primary" @click.stop="handleRowClick(row)">详情</el-button>
                <el-button text type="primary" :disabled="!row.isWritable || !hasRealBackend" @click.stop="openEditDialog(row)">
                  编辑
                </el-button>
                <el-button text type="danger" :disabled="!row.isWritable || !hasRealBackend" @click.stop="removeSkill(row)">
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
            <strong>Skill 详情</strong>
            <el-tag v-if="selectedSkill" :type="selectedSkill.isWritable ? 'success' : 'info'" size="small">
              {{ selectedSkill.isWritable ? '可写' : '只读' }}
            </el-tag>
          </div>
        </template>

        <div v-if="selectedSkill" class="page-stack">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="名称">{{ selectedSkill.name }}</el-descriptions-item>
            <el-descriptions-item label="所属 CLI">{{ selectedSkill.cliTool }}</el-descriptions-item>
            <el-descriptions-item label="触发命令">{{ selectedSkill.triggerCommand }}</el-descriptions-item>
            <el-descriptions-item label="脚本语言">{{ selectedSkill.scriptLanguage }}</el-descriptions-item>
            <el-descriptions-item label="来源类型">{{ selectedSkill.sourceKind }}</el-descriptions-item>
            <el-descriptions-item label="来源路径">{{ selectedSkill.sourcePath || '未设置' }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ selectedSkill.createdAt || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="更新时间">{{ selectedSkill.updatedAt }}</el-descriptions-item>
            <el-descriptions-item label="描述">{{ selectedSkill.description || '暂无描述' }}</el-descriptions-item>
            <el-descriptions-item label="标签">
              <div class="tag-row">
                <el-tag v-for="tag in selectedSkill.tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
                <span v-if="selectedSkill.tags.length === 0" class="muted-text">无标签</span>
              </div>
            </el-descriptions-item>
          </el-descriptions>

          <div class="card-header">
            <strong>脚本内容</strong>
            <div class="table-actions">
              <el-button text type="primary" :disabled="!selectedSkill.isWritable || !hasRealBackend" @click="openEditDialog(selectedSkill)">
                编辑
              </el-button>
              <el-button text type="danger" :disabled="!selectedSkill.isWritable || !hasRealBackend" @click="removeSkill(selectedSkill)">
                删除
              </el-button>
            </div>
          </div>

          <pre class="code-surface">{{ selectedSkill.scriptContent || '# 暂无脚本内容' }}</pre>
        </div>

        <el-empty v-else description="请选择一个 Skill 查看详情" />
      </el-card>
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="760px" destroy-on-close>
      <el-form ref="formRef" :model="formModel" :rules="formRules" label-position="top" class="page-stack">
        <div class="split-grid">
          <el-form-item label="名称" prop="name">
            <el-input v-model="formModel.name" placeholder="例如：Design Review" />
          </el-form-item>

          <el-form-item label="所属 CLI 工具" prop="cliTool">
            <el-select v-model="formModel.cliTool">
              <el-option v-for="tool in cliToolOptions" :key="tool" :label="tool" :value="tool" />
            </el-select>
          </el-form-item>
        </div>

        <el-form-item label="描述" prop="description">
          <el-input v-model="formModel.description" type="textarea" :rows="3" placeholder="说明这个 Skill 的用途与使用场景" />
        </el-form-item>

        <div class="split-grid">
          <el-form-item label="触发命令" prop="triggerCommand">
            <el-input v-model="formModel.triggerCommand" placeholder="例如：/design-review" />
          </el-form-item>

          <el-form-item label="脚本语言" prop="scriptLanguage">
            <el-select v-model="formModel.scriptLanguage">
              <el-option
                v-for="option in scriptLanguageOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>
        </div>

        <el-form-item label="标签" prop="tags">
          <el-select
            v-model="formModel.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="输入后回车，可添加多个标签"
          />
        </el-form-item>

        <el-form-item label="脚本内容" prop="scriptContent">
          <MonacoCodeEditor
            v-model="formModel.scriptContent"
            :language="skillEditorLanguage"
            :height="360"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="table-actions">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="saving" @click="submitSkill">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>
