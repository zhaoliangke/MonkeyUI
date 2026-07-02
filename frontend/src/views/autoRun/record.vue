<template>
  <div class="run-record">
    <el-card header="执行记录">
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="asset_id" label="资产ID" width="80" />
        <el-table-column prop="run_type" label="执行类型" width="100">
          <template #default="{ row }"><el-tag>{{ { single: '单条', batch: '批量', schedule: '定时', cicd: 'CI/CD' }[row.run_type] }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="result" label="结果" width="80">
          <template #default="{ row }"><el-tag :type="{ pass: 'success', fail: 'danger', running: 'warning', blocked: 'info' }[row.result]">{{ { pass: '通过', fail: '失败', running: '运行中', blocked: '阻塞' }[row.result] }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="cost_time" label="耗时(秒)" width="90" />
        <el-table-column prop="fail_reason" label="失败原因" show-overflow-tooltip />
        <el-table-column prop="run_time" label="执行时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRecordList } from '@/api/run'

const loading = ref(false)
const tableData = ref([])

onMounted(async () => {
  loading.value = true
  try { const res = await getRecordList({}); tableData.value = res.data || [] } finally { loading.value = false }
})
</script>
