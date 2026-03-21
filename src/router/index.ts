import { createRouter, createWebHistory } from 'vue-router';

import AppLayout from '@/layouts/AppLayout.vue';

const DashboardPage = () => import('@/pages/DashboardPage.vue');
const SkillsPage = () => import('@/pages/SkillsPage.vue');
const McpsPage = () => import('@/pages/McpsPage.vue');
const AgentsPage = () => import('@/pages/AgentsPage.vue');
const WorkflowsPage = () => import('@/pages/WorkflowsPage.vue');

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'dashboard',
          component: DashboardPage,
          meta: { title: '总览' },
        },
        {
          path: 'skills',
          name: 'skills',
          component: SkillsPage,
          meta: { title: 'Skills' },
        },
        {
          path: 'mcps',
          name: 'mcps',
          component: McpsPage,
          meta: { title: 'MCPs' },
        },
        {
          path: 'agents',
          name: 'agents',
          component: AgentsPage,
          meta: { title: 'Agents' },
        },
        {
          path: 'workflows',
          name: 'workflows',
          component: WorkflowsPage,
          meta: { title: 'Workflows' },
        },
      ],
    },
  ],
});

router.afterEach((to) => {
  document.title = `灵枢台 · ${String(to.meta.title ?? '管理台')}`;
});

export default router;
