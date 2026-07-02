<template>
  <div class="system-setting">
    <el-card header="系统全局配置">
      <el-form :model="configs" label-width="180px">
        <el-form-item label="默认执行引擎">
          <el-select v-model="configs.default_engine"><el-option label="Playwright" value="playwright" /><el-option label="Selenium" value="selenium" /></el-select>
        </el-form-item>
        <el-form-item label="文件存储路径"><el-input v-model="configs.storage_path" /></el-form-item>
        <el-form-item label="执行超时(秒)"><el-input-number v-model="configs.exec_timeout" :min="10" :max="600" /></el-form-item>
        <el-form-item label="失败自动录屏"><el-switch v-model="configs.auto_record" /></el-form-item>
        <el-form-item label="数据脱敏"><el-switch v-model="configs.data_masking" /></el-form-item>
        <el-form-item label="爬取合规校验"><el-switch v-model="configs.crawl_compliance" /></el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave">保存配置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSystemSetting, saveSystemSetting } from '@/api/system'
import { ElMessage } from 'element-plus'

const configs = ref({ default_engine: 'playwright', storage_path: '/static/', exec_timeout: 60, auto_record: true, data_masking: true, crawl_compliance: true })

onMounted(async () => {
  try { const res = await getSystemSetting(); if (res.data) { configs.value = { ...configs.value, ...res.data } } } catch {}
})

async function handleSave() {
  await saveSystemSetting({ configs: configs.value })
  ElMessage.success('配置保存成功')
}
</script>
