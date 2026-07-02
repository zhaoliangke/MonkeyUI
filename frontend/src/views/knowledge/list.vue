<template>
  <div class="knowledge-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>知识库资产</span>
          <div>
            <el-button type="primary" @click="$router.push('/knowledge/edit')">新建资产</el-button>
            <el-button type="success" @click="handleBatch('enable')">批量启用</el-button>
            <el-button type="danger" @click="handleBatch('archive')">批量归档</el-button>
          </div>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input v-model="keyword" placeholder="搜索资产" clearable @input="loadData" />
        </el-col>
      </el-row>
      <el-table :data="tableData" border stripe v-loading="loading" @selection-change="handleSelectionChange" style="margin-top: 10px">
        <el-table-column type="selection" width="45" />
        <el-table-column prop="asset_name" label="资产名称" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="{ draft: 'info', published: 'success', pending_update: 'warning', pending_reflux: 'danger', invalidated: 'info' }[row.status]">
              {{ { draft: '草稿', published: '已发布', pending_update: '待更新', pending_reflux: '待回流', invalidated: '失效' }[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="80" />
        <el-table-column prop="engine_type" label="引擎" width="100" />
        <el-table-column prop="version" label="版本" width="70" />
        <el-table-column prop="update_time" label="更新时间" width="180" />
        <el-table-column label="操作" width="220">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/knowledge/edit/${row.id}`)">编辑</el-button>
            <el-button size="small" type="success" @click="handleExecute(row.id)">执行</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAssetList, batchAssets } from '@/api/knowledge'
import { executeRun } from '@/api/run'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const keyword = ref('')
const selectedIds = ref([])

async function loadData() {
  loading.value = true
  try { const res = await getAssetList({ keyword: keyword.value }); tableData.value = res.data || [] } finally { loading.value = false }
}

function handleSelectionChange(selection) { selectedIds.value = selection.map(s => s.id) }

async function handleBatch(action) {
  if (!selectedIds.value.length) { ElMessage.warning('请选择资产'); return }
  await batchAssets({ ids: selectedIds.value, action })
  ElMessage.success('操作成功')
  loadData()
}

async function handleExecute(assetId) {
  try { await executeRun({ asset_id: assetId }); ElMessage.success('执行任务已提交') } catch {}
}

onMounted(loadData)
</script>

<style scoped>.card-header { display: flex; justify-content: space-between; align-items: center; }</style>
