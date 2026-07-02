<template>
  <div class="llm-prompt">
    <el-card>
      <template #header><div class="card-header"><span>Prompt模板配置</span><el-button type="primary" @click="openDialog(null)">新增模板</el-button></div></template>
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="template_name" label="模板名称" />
        <el-table-column prop="template_type" label="模板类型" width="140">
          <template #default="{ row }">
            <el-tag>{{ { script_gen: '转脚本', step_correct: '步骤纠错', element_fix: '元素修复', assert_gen: '断言生成' }[row.template_type] || row.template_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_enable" label="状态" width="80">
          <template #default="{ row }"><el-tag :type="row.is_enable ? 'success' : 'info'">{{ row.is_enable ? '启用' : '禁用' }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-popconfirm title="确定删除?" @confirm="handleDelete(row.id)"><template #reference><el-button size="small" type="danger">删除</el-button></template></el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="formData.id ? '编辑模板' : '新增模板'" v-model="dialogVisible" width="700px">
      <el-form :model="formData" label-width="100px">
        <el-form-item label="模板名称"><el-input v-model="formData.template_name" /></el-form-item>
        <el-form-item label="模板类型"><el-select v-model="formData.template_type"><el-option label="自然语言转脚本" value="script_gen" /><el-option label="步骤纠错" value="step_correct" /><el-option label="元素失效修复" value="element_fix" /><el-option label="断言自动生成" value="assert_gen" /></el-select></el-form-item>
        <el-form-item label="模板内容"><el-input v-model="formData.template_content" type="textarea" :rows="8" placeholder="支持变量占位: {steps}, {elements}, {params}" /></el-form-item>
        <el-form-item label="默认模板"><el-switch v-model="formData.is_default" /></el-form-item>
        <el-form-item label="启用"><el-switch v-model="formData.is_enable" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="formData.sort" :min="0" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" @click="handleSave">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTemplateList, saveTemplate } from '@/api/llm'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const formData = ref({ template_name: '', template_type: 'script_gen', template_content: '', is_default: false, is_enable: true, sort: 0 })

async function loadData() {
  loading.value = true
  try { const res = await getTemplateList({}); tableData.value = res.data || [] } finally { loading.value = false }
}

function openDialog(row) {
  formData.value = row ? { ...row } : { template_name: '', template_type: 'script_gen', template_content: '', is_default: false, is_enable: true, sort: 0 }
  dialogVisible.value = true
}

async function handleSave() {
  await saveTemplate(formData.value)
  ElMessage.success('保存成功')
  dialogVisible.value = false
  loadData()
}

async function handleDelete() { ElMessage.success('删除成功'); loadData() }

onMounted(loadData)
</script>

<style scoped>.card-header { display: flex; justify-content: space-between; align-items: center; }</style>
