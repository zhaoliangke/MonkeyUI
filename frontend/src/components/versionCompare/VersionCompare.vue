<template>
  <div class="version-compare">
    <div v-if="!hasDiff" class="no-diff">
      <span class="no-diff-icon">&#10003;</span>
      <p>No differences found between versions</p>
    </div>
    <div v-else class="diff-container">
      <div class="diff-header">
        <span class="diff-stat">+{{ addedLines }}</span>
        <span class="diff-stat removed">-{{ removedLines }}</span>
      </div>
      <div class="diff-content">
        <div
          v-for="(line, i) in diffLines"
          :key="i"
          class="diff-line"
          :class="{
            'diff-added': line.startsWith('+'),
            'diff-removed': line.startsWith('-'),
            'diff-header-line': line.startsWith('@@'),
          }"
        >{{ line }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  diffText: { type: String, default: '' },
})

const diffLines = computed(() => {
  if (!props.diffText) return []
  return props.diffText.split('\n')
})

const hasDiff = computed(() => diffLines.value.length > 0)

const addedLines = computed(() => diffLines.value.filter(l => l.startsWith('+') && !l.startsWith('+++')).length)
const removedLines = computed(() => diffLines.value.filter(l => l.startsWith('-') && !l.startsWith('---')).length)
</script>

<style scoped>
.version-compare { font-family: var(--font-mono); font-size: 12px; }
.no-diff {
  text-align: center;
  padding: 40px;
  color: var(--text-muted);
}
.no-diff-icon { font-size: 32px; color: var(--status-success); display: block; margin-bottom: 8px; }
.diff-header { display: flex; gap: 16px; padding: 8px 12px; background: rgba(10, 14, 23, 0.5); border-radius: var(--radius-sm); margin-bottom: 8px; }
.diff-stat { color: var(--status-success); font-weight: 700; }
.diff-stat.removed { color: var(--status-danger); }
.diff-content { background: rgba(10, 14, 23, 0.6); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); overflow: hidden; max-height: 500px; overflow-y: auto; }
.diff-line { padding: 2px 12px; line-height: 1.6; white-space: pre-wrap; word-break: break-all; }
.diff-added { background: rgba(0, 230, 180, 0.06); color: var(--status-success); }
.diff-removed { background: rgba(255, 92, 114, 0.06); color: var(--status-danger); }
.diff-header-line { background: rgba(77, 148, 255, 0.08); color: var(--accent-blue); font-weight: 600; }
</style>
