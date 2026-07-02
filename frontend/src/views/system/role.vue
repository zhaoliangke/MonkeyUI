<template>
  <div class="system-role">
    <el-card>
      <template #header><div class="card-header"><span>角色管理</span><el-button type="primary" @click="openDialog(null)">新增角色</el-button></div></template>
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="角色名称" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }"><el-button size="small" @click="openDialog(row)">编辑</el-button></template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="formData.id ? '编辑角色' : '新增角色'" v-model="dialogVisible" width="400px">
      <el-form :model="formData" label-width="80px">
        <el-form-item label="角色名称"><el-input v-model="formData.name" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" @click="handleSave">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRoleList, saveRole } from '@/api/system'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const formData = ref({ name: '' })

async function loadData() {
  loading.value = true
  try { const res = await getRoleList(); tableData.value = res.data || [] } finally { loading.value = false }
}

function openDialog(row) { formData.value = row ? { ...row } : { name: '' }; dialogVisible.value = true }

async function handleSave() { await saveRole(formData.value); ElMessage.success('保存成功'); dialogVisible.value = false; loadData() }

onMounted(loadData)
</script>

<style scoped>.card-header { display: flex; justify-content: space-between; align-items: center; }</style>
