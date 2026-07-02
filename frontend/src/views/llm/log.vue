<template>
  <div class="llm-log">
    <el-card header="AI调用日志">
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="template_type" label="模板类型" width="120" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }"><el-tag :type="row.status === 'success' ? 'success' : 'danger'">{{ row.status }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="cost_time" label="耗时(秒)" width="100" />
        <el-table-column prop="input_content" label="入参" show-overflow-tooltip />
        <el-table-column prop="error_msg" label="错误信息" show-overflow-tooltip />
        <el-table-column prop="create_time" label="时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getLLMLogList } from '@/api/llm'

const loading = ref(false)
const tableData = ref([])

onMounted(async () => {
  loading.value = true
  try { const res = await getLLMLogList({}); tableData.value = res.data || [] } finally { loading.value = false }
})
</script>
