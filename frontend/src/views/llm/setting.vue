<template>
  <div class="llm-setting">
    <el-card>
      <template #header><div class="card-header"><span>LLM模型配置</span><el-button type="primary" @click="openDialog(null)">新增配置</el-button></div></template>
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="model_name" label="模型名称" />
        <el-table-column prop="model_type" label="模型类型" width="100">
          <template #default="{ row }"><el-tag>{{ row.model_type === 'public' ? '公有云' : '私有化' }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="api_base" label="API地址" />
        <el-table-column prop="is_enable" label="状态" width="80">
          <template #default="{ row }"><el-tag :type="row.is_enable ? 'success' : 'info'">{{ row.is_enable ? '启用' : '禁用' }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" type="success" @click="handleTest(row)">连通测试</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="formData.id ? '编辑配置' : '新增配置'" v-model="dialogVisible" width="600px">
      <el-form :model="formData" label-width="120px">
        <el-form-item label="模型类型"><el-select v-model="formData.model_type"><el-option label="公有云" value="public" /><el-option label="私有化本地" value="private" /></el-select></el-form-item>
        <el-form-item label="模型名称"><el-input v-model="formData.model_name" /></el-form-item>
        <el-form-item label="API地址"><el-input v-model="formData.api_base" /></el-form-item>
        <el-form-item label="API密钥"><el-input v-model="formData.api_key" type="password" show-password /></el-form-item>
        <el-form-item label="超时(秒)"><el-input-number v-model="formData.timeout" :min="10" :max="300" /></el-form-item>
        <el-form-item label="温度"><el-slider v-model="formData.temperature" :min="0" :max="1" :step="0.1" show-input /></el-form-item>
        <el-form-item label="最大Token"><el-input-number v-model="formData.max_tokens" :min="100" :max="32768" /></el-form-item>
        <el-form-item label="启用"><el-switch v-model="formData.is_enable" /></el-form-item>
        <el-form-item label="设为默认"><el-switch v-model="formData.is_default" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" @click="handleSave">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTemplateList, saveLLMConfig, testLLMConfig } from '@/api/llm'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const formData = ref({ model_type: 'public', model_name: '', api_base: '', api_key: '', timeout: 60, temperature: 0.7, max_tokens: 4096, is_enable: true, is_default: false })

async function loadData() {
  loading.value = true
  try {
    const res = await getTemplateList({ template_type: '' })
    tableData.value = res.data || []
  } finally { loading.value = false }
}

function openDialog(row) {
  formData.value = row ? { ...row } : { model_type: 'public', model_name: '', api_base: '', api_key: '', timeout: 60, temperature: 0.7, max_tokens: 4096, is_enable: true, is_default: false }
  dialogVisible.value = true
}

async function handleSave() {
  await saveLLMConfig(formData.value)
  ElMessage.success('保存成功')
  dialogVisible.value = false
  loadData()
}

async function handleTest(row) {
  try {
    const res = await testLLMConfig({ id: row.id })
    ElMessage.success(res.data?.message || '连通性正常')
  } catch { ElMessage.error('连通测试失败') }
}

onMounted(loadData)
</script>

<style scoped>.card-header { display: flex; justify-content: space-between; align-items: center; }</style>
