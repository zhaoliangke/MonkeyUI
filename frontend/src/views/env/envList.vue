<template>
  <div class="env-list">
    <el-card header="环境管理">
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="env_name" label="环境名称" />
        <el-table-column prop="env_type" label="类型">
          <template #default="{ row }"><el-tag>{{ { test: '测试', staging: '预发', production: '生产' }[row.env_type] }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="base_url" label="基础URL" show-overflow-tooltip />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="openEnvDialog(row)">编辑</el-button>
            <el-button size="small" type="info" @click="openCredDialog(row)">管理凭据</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="编辑环境" v-model="dialogVisible" width="500px">
      <el-form :model="envForm" label-width="100px">
        <el-form-item label="环境名称"><el-input v-model="envForm.env_name" /></el-form-item>
        <el-form-item label="环境类型"><el-select v-model="envForm.env_type"><el-option label="测试" value="test" /><el-option label="预发" value="staging" /><el-option label="生产" value="production" /></el-select></el-form-item>
        <el-form-item label="基础URL"><el-input v-model="envForm.base_url" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" @click="handleEnvSave">保存</el-button></template>
    </el-dialog>

    <el-dialog title="管理凭据" v-model="credDialogVisible" width="600px">
      <el-table :data="credData" border stripe>
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="account" label="账号" />
        <el-table-column prop="is_enable" label="状态"><template #default="{ row }"><el-tag :type="row.is_enable ? 'success' : 'info'">{{ row.is_enable ? '启用' : '禁用' }}</el-tag></template></el-table-column>
      </el-table>
      <template #footer><el-button @click="credDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getEnvList, saveEnv, getCredentialList } from '@/api/env'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const credDialogVisible = ref(false)
const credData = ref([])
const envForm = ref({ env_name: '', env_type: 'test', base_url: '' })

async function loadData() {
  loading.value = true
  try { const res = await getEnvList(); tableData.value = res.data || [] } finally { loading.value = false }
}

function openEnvDialog(row) { envForm.value = row ? { ...row } : { env_name: '', env_type: 'test', base_url: '' }; dialogVisible.value = true }

async function handleEnvSave() { await saveEnv(envForm.value); ElMessage.success('保存成功'); dialogVisible.value = false; loadData() }

async function openCredDialog(row) {
  try { const res = await getCredentialList({ env_id: row.id }); credData.value = res.data || [] } catch {}
  credDialogVisible.value = true
}

onMounted(loadData)
</script>
