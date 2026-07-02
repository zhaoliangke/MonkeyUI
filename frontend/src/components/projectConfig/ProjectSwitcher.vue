<template>
  <el-select
    v-model="currentId"
    placeholder="Select Project"
    size="small"
    popper-class="project-select-popper"
    style="width: 220px"
    @change="handleSwitch"
    filterable
  >
    <template #prefix>
      <span style="color: var(--accent-primary); margin-right: 4px; font-size: 12px;">&#9670;</span>
    </template>
    <el-option v-for="p in projects" :key="p.id" :label="p.project_name" :value="p.id">
      <span style="float: left">{{ p.project_name }}</span>
      <span style="float: right; color: var(--text-muted); font-size: 11px; font-family: var(--font-mono)">{{ p.project_code }}</span>
    </el-option>
  </el-select>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProjectList } from '@/api/project'
import { useProjectStore } from '@/store/project'

const store = useProjectStore()
const projects = ref([])
const currentId = ref(store.currentProjectId || '')

async function loadProjects() {
  try { const res = await getProjectList({}); projects.value = res.data || [] } catch {}
}

function handleSwitch(val) {
  const project = projects.value.find(p => p.id === val)
  store.setProject(val, project ? project.project_name : '')
}

onMounted(loadProjects)
</script>
