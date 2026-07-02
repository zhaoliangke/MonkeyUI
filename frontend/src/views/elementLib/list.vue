<template>
  <div class="element-list">
    <el-card header="公共元素库">
      <div style="margin-bottom: 10px">
        <el-input v-model="keyword" placeholder="搜索元素" clearable style="width: 200px" @input="loadData" />
      </div>
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="element_name" label="元素名称" />
        <el-table-column prop="page_name" label="所属页面" show-overflow-tooltip />
        <el-table-column prop="element_type" label="类型" width="80" />
        <el-table-column prop="locator_type" label="定位方式" width="80" />
        <el-table-column prop="locator_value" label="定位值" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }"><el-tag :type="row.status === 'valid' ? 'success' : 'danger'">{{ row.status === 'valid' ? '有效' : '失效' }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="handleRepair(row)">AI修复</el-button>
            <el-button size="small" type="info" @click="handleRelated(row)">关联用例</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getElementList, repairElement, getRelatedCases } from '@/api/element'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const keyword = ref('')

async function loadData() {
  loading.value = true
  try { const res = await getElementList({ keyword: keyword.value }); tableData.value = res.data || [] } finally { loading.value = false }
}

async function handleRepair(row) {
  await repairElement({ id: row.id })
  ElMessage.success('修复成功')
  loadData()
}

async function handleRelated(row) {
  try {
    const res = await getRelatedCases({ element_name: row.element_name })
    ElMessage.info(`关联 ${res.data?.count || 0} 个用例`)
  } catch {}
}

onMounted(loadData)
</script>
