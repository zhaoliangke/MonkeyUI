<template>
  <div class="system-user">
    <el-card>
      <template #header><div class="card-header"><span>用户管理</span><el-button type="primary" @click="openDialog(null)">新增用户</el-button></div></template>
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }"><el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '启用' : '禁用' }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="date_joined" label="注册时间" width="180" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }"><el-button size="small" @click="openDialog(row)">编辑</el-button></template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="formData.id ? '编辑用户' : '新增用户'" v-model="dialogVisible" width="450px">
      <el-form :model="formData" label-width="80px">
        <el-form-item label="用户名"><el-input v-model="formData.username" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="formData.email" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="formData.password" type="password" show-password /></el-form-item>
        <el-form-item label="激活"><el-switch v-model="formData.is_active" /></el-form-item>
        <el-form-item label="管理员"><el-switch v-model="formData.is_staff" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" @click="handleSave">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUserList, saveUser } from '@/api/system'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const formData = ref({ username: '', email: '', password: '', is_active: true, is_staff: false })

async function loadData() {
  loading.value = true
  try { const res = await getUserList({}); tableData.value = res.data || [] } finally { loading.value = false }
}

function openDialog(row) {
  formData.value = row ? { ...row, password: '' } : { username: '', email: '', password: '', is_active: true, is_staff: false }
  dialogVisible.value = true
}

async function handleSave() {
  await saveUser(formData.value)
  ElMessage.success('保存成功')
  dialogVisible.value = false
  loadData()
}

onMounted(loadData)
</script>

<style scoped>.card-header { display: flex; justify-content: space-between; align-items: center; }</style>
