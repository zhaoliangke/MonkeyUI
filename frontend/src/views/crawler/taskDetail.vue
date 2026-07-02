<template>
  <div class="crawler-detail">
    <el-card :header="'爬取任务详情 #' + taskId">
      <el-descriptions v-if="task" :column="2" border>
        <el-descriptions-item label="任务名称">{{ task.task_name }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="{ pending: 'info', running: 'warning', completed: 'success', failed: 'danger' }[task.status]">{{ task.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="目标URL">{{ task.url }}</el-descriptions-item>
        <el-descriptions-item label="元素数">{{ task.element_count }}</el-descriptions-item>
        <el-descriptions-item label="步骤数">{{ task.step_count }}</el-descriptions-item>
        <el-descriptions-item label="生成资产ID">{{ task.auto_asset_id || '-' }}</el-descriptions-item>
        <el-descriptions-item label="结果信息" :span="2">{{ task.result_msg }}</el-descriptions-item>
      </el-descriptions>
      <div style="margin-top: 20px">
        <el-button v-if="task && task.auto_asset_id" type="primary" @click="$router.push(`/knowledge/edit/${task.auto_asset_id}`)">查看生成资产</el-button>
        <el-button @click="$router.back()">返回</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getCrawlProgress } from '@/api/crawler'

const route = useRoute()
const taskId = route.params.id
const task = ref(null)

onMounted(async () => {
  try { const res = await getCrawlProgress({ id: taskId }); task.value = res.data } catch {}
})
</script>
