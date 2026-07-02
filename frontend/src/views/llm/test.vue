<template>
  <div class="llm-test">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card header="输入区域">
          <el-form label-width="100px">
            <el-form-item label="模板类型"><el-select v-model="templateType"><el-option label="自然语言转脚本" value="script_gen" /><el-option label="步骤纠错" value="step_correct" /><el-option label="元素修复" value="element_fix" /><el-option label="断言生成" value="assert_gen" /></el-select></el-form-item>
            <el-form-item label="自然语言步骤"><el-input v-model="stepsText" type="textarea" :rows="6" placeholder="输入自然语言测试步骤，每行一个步骤" /></el-form-item>
            <el-form-item label="元素信息"><el-input v-model="elementsText" type="textarea" :rows="4" placeholder="输入元素信息(选填)" /></el-form-item>
            <el-form-item><el-button type="primary" @click="handleGenerate" :loading="generating">生成脚本</el-button></el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="生成结果">
          <div v-if="result.script_content">
            <el-tag type="success" style="margin-bottom: 10px">生成耗时: {{ result.cost_time?.toFixed(2) }}s</el-tag>
            <pre class="script-preview"><code>{{ result.script_content }}</code></pre>
          </div>
          <el-empty v-else description="点击生成按钮查看AI生成的脚本" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { generateScript } from '@/api/llm'
import { ElMessage } from 'element-plus'

const templateType = ref('script_gen')
const stepsText = ref('')
const elementsText = ref('')
const generating = ref(false)
const result = ref({})

async function handleGenerate() {
  if (!stepsText.value) { ElMessage.warning('请输入自然语言步骤'); return }
  generating.value = true
  try {
    const res = await generateScript({ steps_text: stepsText.value, elements_text: elementsText.value, template_type: templateType.value })
    result.value = res.data || {}
    ElMessage.success('脚本生成成功')
  } finally { generating.value = false }
}
</script>

<style scoped>.script-preview { background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 4px; overflow-x: auto; font-size: 13px; line-height: 1.6; max-height: 500px; overflow-y: auto; }</style>
