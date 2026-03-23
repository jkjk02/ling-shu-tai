<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, reactive, ref, watch } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';

import { agentsApi, workflowsApi } from '@/api/resources';
import { getErrorMessage } from '@/api/http';
import AppSectionHeader from '@/components/AppSectionHeader.vue';
import { mockAgents, mockWorkflows } from '@/data/mock';
import type { Agent, Workflow, WorkflowDraft, WorkflowEdge, WorkflowNode } from '@/types/resources';

type NodeKind = 'start' | 'task' | 'review' | 'decision' | 'end';
type NodeStatus = 'ready' | 'running' | 'blocked' | 'done';

interface WorkflowNodeConfig {
  kind: NodeKind;
  stage: string;
  status: NodeStatus;
  notes: string;
}

interface NodeTemplate {
  kind: NodeKind;
  label: string;
  description: string;
  stage: string;
  accent: string;
}

interface DrawableEdge {
  id: string;
  label: string;
  condition: string;
  path: string;
  midX: number;
  midY: number;
  source: string;
  target: string;
}

const GRID_SIZE = 24;
const NODE_WIDTH = 220;
const NODE_HEIGHT = 112;
const MIN_ZOOM = 0.35;
const MAX_ZOOM = 1.8;

const workflowTemplates: NodeTemplate[] = [
  { kind: 'start', label: '开始', description: '定义入口与目标上下文。', stage: 'intake', accent: '#1b7f6b' },
  { kind: 'task', label: '执行', description: '绑定 Agent 执行主要工作。', stage: 'implementation', accent: '#2a6ad8' },
  { kind: 'review', label: '评审', description: '人工或模型评审结果。', stage: 'review', accent: '#b06a00' },
  { kind: 'decision', label: '决策', description: '条件分支与路由判断。', stage: 'decision', accent: '#7d35c7' },
  { kind: 'end', label: '结束', description: '收敛交付或关闭流程。', stage: 'handoff', accent: '#5a6270' },
];

const nodeStatusOptions: NodeStatus[] = ['ready', 'running', 'blocked', 'done'];

const workflows = ref<Workflow[]>([]);
const agents = ref<Agent[]>([]);
const loading = ref(false);
const saving = ref(false);
const warningMessage = ref('');
const usingMockData = ref(false);
const selectedWorkflowId = ref('');
const selectedNodeId = ref('');
const selectedEdgeId = ref('');
const canvasBoardRef = ref<HTMLElement>();

const editor = reactive<WorkflowDraft>(createEmptyWorkflowDraft());

const connectState = reactive({
  sourceNodeId: '',
});

const interactionState = reactive({
  mode: '' as '' | 'pan' | 'node',
  nodeId: '',
  startMouseX: 0,
  startMouseY: 0,
  originX: 0,
  originY: 0,
  viewportX: 0,
  viewportY: 0,
});

const selectedWorkflow = computed(() => {
  if (!selectedWorkflowId.value) {
    return null;
  }
  return workflows.value.find((item) => item.id === selectedWorkflowId.value) ?? null;
});

const selectedNode = computed(
  () => editor.nodes.find((node) => node.id === selectedNodeId.value) ?? editor.nodes[0] ?? null,
);

const selectedNodeConfig = computed(() => (selectedNode.value ? ensureNodeConfig(selectedNode.value) : null));

const selectedEdge = computed(
  () => editor.edges.find((edge) => edge.id === selectedEdgeId.value) ?? editor.edges[0] ?? null,
);

const agentNameMap = computed(() => new Map(agents.value.map((item) => [item.id, item.name])));
const hasRealBackend = computed(() => !usingMockData.value);
const isCreateMode = computed(() => !selectedWorkflowId.value);

const canvasSceneStyle = computed(() => ({
  transform: `translate(${editor.viewport.x}px, ${editor.viewport.y}px) scale(${editor.viewport.zoom})`,
}));

const sceneSize = computed(() => {
  const bounds = getNodeBounds(editor.nodes);
  return {
    width: Math.max(1800, bounds.maxX + 360),
    height: Math.max(1200, bounds.maxY + 280),
  };
});

const drawableEdges = computed<DrawableEdge[]>(() =>
  editor.edges
    .map((edge) => {
      const source = editor.nodes.find((node) => node.id === edge.source);
      const target = editor.nodes.find((node) => node.id === edge.target);
      if (!source || !target) {
        return null;
      }

      const x1 = source.x + NODE_WIDTH;
      const y1 = source.y + NODE_HEIGHT / 2;
      const x2 = target.x;
      const y2 = target.y + NODE_HEIGHT / 2;
      const distance = Math.max(Math.abs(x2 - x1) * 0.42, 72);
      const path = `M ${x1} ${y1} C ${x1 + distance} ${y1}, ${x2 - distance} ${y2}, ${x2} ${y2}`;

      return {
        id: edge.id,
        label: edge.label?.trim() ?? '',
        condition: edge.condition?.trim() ?? '',
        path,
        midX: (x1 + x2) / 2,
        midY: (y1 + y2) / 2,
        source: edge.source,
        target: edge.target,
      };
    })
    .filter((edge): edge is DrawableEdge => edge !== null),
);

const workflowWarnings = computed(() => {
  const warnings: string[] = [];
  const nodeIds = new Set(editor.nodes.map((node) => node.id));

  if (!editor.name.trim()) {
    warnings.push('Workflow 名称为空。');
  }
  if (editor.nodes.length === 0) {
    warnings.push('当前流程还没有任何节点。');
  }

  const startNodes = editor.nodes.filter((node) => ensureNodeConfig(node).kind === 'start');
  const endNodes = editor.nodes.filter((node) => ensureNodeConfig(node).kind === 'end');
  if (editor.nodes.length > 0 && startNodes.length === 0) {
    warnings.push('建议至少设置一个开始节点。');
  }
  if (editor.nodes.length > 0 && endNodes.length === 0) {
    warnings.push('建议至少设置一个结束节点。');
  }

  const nodesWithoutAgent = editor.nodes
    .filter((node) => {
      const kind = ensureNodeConfig(node).kind;
      return kind !== 'start' && kind !== 'end' && !node.agentId;
    })
    .map((node) => node.label || node.id);
  if (nodesWithoutAgent.length) {
    warnings.push(`存在未绑定 Agent 的节点：${nodesWithoutAgent.join('、')}`);
  }

  const isolatedNodes = editor.nodes
    .filter((node) => !editor.edges.some((edge) => edge.source === node.id || edge.target === node.id))
    .map((node) => node.label || node.id);
  if (editor.nodes.length > 1 && isolatedNodes.length) {
    warnings.push(`存在未连线节点：${isolatedNodes.join('、')}`);
  }

  const invalidEdges = editor.edges.filter(
    (edge) => !nodeIds.has(edge.source) || !nodeIds.has(edge.target) || edge.source === edge.target,
  );
  if (invalidEdges.length) {
    warnings.push(`存在 ${invalidEdges.length} 条无效连线。`);
  }

  if (hasDirectedCycle(editor.nodes, editor.edges)) {
    warnings.push('当前流程存在环路；若这不是有意设计，建议重新整理编排顺序。');
  }

  return warnings;
});

function createEmptyWorkflowDraft(): WorkflowDraft {
  return {
    name: '',
    description: '',
    nodes: [],
    edges: [],
    viewport: {
      x: 0,
      y: 0,
      zoom: 1,
    },
  };
}

function normalizeNode(node: WorkflowNode): WorkflowNode {
  return {
    ...node,
    x: Number.isFinite(node.x) ? node.x : 0,
    y: Number.isFinite(node.y) ? node.y : 0,
    config: toNodeConfigRecord(normalizeNodeConfig(node.config)),
  };
}

function normalizeNodeConfig(config: Record<string, unknown> | undefined): WorkflowNodeConfig {
  const raw = config ?? {};
  const kind = raw.kind;
  const status = raw.status;
  return {
    kind: kind === 'start' || kind === 'task' || kind === 'review' || kind === 'decision' || kind === 'end' ? kind : 'task',
    stage: typeof raw.stage === 'string' ? raw.stage : '',
    status: status === 'ready' || status === 'running' || status === 'blocked' || status === 'done' ? status : 'ready',
    notes: typeof raw.notes === 'string' ? raw.notes : '',
  };
}

function ensureNodeConfig(node: WorkflowNode): WorkflowNodeConfig {
  const config = normalizeNodeConfig(node.config);
  node.config = toNodeConfigRecord(config);
  return node.config as unknown as WorkflowNodeConfig;
}

function toNodeConfigRecord(config: WorkflowNodeConfig): Record<string, unknown> {
  return { ...config };
}

function cloneWorkflow(workflow: Workflow): WorkflowDraft {
  return {
    id: workflow.id,
    name: workflow.name,
    description: workflow.description,
    nodes: workflow.nodes.map((node) => normalizeNode({ ...node })),
    edges: workflow.edges.map((edge) => ({ ...edge, condition: edge.condition ?? null })),
    viewport: { ...workflow.viewport },
  };
}

function applyEditorDraft(draft: WorkflowDraft) {
  editor.id = draft.id;
  editor.name = draft.name;
  editor.description = draft.description;
  editor.nodes = draft.nodes.map((node) => normalizeNode({ ...node }));
  editor.edges = draft.edges.map((edge) => ({ ...edge, condition: edge.condition ?? null }));
  editor.viewport = { ...draft.viewport };
  selectedNodeId.value = editor.nodes[0]?.id ?? '';
  selectedEdgeId.value = editor.edges[0]?.id ?? '';
  connectState.sourceNodeId = '';
}

function syncSelection(preferredId?: string) {
  if (preferredId && workflows.value.some((item) => item.id === preferredId)) {
    selectedWorkflowId.value = preferredId;
    return;
  }

  if (workflows.value.some((item) => item.id === selectedWorkflowId.value)) {
    return;
  }

  selectedWorkflowId.value = workflows.value[0]?.id ?? '';
}

function loadSelectedWorkflowIntoEditor() {
  if (!selectedWorkflow.value) {
    applyEditorDraft(createEmptyWorkflowDraft());
    return;
  }
  applyEditorDraft(cloneWorkflow(selectedWorkflow.value));
}

async function loadPageData(preferredId?: string) {
  loading.value = true;
  warningMessage.value = '';

  try {
    const [workflowItems, agentItems] = await Promise.all([workflowsApi.list(), agentsApi.list()]);
    workflows.value = workflowItems;
    agents.value = agentItems;
    usingMockData.value = false;
  } catch (error) {
    workflows.value = mockWorkflows;
    agents.value = mockAgents;
    usingMockData.value = true;
    warningMessage.value = getErrorMessage(
      error,
      'Workflow 接口暂不可用，当前显示本地示例数据，已禁用保存和删除操作。',
    );
  } finally {
    syncSelection(preferredId);
    loadSelectedWorkflowIntoEditor();
    await nextTick();
    loading.value = false;
  }
}

function selectWorkflow(workflow: Workflow) {
  selectedWorkflowId.value = workflow.id;
  loadSelectedWorkflowIntoEditor();
}

function startNewWorkflow() {
  selectedWorkflowId.value = '';
  applyEditorDraft(createEmptyWorkflowDraft());
}

function makeLocalId(prefix: string) {
  return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`;
}

function snapToGrid(value: number) {
  return Math.round(value / GRID_SIZE) * GRID_SIZE;
}

function addNodeFromTemplate(template: NodeTemplate) {
  const position = getNextNodePosition();
  const node: WorkflowNode = {
    id: makeLocalId('node'),
    label: `${template.label} ${editor.nodes.filter((item) => ensureNodeConfig(item).kind === template.kind).length + 1}`,
    agentId: template.kind === 'start' || template.kind === 'end' ? null : agents.value[0]?.id ?? null,
    x: position.x,
    y: position.y,
    config: {
      kind: template.kind,
      stage: template.stage,
      status: 'ready',
      notes: template.description,
    },
  };
  editor.nodes.push(node);
  selectedNodeId.value = node.id;
}

function duplicateNode(node: WorkflowNode) {
  const config = ensureNodeConfig(node);
  const next: WorkflowNode = {
    id: makeLocalId('node'),
    label: `${node.label} Copy`,
    agentId: node.agentId,
    x: snapToGrid(node.x + GRID_SIZE * 2),
    y: snapToGrid(node.y + GRID_SIZE * 2),
    config: { ...config },
  };
  editor.nodes.push(next);
  selectedNodeId.value = next.id;
}

function getNextNodePosition() {
  const count = editor.nodes.length;
  return {
    x: snapToGrid(96 + (count % 3) * 280),
    y: snapToGrid(96 + Math.floor(count / 3) * 180),
  };
}

function removeNode(nodeId: string) {
  editor.nodes = editor.nodes.filter((node) => node.id !== nodeId);
  editor.edges = editor.edges.filter((edge) => edge.source !== nodeId && edge.target !== nodeId);
  if (selectedNodeId.value === nodeId) {
    selectedNodeId.value = editor.nodes[0]?.id ?? '';
  }
  if (!editor.edges.some((edge) => edge.id === selectedEdgeId.value)) {
    selectedEdgeId.value = editor.edges[0]?.id ?? '';
  }
  if (connectState.sourceNodeId === nodeId) {
    connectState.sourceNodeId = '';
  }
}

function beginConnection(sourceNodeId: string) {
  connectState.sourceNodeId = connectState.sourceNodeId === sourceNodeId ? '' : sourceNodeId;
}

function completeConnection(targetNodeId: string) {
  if (!connectState.sourceNodeId) {
    return;
  }
  if (connectState.sourceNodeId === targetNodeId) {
    ElMessage.warning('起点和终点不能相同');
    return;
  }
  const exists = editor.edges.some(
    (edge) => edge.source === connectState.sourceNodeId && edge.target === targetNodeId,
  );
  if (exists) {
    ElMessage.warning('该连线已存在');
    connectState.sourceNodeId = '';
    return;
  }

  const edge: WorkflowEdge = {
    id: makeLocalId('edge'),
    source: connectState.sourceNodeId,
    target: targetNodeId,
    label: '',
    condition: null,
  };
  editor.edges.push(edge);
  selectedEdgeId.value = edge.id;
  connectState.sourceNodeId = '';
}

function removeEdge(edgeId: string) {
  editor.edges = editor.edges.filter((edge) => edge.id !== edgeId);
  if (selectedEdgeId.value === edgeId) {
    selectedEdgeId.value = editor.edges[0]?.id ?? '';
  }
}

function getNodeKind(node: WorkflowNode) {
  return ensureNodeConfig(node).kind;
}

function getNodeStage(node: WorkflowNode) {
  return ensureNodeConfig(node).stage || '未分组';
}

function getNodeStatus(node: WorkflowNode) {
  return ensureNodeConfig(node).status;
}

function getNodeNotes(node: WorkflowNode) {
  return ensureNodeConfig(node).notes;
}

function buildPayload() {
  return {
    name: editor.name.trim(),
    description: editor.description.trim(),
    nodes: editor.nodes.map((node) => ({
      id: node.id,
      label: node.label.trim(),
      agent_id: node.agentId,
      position: {
        x: snapToGrid(node.x),
        y: snapToGrid(node.y),
      },
      config: { ...ensureNodeConfig(node) },
    })),
    edges: editor.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.label?.trim() || '',
      condition: edge.condition?.trim() || null,
    })),
    viewport: {
      x: editor.viewport.x,
      y: editor.viewport.y,
      zoom: Number(editor.viewport.zoom.toFixed(2)),
    },
  };
}

async function saveWorkflow() {
  if (!hasRealBackend.value) {
    return;
  }
  if (!editor.name.trim()) {
    ElMessage.warning('请输入 Workflow 名称');
    return;
  }

  saving.value = true;
  try {
    const payload = buildPayload();

    if (isCreateMode.value) {
      const created = await workflowsApi.create(payload);
      await loadPageData(created.id);
      ElMessage.success(`Workflow ${created.name} 已创建`);
    } else {
      const updated = await workflowsApi.update(selectedWorkflowId.value, payload);
      await loadPageData(updated.id);
      ElMessage.success(`Workflow ${updated.name} 已保存`);
    }
  } catch (error) {
    ElMessage.error(getErrorMessage(error, 'Workflow 保存失败，请检查节点与连线配置。'));
  } finally {
    saving.value = false;
  }
}

async function deleteWorkflow(workflowId: string, workflowName: string) {
  if (!hasRealBackend.value) {
    return;
  }
  try {
    await ElMessageBox.confirm(`将删除 Workflow「${workflowName}」，此操作无法撤销。`, '删除确认', {
      type: 'warning',
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
    });
  } catch {
    return;
  }

  try {
    await workflowsApi.remove(workflowId);
    ElMessage.success(`Workflow ${workflowName} 已删除`);
    await loadPageData();
  } catch (error) {
    ElMessage.error(getErrorMessage(error, 'Workflow 删除失败，请稍后重试。'));
  }
}

function startNodeDrag(node: WorkflowNode, event: MouseEvent) {
  interactionState.mode = 'node';
  interactionState.nodeId = node.id;
  interactionState.startMouseX = event.clientX;
  interactionState.startMouseY = event.clientY;
  interactionState.originX = node.x;
  interactionState.originY = node.y;
  window.addEventListener('mousemove', handleInteractionMove);
  window.addEventListener('mouseup', stopInteraction);
}

function startCanvasPan(event: MouseEvent) {
  const target = event.target as HTMLElement;
  if (target.closest('.workflow-node') || target.closest('.workflow-edge-hit') || target.closest('.workflow-edge-label')) {
    return;
  }
  interactionState.mode = 'pan';
  interactionState.startMouseX = event.clientX;
  interactionState.startMouseY = event.clientY;
  interactionState.viewportX = editor.viewport.x;
  interactionState.viewportY = editor.viewport.y;
  window.addEventListener('mousemove', handleInteractionMove);
  window.addEventListener('mouseup', stopInteraction);
}

function handleInteractionMove(event: MouseEvent) {
  if (interactionState.mode === 'node') {
    const node = editor.nodes.find((item) => item.id === interactionState.nodeId);
    if (!node) {
      return;
    }
    const dx = (event.clientX - interactionState.startMouseX) / editor.viewport.zoom;
    const dy = (event.clientY - interactionState.startMouseY) / editor.viewport.zoom;
    node.x = snapToGrid(Math.max(0, interactionState.originX + dx));
    node.y = snapToGrid(Math.max(0, interactionState.originY + dy));
    return;
  }

  if (interactionState.mode === 'pan') {
    editor.viewport.x = interactionState.viewportX + (event.clientX - interactionState.startMouseX);
    editor.viewport.y = interactionState.viewportY + (event.clientY - interactionState.startMouseY);
  }
}

function stopInteraction() {
  interactionState.mode = '';
  interactionState.nodeId = '';
  window.removeEventListener('mousemove', handleInteractionMove);
  window.removeEventListener('mouseup', stopInteraction);
}

function handleCanvasWheel(event: WheelEvent) {
  event.preventDefault();
  const board = canvasBoardRef.value;
  if (!board) {
    return;
  }
  const rect = board.getBoundingClientRect();
  const pointerX = event.clientX - rect.left;
  const pointerY = event.clientY - rect.top;
  const nextZoom = clamp(editor.viewport.zoom + (event.deltaY < 0 ? 0.1 : -0.1), MIN_ZOOM, MAX_ZOOM);
  const worldX = (pointerX - editor.viewport.x) / editor.viewport.zoom;
  const worldY = (pointerY - editor.viewport.y) / editor.viewport.zoom;
  editor.viewport.x = pointerX - worldX * nextZoom;
  editor.viewport.y = pointerY - worldY * nextZoom;
  editor.viewport.zoom = Number(nextZoom.toFixed(2));
}

function zoomBy(step: number) {
  editor.viewport.zoom = Number(clamp(editor.viewport.zoom + step, MIN_ZOOM, MAX_ZOOM).toFixed(2));
}

function resetViewport() {
  editor.viewport.x = 0;
  editor.viewport.y = 0;
  editor.viewport.zoom = 1;
}

function fitView() {
  const board = canvasBoardRef.value;
  if (!board || editor.nodes.length === 0) {
    resetViewport();
    return;
  }
  const rect = board.getBoundingClientRect();
  const bounds = getNodeBounds(editor.nodes);
  const width = Math.max(bounds.maxX - bounds.minX + NODE_WIDTH + 96, 320);
  const height = Math.max(bounds.maxY - bounds.minY + NODE_HEIGHT + 96, 220);
  const zoom = clamp(Math.min(rect.width / width, rect.height / height, 1.25), MIN_ZOOM, MAX_ZOOM);
  editor.viewport.zoom = Number(zoom.toFixed(2));
  editor.viewport.x = Math.round((rect.width - width * zoom) / 2 - bounds.minX * zoom + 48);
  editor.viewport.y = Math.round((rect.height - height * zoom) / 2 - bounds.minY * zoom + 48);
}

function autoLayout() {
  if (editor.nodes.length === 0) {
    return;
  }

  const incoming = new Map<string, number>(editor.nodes.map((node) => [node.id, 0]));
  const outgoing = new Map<string, string[]>(editor.nodes.map((node) => [node.id, []]));

  for (const edge of editor.edges) {
    incoming.set(edge.target, (incoming.get(edge.target) ?? 0) + 1);
    outgoing.set(edge.source, [...(outgoing.get(edge.source) ?? []), edge.target]);
  }

  const queue = editor.nodes.filter((node) => (incoming.get(node.id) ?? 0) === 0).map((node) => node.id);
  const layers = new Map<string, number>();

  while (queue.length) {
    const nodeId = queue.shift()!;
    const currentLayer = layers.get(nodeId) ?? 0;
    for (const target of outgoing.get(nodeId) ?? []) {
      const nextLayer = Math.max(layers.get(target) ?? 0, currentLayer + 1);
      layers.set(target, nextLayer);
      incoming.set(target, (incoming.get(target) ?? 1) - 1);
      if ((incoming.get(target) ?? 0) === 0) {
        queue.push(target);
      }
    }
  }

  let fallbackLayer = Math.max(...layers.values(), 0);
  for (const node of editor.nodes) {
    if (!layers.has(node.id)) {
      fallbackLayer += 1;
      layers.set(node.id, fallbackLayer);
    }
  }

  const grouped = new Map<number, WorkflowNode[]>();
  for (const node of editor.nodes) {
    const layer = layers.get(node.id) ?? 0;
    grouped.set(layer, [...(grouped.get(layer) ?? []), node]);
  }

  const orderedLayers = [...grouped.keys()].sort((a, b) => a - b);
  orderedLayers.forEach((layer) => {
    const nodes = grouped.get(layer) ?? [];
    nodes.forEach((node, index) => {
      node.x = snapToGrid(96 + layer * 320);
      node.y = snapToGrid(96 + index * 176);
    });
  });

  nextTick(() => fitView());
}

function selectEdge(edgeId: string) {
  selectedEdgeId.value = edgeId;
}

function getNodeBounds(nodes: WorkflowNode[]) {
  if (nodes.length === 0) {
    return { minX: 0, minY: 0, maxX: 0, maxY: 0 };
  }
  return nodes.reduce(
    (acc, node) => ({
      minX: Math.min(acc.minX, node.x),
      minY: Math.min(acc.minY, node.y),
      maxX: Math.max(acc.maxX, node.x),
      maxY: Math.max(acc.maxY, node.y),
    }),
    { minX: nodes[0].x, minY: nodes[0].y, maxX: nodes[0].x, maxY: nodes[0].y },
  );
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max);
}

function hasDirectedCycle(nodes: WorkflowNode[], edges: WorkflowEdge[]) {
  const outgoing = new Map<string, string[]>(nodes.map((node) => [node.id, []]));
  for (const edge of edges) {
    if (outgoing.has(edge.source)) {
      outgoing.set(edge.source, [...(outgoing.get(edge.source) ?? []), edge.target]);
    }
  }

  const visiting = new Set<string>();
  const visited = new Set<string>();

  const dfs = (nodeId: string): boolean => {
    if (visiting.has(nodeId)) {
      return true;
    }
    if (visited.has(nodeId)) {
      return false;
    }
    visiting.add(nodeId);
    for (const nextId of outgoing.get(nodeId) ?? []) {
      if (dfs(nextId)) {
        return true;
      }
    }
    visiting.delete(nodeId);
    visited.add(nodeId);
    return false;
  };

  return nodes.some((node) => dfs(node.id));
}

watch(selectedWorkflowId, () => {
  loadSelectedWorkflowIntoEditor();
});

onBeforeUnmount(() => {
  stopInteraction();
});

loadPageData();
</script>

<template>
  <div class="page-stack">
    <AppSectionHeader
      title="Workflows 编排"
      description="把最小工作流编辑器提升成更接近真实编排器的体验：节点模板、缩放平移、连线条件、校验提示与结构化节点配置。"
    >
      <div class="skills-toolbar">
        <el-button data-testid="workflow-new-button" @click="startNewWorkflow">新建 Workflow</el-button>
        <el-button data-testid="workflow-save-button" type="primary" :disabled="!hasRealBackend" :loading="saving" @click="saveWorkflow">保存 Workflow</el-button>
        <el-button
          v-if="selectedWorkflow"
          data-testid="workflow-delete-button"
          type="danger"
          plain
          :disabled="!hasRealBackend"
          @click="deleteWorkflow(selectedWorkflow.id, selectedWorkflow.name)"
        >
          删除当前
        </el-button>
      </div>
    </AppSectionHeader>

    <el-alert v-if="warningMessage" :title="warningMessage" type="warning" show-icon :closable="false" />

    <div class="workflow-grid workflow-grid--expanded">
      <el-card shadow="never">
        <template #header>
          <div class="card-header">
            <strong>Workflow 列表</strong>
            <span>{{ workflows.length }} 条</span>
          </div>
        </template>

        <el-table data-testid="workflow-list-table" v-loading="loading" :data="workflows" row-key="id" empty-text="暂无 Workflow" @row-click="selectWorkflow">
          <el-table-column prop="name" label="名称" min-width="170" />
          <el-table-column prop="description" label="描述" min-width="220" show-overflow-tooltip />
          <el-table-column label="节点" width="90">
            <template #default="{ row }">{{ row.nodes.length }}</template>
          </el-table-column>
          <el-table-column label="连线" width="90">
            <template #default="{ row }">{{ row.edges.length }}</template>
          </el-table-column>
          <el-table-column prop="updatedAt" label="更新时间" min-width="170" />
        </el-table>
      </el-card>

      <div class="page-stack">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <strong>流程元数据</strong>
              <div class="table-actions">
                <el-tag size="small" :type="isCreateMode ? 'warning' : 'success'">
                  {{ isCreateMode ? '新建中' : '已加载' }}
                </el-tag>
                <el-tag v-if="connectState.sourceNodeId" size="small" type="danger">连线中</el-tag>
              </div>
            </div>
          </template>

          <div class="page-stack">
            <div class="split-grid">
              <el-form-item label="名称" class="form-item-reset">
                <el-input v-model="editor.name" data-testid="workflow-name-input" placeholder="例如：交付流水线" />
              </el-form-item>

              <el-form-item label="缩放" class="form-item-reset">
                <el-input-number v-model="editor.viewport.zoom" :min="MIN_ZOOM" :max="MAX_ZOOM" :step="0.1" style="width: 100%" />
              </el-form-item>
            </div>

            <el-form-item label="描述" class="form-item-reset">
              <el-input
                v-model="editor.description"
                data-testid="workflow-description-input"
                type="textarea"
                :rows="3"
                placeholder="描述这个 Workflow 的目标与适用场景"
              />
            </el-form-item>

            <div class="summary-stats">
              <div><span>节点数</span><strong>{{ editor.nodes.length }}</strong></div>
              <div><span>连线数</span><strong>{{ editor.edges.length }}</strong></div>
              <div><span>告警数</span><strong>{{ workflowWarnings.length }}</strong></div>
            </div>

            <div class="workflow-warning-list">
              <div v-for="warning in workflowWarnings" :key="warning" class="workflow-warning-item">
                {{ warning }}
              </div>
              <div v-if="workflowWarnings.length === 0" class="workflow-warning-item workflow-warning-item--ok">
                当前流程未发现结构性告警。
              </div>
            </div>
          </div>
        </el-card>

        <el-card shadow="never" class="canvas-card">
          <template #header>
            <div class="card-header">
              <strong>编排画布</strong>
              <div class="table-actions">
                <el-button data-testid="workflow-fit-view-button" text @click="fitView">适配视图</el-button>
                <el-button data-testid="workflow-auto-layout-button" text @click="autoLayout">自动布局</el-button>
                <el-button text @click="zoomBy(-0.1)">缩小</el-button>
                <el-button text @click="zoomBy(0.1)">放大</el-button>
                <el-button text @click="resetViewport">重置</el-button>
              </div>
            </div>
          </template>

          <div class="workflow-studio">
            <aside class="workflow-palette">
              <div class="workflow-palette__head">
                <strong>节点模板</strong>
                <span>拖拽替代方案</span>
              </div>
              <button
                v-for="template in workflowTemplates"
                :key="template.kind"
                class="workflow-palette__item"
                type="button"
                :data-testid="`workflow-template-${template.kind}`"
                :style="{ '--workflow-accent': template.accent }"
                @click="addNodeFromTemplate(template)"
              >
                <strong>{{ template.label }}</strong>
                <span>{{ template.description }}</span>
              </button>
              <div class="workflow-palette__note">
                先点“输出端口”，再点目标节点的“输入端口”即可连线。
              </div>
            </aside>

            <div
              ref="canvasBoardRef"
              data-testid="workflow-canvas-board"
              class="workflow-board"
              @mousedown="startCanvasPan"
              @wheel.passive.prevent="handleCanvasWheel"
            >
              <div class="workflow-board__chrome">
                <span>平移：拖拽空白区域</span>
                <span>缩放：滚轮</span>
                <span>吸附：{{ GRID_SIZE }} px</span>
              </div>

              <div class="workflow-board__viewport">
                <div class="workflow-board__scene" :style="canvasSceneStyle">
                  <div class="workflow-board__grid" :style="{ width: `${sceneSize.width}px`, height: `${sceneSize.height}px` }"></div>

                  <svg
                    class="workflow-lines"
                    :viewBox="`0 0 ${sceneSize.width} ${sceneSize.height}`"
                    :style="{ width: `${sceneSize.width}px`, height: `${sceneSize.height}px` }"
                    aria-hidden="true"
                  >
                    <defs>
                      <marker
                        id="workflow-arrow"
                        markerWidth="12"
                        markerHeight="12"
                        refX="10"
                        refY="6"
                        orient="auto"
                        markerUnits="strokeWidth"
                      >
                        <path d="M 0 0 L 12 6 L 0 12 z" fill="#2a6ad8" />
                      </marker>
                    </defs>

                    <g v-for="edge in drawableEdges" :key="edge.id">
                      <path
                        class="workflow-edge-hit"
                        :class="{ 'workflow-edge-hit--selected': edge.id === selectedEdgeId }"
                        :d="edge.path"
                        marker-end="url(#workflow-arrow)"
                        @click.stop="selectEdge(edge.id)"
                      />
                    </g>
                  </svg>

                  <div
                    v-for="edge in drawableEdges"
                    :key="`${edge.id}-label`"
                    class="workflow-edge-label"
                    :class="{ 'workflow-edge-label--selected': edge.id === selectedEdgeId }"
                    :style="{ left: `${edge.midX}px`, top: `${edge.midY}px` }"
                    @click.stop="selectEdge(edge.id)"
                  >
                    <strong>{{ edge.label || '未命名连线' }}</strong>
                    <span>{{ edge.condition || '无条件' }}</span>
                  </div>

                  <article
                    v-for="node in editor.nodes"
                    :key="node.id"
                    :data-testid="`workflow-node-${node.id}`"
                    :data-node-id="node.id"
                    :data-node-label="node.label"
                    class="workflow-node"
                    :class="[
                      `workflow-node--${getNodeKind(node)}`,
                      { 'workflow-node--selected': node.id === selectedNodeId, 'workflow-node--connecting': connectState.sourceNodeId === node.id },
                    ]"
                    :style="{ left: `${node.x}px`, top: `${node.y}px` }"
                    @click="selectedNodeId = node.id"
                  >
                    <button
                      class="workflow-node__port workflow-node__port--in"
                      :data-testid="`workflow-node-port-in-${node.id}`"
                      type="button"
                      @click.stop="completeConnection(node.id)"
                    >
                      输入
                    </button>

                    <div class="workflow-node__body" :data-testid="`workflow-node-body-${node.id}`" @mousedown.prevent="startNodeDrag(node, $event)">
                      <div class="workflow-node__meta">
                        <el-tag size="small" effect="plain">{{ getNodeKind(node) }}</el-tag>
                        <el-tag size="small" :type="getNodeStatus(node) === 'blocked' ? 'danger' : getNodeStatus(node) === 'done' ? 'success' : 'info'">
                          {{ getNodeStatus(node) }}
                        </el-tag>
                      </div>
                      <strong>{{ node.label }}</strong>
                      <span>{{ node.agentId ? agentNameMap.get(node.agentId) ?? node.agentId : '未绑定 Agent' }}</span>
                      <p>{{ getNodeStage(node) }}</p>
                    </div>

                    <button
                      class="workflow-node__port workflow-node__port--out"
                      :data-testid="`workflow-node-port-out-${node.id}`"
                      type="button"
                      @click.stop="beginConnection(node.id)"
                    >
                      输出
                    </button>
                  </article>
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <div class="split-grid">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <strong>节点配置</strong>
                <div class="table-actions">
                  <el-button v-if="selectedNode" text @click="duplicateNode(selectedNode)">复制节点</el-button>
                  <el-button v-if="selectedNode" text type="danger" @click="removeNode(selectedNode.id)">删除节点</el-button>
                </div>
              </div>
            </template>

            <div v-if="selectedNode && selectedNodeConfig" class="page-stack">
              <el-form-item label="节点标题" class="form-item-reset">
                <el-input v-model="selectedNode.label" />
              </el-form-item>

              <div class="split-grid">
                <el-form-item label="节点类型" class="form-item-reset">
                  <el-select v-model="selectedNodeConfig.kind">
                    <el-option v-for="template in workflowTemplates" :key="template.kind" :label="template.kind" :value="template.kind" />
                  </el-select>
                </el-form-item>

                <el-form-item label="执行状态" class="form-item-reset">
                  <el-select v-model="selectedNodeConfig.status">
                    <el-option v-for="status in nodeStatusOptions" :key="status" :label="status" :value="status" />
                  </el-select>
                </el-form-item>
              </div>

              <el-form-item label="关联 Agent" class="form-item-reset">
                <el-select v-model="selectedNode.agentId" clearable placeholder="可为空">
                  <el-option v-for="agent in agents" :key="agent.id" :label="agent.name" :value="agent.id" />
                </el-select>
              </el-form-item>

              <el-form-item label="阶段标签" class="form-item-reset">
                <el-input v-model="selectedNodeConfig.stage" placeholder="例如：requirements / review / test" />
              </el-form-item>

              <el-form-item label="节点说明" class="form-item-reset">
                <el-input v-model="selectedNodeConfig.notes" type="textarea" :rows="4" placeholder="记录这个节点的职责、输入或交接条件" />
              </el-form-item>

              <div class="split-grid">
                <el-form-item label="X" class="form-item-reset">
                  <el-input-number v-model="selectedNode.x" :min="0" :step="GRID_SIZE" style="width: 100%" />
                </el-form-item>

                <el-form-item label="Y" class="form-item-reset">
                  <el-input-number v-model="selectedNode.y" :min="0" :step="GRID_SIZE" style="width: 100%" />
                </el-form-item>
              </div>
            </div>

            <el-empty v-else description="请先从左侧模板区新增或选择一个节点" />
          </el-card>

          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <strong>连线配置</strong>
                <div class="table-actions">
                  <el-button v-if="connectState.sourceNodeId" text @click="connectState.sourceNodeId = ''">取消连线</el-button>
                  <el-button v-if="selectedEdge" text type="danger" @click="removeEdge(selectedEdge.id)">删除连线</el-button>
                </div>
              </div>
            </template>

            <div class="page-stack">
              <div v-if="selectedEdge" class="page-stack">
                <div class="split-grid">
                  <el-form-item label="起点" class="form-item-reset">
                    <el-select v-model="selectedEdge.source">
                      <el-option v-for="node in editor.nodes" :key="node.id" :label="node.label" :value="node.id" />
                    </el-select>
                  </el-form-item>

                  <el-form-item label="终点" class="form-item-reset">
                    <el-select v-model="selectedEdge.target">
                      <el-option v-for="node in editor.nodes" :key="node.id" :label="node.label" :value="node.id" />
                    </el-select>
                  </el-form-item>
                </div>

                <el-form-item label="连线标签" class="form-item-reset">
                  <el-input v-model="selectedEdge.label" placeholder="例如：通过 / 驳回 / 回流" />
                </el-form-item>

                <el-form-item label="触发条件" class="form-item-reset">
                  <el-input
                    v-model="selectedEdge.condition"
                    type="textarea"
                    :rows="3"
                    placeholder="例如：评审通过后进入测试；失败则回流实现"
                  />
                </el-form-item>
              </div>

              <el-empty v-else description="先在画布中选择一条连线，或通过节点输出端口创建新连线" />

              <el-table :data="editor.edges" row-key="id" empty-text="暂无连线" @row-click="selectEdge($event.id)">
                <el-table-column label="起点" min-width="130">
                  <template #default="{ row }">
                    {{ editor.nodes.find((node) => node.id === row.source)?.label ?? row.source }}
                  </template>
                </el-table-column>
                <el-table-column label="终点" min-width="130">
                  <template #default="{ row }">
                    {{ editor.nodes.find((node) => node.id === row.target)?.label ?? row.target }}
                  </template>
                </el-table-column>
                <el-table-column prop="label" label="标签" min-width="120" />
                <el-table-column prop="condition" label="条件" min-width="150" show-overflow-tooltip />
              </el-table>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>
