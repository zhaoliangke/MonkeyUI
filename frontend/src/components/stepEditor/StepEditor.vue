<template>
  <div class="step-editor">
    <el-button type="primary" size="small" @click="addStep">添加步骤</el-button>
    <el-table :data="modelValue" border stripe style="margin-top: 10px">
      <el-table-column type="index" width="50" />
      <el-table-column label="排序号" width="80">
        <template #default="{ row }">
          <el-input-number v-model="row.sort_num" :min="1" size="small" controls-position="right" />
        </template>
      </el-table-column>
      <el-table-column label="步骤内容">
        <template #default="{ row }">
          <el-input v-model="row.step_content" placeholder="输入自然语言步骤描述" />
        </template>
      </el-table-column>
      <el-table-column label="元素名称" width="140">
        <template #default="{ row }">
          <el-input v-model="row.element_name" placeholder="关联元素" />
        </template>
      </el-table-column>
      <el-table-column label="操作类型" width="120">
        <template #default="{ row }">
          <el-select v-model="row.action_type" placeholder="选择">
            <el-option label="点击" value="click" />
            <el-option label="输入" value="fill" />
            <el-option label="选择" value="select" />
            <el-option label="导航" value="navigate" />
            <el-option label="验证可见" value="assert_visible" />
            <el-option label="验证文本" value="assert_text" />
            <el-option label="等待" value="wait" />
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="参数" width="140">
        <template #default="{ row }">
          <el-input v-model="row.param" placeholder="操作参数" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="80">
        <template #default="{ $index }">
          <el-button type="danger" size="small" @click="removeStep($index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
const props = defineProps({ modelValue: { type: Array, default: () => [] } })
const emit = defineEmits(['update:modelValue'])

function addStep() {
  const steps = [...props.modelValue]
  steps.push({ sort_num: steps.length + 1, step_content: '', element_name: '', action_type: 'click', param: '', assert_text: '', is_valid: true })
  emit('update:modelValue', steps)
}
function removeStep(index) {
  const steps = [...props.modelValue]
  steps.splice(index, 1)
  emit('update:modelValue', steps)
}
</script>
