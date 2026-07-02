<template>
  <div class="reflux-center">
    <div class="page-header">
      <div>
        <h1 class="page-title">Reflux &amp; Self-Healing Center</h1>
        <p class="page-subtitle">Monitor execution results, analyze diffs, and trigger automated self-healing pipelines</p>
      </div>
    </div>

    <div class="stats-row">
      <div v-for="c in cards" :key="c.label" class="stat-card glass" :class="`accent-${c.accent}`">
        <div class="stat-value">{{ c.value }}</div>
        <div class="stat-label">{{ c.label }}</div>
      </div>
    </div>

    <div class="content-grid">
      <div class="card glass">
        <div class="card-header">Recent Refux Records</div>
        <div class="card-body no-pad">
          <table class="tech-table">
            <thead><tr><th>Asset</th><th>Run ID</th><th>Result</th><th>Diff</th><th>Healed</th><th>Time</th></tr></thead>
            <tbody>
              <tr v-for="r in records" :key="r.id" @click="selectedRecord = r" class="clickable-row">
                <td class="mono">{{ r.asset_name }}</td>
                <td class="mono">#{{ r.run_id }}</td>
                <td><span :class="`badge ${r.result === 'pass' ? 'success' : 'danger'}`">{{ r.result }}</span></td>
                <td>{{ r.diff_count > 0 ? r.diff_count + ' diffs' : 'No diff' }}</td>
                <td><span :class="`badge ${r.is_healed ? 'healed' : ''}`">{{ r.is_healed ? 'Healed' : 'Pending' }}</span></td>
                <td>{{ r.created_at }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="selectedRecord" class="card glass" style="grid-column: span 2;">
        <div class="card-header">
          <span>Diff Detail: {{ selectedRecord.asset_name }} #{{ selectedRecord.run_id }}</span>
          <button class="action-btn" @click="handleHeal">&#9670; Heal</button>
        </div>
        <div class="card-body" style="padding: 16px;">
          <VersionCompare :diffText="selectedRecord.diff_text || 'No diff data'" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRefluxList, triggerReflux, getRefluxStats } from '@/api/reflux'
import VersionCompare from '@/components/versionCompare/VersionCompare.vue'
import { ElMessage } from 'element-plus'

const records = ref([])
const selectedRecord = ref(null)
const cards = ref([
  { label: 'Total Runs', value: 0, accent: 'cyan' },
  { label: 'Pass Rate', value: '0%', accent: 'green' },
  { label: 'Diff Events', value: 0, accent: 'blue' },
  { label: 'Healed', value: 0, accent: 'purple' },
])

onMounted(async () => {
  try { const r = await getRefluxList({}); records.value = (r.data || []).slice(0, 20) } catch {}
  try { const r = await getRefluxStats(); const d = r.data || {}; cards.value[0].value = d.total || 0; cards.value[1].value = (d.pass_rate || 0) + '%'; cards.value[2].value = d.diff_events || 0; cards.value[3].value = d.healed || 0 } catch {}
})

async function handleHeal() {
  if (!selectedRecord.value) return
  await triggerReflux({ run_id: selectedRecord.value.run_id })
  ElMessage.success('Self-healing initiated')
}
</script>

<style scoped>
.reflux-center { max-width: 1400px; margin: 0 auto; }
.content-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; margin-top: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.card-body.no-pad { padding: 0; overflow-x: auto; }
.clickable-row { cursor: pointer; }
.clickable-row:hover { background: rgba(0, 230, 180, 0.04); }
</style>
