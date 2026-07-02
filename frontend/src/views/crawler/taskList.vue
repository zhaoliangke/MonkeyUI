<template>
  <div class="crawler-list">
    <el-card>
      <template #header><div class="card-header"><span>爬取任务</span><el-button type="primary" @click="openDialog">新建爬取任务</el-button></div></template>
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="task_name" label="任务名称" />
        <el-table-column prop="url" label="目标URL" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="{ pending: 'info', running: 'warning', completed: 'success', failed: 'danger', stopped: 'info' }[row.status]">
              {{ { pending: '待执行', running: '采集中', completed: '已完成', failed: '失败', stopped: '已停止' }[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="element_count" label="元素数" width="80" />
        <el-table-column prop="step_count" label="步骤数" width="80" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/crawler/detail/${row.id}`)">详情</el-button>
            <el-button v-if="row.auto_asset_id" size="small" type="success" @click="$router.push(`/knowledge/edit/${row.auto_asset_id}`)">查看资产</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="新建爬取任务" v-model="dialogVisible" width="500px">
      <el-form :model="formData" label-width="100px">
        <el-form-item label="任务名称"><el-input v-model="formData.task_name" /></el-form-item>
        <el-form-item label="目标URL"><el-input v-model="formData.url" /></el-form-item>
        <el-form-item label="环境"><el-select v-model="formData.env_id"><el-option v-for="e in envs" :key="e.id" :label="e.env_name" :value="e.id" /></el-select></el-form-item>
        <el-form-item label="凭据"><el-select v-model="formData.credential_id"><el-option v-for="c in credentials" :key="c.id" :label="c.title" :value="c.id" /></el-select></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" @click="handleStart">启动爬取</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCrawlerTaskList, startCrawl } from '@/api/crawler'
import { getEnvList, getCredentialList } from '@/api/env'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const envs = ref([])
const credentials = ref([])
const formData = ref({ task_name: '', url: '', env_id: null, credential_id: null })

async function loadData() {
  loading.value = true
  try { const res = await getCrawlerTaskList({}); tableData.value = res.data || [] } finally { loading.value = false }
}

async function openDialog() {
  try { const r1 = await getEnvList(); envs.value = r1.data || [] } catch {}
  try { const r2 = await getCredentialList({}); credentials.value = r2.data || [] } catch {}
  dialogVisible.value = true
}

async function handleStart() {
  await startCrawl(formData.value)
  ElMessage.success('爬取任务已启动')
  dialogVisible.value = false
  loadData()
}

onMounted(loadData)
</script>

<style scoped>.card-header { display: flex; justify-content: space-between; align-items: center; }</style>
