<template>
  <div class="project-config">
    <el-card header="项目配置">
      <el-form label-width="120px">
        <el-form-item label="默认LLM模型">
          <el-select v-model="config.default_llm_config_id" placeholder="选择模型">
            <el-option v-for="m in llmModels" :key="m.id" :label="m.model_name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="默认环境">
          <el-select v-model="config.default_env_id" placeholder="选择环境">
            <el-option v-for="e in envs" :key="e.id" :label="e.env_name" :value="e.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="全局超时(秒)">
          <el-input-number v-model="config.global_timeout" :min="10" :max="600" />
        </el-form-item>
        <el-form-item label="全局重试次数">
          <el-input-number v-model="config.global_retry" :min="0" :max="10" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave">保存配置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProjectList, saveProject } from '@/api/project'
import { getEnvList } from '@/api/env'
import { getTemplateList } from '@/api/llm'
import { ElMessage } from 'element-plus'

const route = useRoute()
const config = ref({ global_timeout: 60, global_retry: 0 })
const llmModels = ref([])
const envs = ref([])

onMounted(async () => {
  try {
    const res = await getTemplateList({})
    llmModels.value = res.data || []
  } catch {}
  try {
    const res = await getEnvList()
    envs.value = res.data || []
  } catch {}
})

async function handleSave() {
  config.value.id = route.params.id
  await saveProject(config.value)
  ElMessage.success('配置保存成功')
}
</script>
