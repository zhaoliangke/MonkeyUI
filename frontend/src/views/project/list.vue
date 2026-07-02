<template>
  <div class="project-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>项目管理</span>
          <el-button type="primary" @click="openDialog(null)">新建项目</el-button>
        </div>
      </template>
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="project_name" label="项目名称" />
        <el-table-column prop="project_code" label="项目编码" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">{{ row.status === 1 ? '启用' : '禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180" />
        <el-table-column label="操作" width="300">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" type="success" @click="setDefault(row.id)">设为默认</el-button>
            <el-popconfirm title="确定删除?" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="formData.id ? '编辑项目' : '新建项目'" v-model="dialogVisible" width="500px">
      <el-form :model="formData" label-width="100px">
        <el-form-item label="项目名称">
          <el-input v-model="formData.project_name" />
        </el-form-item>
        <el-form-item label="项目编码">
          <el-input v-model="formData.project_code" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="formData.status" :active-value="1" :inactive-value="0" />
        </el-form-item>
        <el-form-item label="执行超时(秒)">
          <el-input-number v-model="formData.global_timeout" :min="10" :max="600" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProjectList, saveProject, setDefaultProject, deleteProject } from '@/api/project'
import { useProjectStore } from '@/store/project'
import { ElMessage } from 'element-plus'

const store = useProjectStore()
const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const formData = ref({ project_name: '', project_code: '', description: '', status: 1, global_timeout: 60 })

async function loadData() {
  loading.value = true
  try {
    const res = await getProjectList({})
    tableData.value = res.data || []
  } finally { loading.value = false }
}

function openDialog(row) {
  formData.value = row ? { ...row } : { project_name: '', project_code: '', description: '', status: 1, global_timeout: 60 }
  dialogVisible.value = true
}

async function handleSave() {
  await saveProject(formData.value)
  ElMessage.success('保存成功')
  dialogVisible.value = false
  loadData()
}

async function setDefault(id) {
  await setDefaultProject(id)
  store.setProject(id, tableData.value.find(p => p.id === id)?.project_name || '')
  ElMessage.success('已设为默认项目')
  loadData()
}

async function handleDelete(id) {
  await deleteProject(id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
