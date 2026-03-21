<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { Connection, Cpu, DataAnalysis, Document, Histogram } from '@element-plus/icons-vue';

const route = useRoute();

const navItems = [
  { label: '总览', path: '/', icon: Histogram, description: '扫描状态与资源汇总', testId: 'nav-dashboard' },
  { label: 'Skills', path: '/skills', icon: Document, description: '技能定义与脚本维护', testId: 'nav-skills' },
  { label: 'MCPs', path: '/mcps', icon: Cpu, description: '模型与推理参数配置', testId: 'nav-mcps' },
  { label: 'Agents', path: '/agents', icon: DataAnalysis, description: '角色、Prompt 与技能分配', testId: 'nav-agents' },
  { label: 'Workflows', path: '/workflows', icon: Connection, description: '多 Agent 画布编排', testId: 'nav-workflows' },
];

const pageTitle = computed(() => String(route.meta.title ?? '灵枢台'));
</script>

<template>
  <div class="app-shell">
    <aside class="app-sidebar">
      <div class="brand-block">
        <p class="brand-eyebrow">Ling Shu Tai</p>
        <h1>灵枢台</h1>
        <p>CLI 资源与多智能体编排管理台</p>
      </div>

      <el-menu :default-active="route.path" class="side-menu" router>
        <el-menu-item
          v-for="item in navItems"
          :key="item.path"
          :index="item.path"
          :route="item.path"
          :data-testid="item.testId"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </el-menu-item>
      </el-menu>

      <div class="side-panel">
        <span class="panel-label">当前阶段</span>
        <strong>实现中</strong>
        <p>前端骨架已接入页面框架，等待后端 API 联调。</p>
      </div>
    </aside>

    <main class="app-main">
      <header class="topbar">
        <div>
          <p class="topbar-caption">平台工作台</p>
          <h2>{{ pageTitle }}</h2>
        </div>
        <div class="topbar-status">
          <span>环境：本地开发</span>
          <el-tag type="success" effect="dark">REST API</el-tag>
        </div>
      </header>

      <section class="page-body">
        <router-view />
      </section>
    </main>
  </div>
</template>
