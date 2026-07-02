<template>
  <div class="batch-task">
    <el-card header="批量回归任务">
      <div style="margin-bottom: 10px">
        <el-input v-model="keyword" placeholder="搜索资产" clearable style="width: 300px" />
        <el-button type="primary" @click="loadAssets" style="margin-left: 10px">搜索</el-button>
      </div>
      <el-table :data="assets" border stripe v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="45" />
        <el-table-column prop="asset_name" label="资产名称" />
        <el-table-column prop="status" label="状态" width="100" />
        <el-table-column prop="priority" label="优先级" width="80" />
      </el-table>
      <div style="margin-top: 15px">
        <el-button type="primary" @click="handleBatchExecute" :disabled="!selectedIds.length">批量执行 ({{ selectedIds.length }})</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { getAssetList } from '@/api/knowledge'
import { executeBatch } from '@/api/run'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const keyword = ref('')
const assets = ref([])
const selectedIds = ref([])

async function loadAssets() {
  loading.value = true
  try { const res = await getAssetList({ keyword: keyword.value }); assets.value = res.data || [] } finally { loading.value = false }
}

function handleSelectionChange(val) { selectedIds.value = val.map(v => v.id) }

async function handleBatchExecute() {
  await executeBatch({ asset_ids: selectedIds.value })
  ElMessage.success('批量执行任务已提交')
}
</script>
