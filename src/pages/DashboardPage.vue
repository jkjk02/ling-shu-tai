<script setup lang="ts">
import { onMounted, ref } from 'vue';

import { dashboardApi } from '@/api/resources';
import { getErrorMessage } from '@/api/http';
import AppSectionHeader from '@/components/AppSectionHeader.vue';
import StatusPill from '@/components/StatusPill.vue';
import { mockDashboard } from '@/data/mock';
import type { DashboardResponse } from '@/types/resources';

const shortcuts = [
  { title: 'Skills', route: '/skills', desc: '查看工具技能、触发命令与脚本资产。' },
  { title: 'MCPs', route: '/mcps', desc: '管理模型配置、温度与额外参数。' },
  { title: 'Agents', route: '/agents', desc: '配置角色 Prompt 与技能授权。' },
  { title: 'Workflows', route: '/workflows', desc: '编排节点、连线与流程模板。' },
];

const dashboard = ref<DashboardResponse>(mockDashboard);
const loading = ref(false);
const warningMessage = ref('');

async function loadDashboard() {
  loading.value = true;
  warningMessage.value = '';

  try {
    dashboard.value = await dashboardApi.getOverview();
  } catch (error) {
    dashboard.value = mockDashboard;
    warningMessage.value = getErrorMessage(error, '总览接口暂不可用，当前显示本地示例数据。');
  } finally {
    loading.value = false;
  }
}

onMounted(loadDashboard);
</script>

<template>
  <div class="page-stack">
    <AppSectionHeader title="平台总览" description="集中查看三类 CLI 工具资源发现状态与协作资产规模。" />

    <el-alert v-if="warningMessage" :title="warningMessage" type="warning" show-icon :closable="false" />

    <section class="metric-grid">
      <article v-for="summary in dashboard.summaries" :key="summary.cliTool" v-loading="loading" class="metric-card">
        <div class="metric-card__head">
          <h4>{{ summary.cliTool }}</h4>
          <StatusPill :status="summary.status" />
        </div>
        <div class="metric-list">
          <div>
            <span>Skills</span>
            <strong>{{ summary.skillCount }}</strong>
          </div>
          <div>
            <span>MCPs</span>
            <strong>{{ summary.mcpCount }}</strong>
          </div>
          <div>
            <span>最近扫描</span>
            <strong>{{ summary.lastScanAt }}</strong>
          </div>
        </div>
      </article>
    </section>

    <section class="overview-grid">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span>资源规模</span>
          </div>
        </template>
        <div class="summary-stats">
          <div>
            <span>Agents</span>
            <strong>{{ dashboard.agentCount }}</strong>
          </div>
          <div>
            <span>Workflows</span>
            <strong>{{ dashboard.workflowCount }}</strong>
          </div>
          <div>
            <span>最后更新</span>
            <strong>{{ dashboard.lastUpdatedAt }}</strong>
          </div>
        </div>
      </el-card>

      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span>快速入口</span>
          </div>
        </template>
        <div class="shortcut-grid">
          <router-link v-for="shortcut in shortcuts" :key="shortcut.title" :to="shortcut.route" class="shortcut-card">
            <strong>{{ shortcut.title }}</strong>
            <p>{{ shortcut.desc }}</p>
          </router-link>
        </div>
      </el-card>
    </section>
  </div>
</template>
