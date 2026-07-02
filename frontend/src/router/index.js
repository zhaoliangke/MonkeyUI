import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/index.vue') },
  { path: '/project/list', name: 'ProjectList', component: () => import('@/views/project/list.vue') },
  { path: '/project/config/:id', name: 'ProjectConfig', component: () => import('@/views/project/config.vue') },
  { path: '/llm/setting', name: 'LLMSetting', component: () => import('@/views/llm/setting.vue') },
  { path: '/llm/prompt', name: 'LLMPrompt', component: () => import('@/views/llm/prompt.vue') },
  { path: '/llm/test', name: 'LLMTest', component: () => import('@/views/llm/test.vue') },
  { path: '/llm/log', name: 'LLMLog', component: () => import('@/views/llm/log.vue') },
  { path: '/knowledge/list', name: 'KnowledgeList', component: () => import('@/views/knowledge/list.vue') },
  { path: '/knowledge/edit/:id?', name: 'KnowledgeEdit', component: () => import('@/views/knowledge/edit.vue') },
  { path: '/crawler/task-list', name: 'CrawlerTaskList', component: () => import('@/views/crawler/taskList.vue') },
  { path: '/crawler/detail/:id', name: 'CrawlerDetail', component: () => import('@/views/crawler/taskDetail.vue') },
  { path: '/element/list', name: 'ElementList', component: () => import('@/views/elementLib/list.vue') },
  { path: '/env/list', name: 'EnvList', component: () => import('@/views/env/envList.vue') },
  { path: '/run/record', name: 'RunRecord', component: () => import('@/views/autoRun/record.vue') },
  { path: '/run/batch', name: 'BatchTask', component: () => import('@/views/autoRun/batchTask.vue') },
  { path: '/reflux/center', name: 'RefluxCenter', component: () => import('@/views/reflux/center.vue') },
  { path: '/system/user', name: 'SystemUser', component: () => import('@/views/system/user.vue') },
  { path: '/system/role', name: 'SystemRole', component: () => import('@/views/system/role.vue') },
  { path: '/system/setting', name: 'SystemSetting', component: () => import('@/views/system/setting.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
