<template>
  <div class="dashboard">
    <!-- Welcome Header -->
    <div class="dashboard-header">
      <div>
        <h1 class="page-title">Dashboard</h1>
        <p class="page-subtitle">{{ store.currentProjectName || 'No project selected' }} &mdash; Real-time system overview</p>
      </div>
      <div class="header-actions">
        <button class="action-btn primary" @click="$router.push('/knowledge/edit')">
          <span class="btn-icon">+</span> New Asset
        </button>
        <button class="action-btn" @click="$router.push('/crawler/task-list')">
          <span class="btn-icon">&#8981;</span> Start Crawl
        </button>
      </div>
    </div>

    <!-- Stat Cards Row -->
    <div class="stat-grid">
      <div class="stat-card" v-for="s in stats" :key="s.label" :class="s.accent">
        <div class="stat-icon" v-html="s.icon"></div>
        <div class="stat-info">
          <div class="stat-value">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
        <div class="stat-trend" v-if="s.trend">
          <span :class="s.trendDir">{{ s.trend }}</span>
        </div>
      </div>
    </div>

    <!-- Two Column Layout -->
    <div class="dashboard-grid">
      <!-- Quick Actions -->
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">Quick Actions</span>
        </div>
        <div class="panel-body">
          <div class="quick-actions">
            <button class="quick-btn" v-for="qa in quickActions" :key="qa.label" @click="$router.push(qa.path)">
              <span class="quick-icon" v-html="qa.icon"></span>
              <span class="quick-label">{{ qa.label }}</span>
              <span class="quick-desc">{{ qa.desc }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Project Info / Recent Activity -->
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">System Status</span>
        </div>
        <div class="panel-body">
          <div class="status-list">
            <div class="status-row">
              <span class="status-label">Backend Server</span>
              <span class="status-value ok">Operational</span>
            </div>
            <div class="status-row">
              <span class="status-label">LLM Engine</span>
              <span class="status-value" :class="llmStatus.class">{{ llmStatus.text }}</span>
            </div>
            <div class="status-row">
              <span class="status-label">Playwright</span>
              <span class="status-value ok">Ready</span>
            </div>
            <div class="status-row">
              <span class="status-label">Database</span>
              <span class="status-value ok">Connected</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useProjectStore } from '@/store/project'
import { getDashboardStats } from '@/api/knowledge'

const store = useProjectStore()

const llmStatus = ref({ class: 'warn', text: 'Pending Config' })

const stats = ref([
  { label: 'Total Assets', value: 0, icon: '&#9000;', accent: 'cyan', trend: '', trendDir: '' },
  { label: 'Active Assets', value: 0, icon: '&#10003;', accent: 'green', trend: '', trendDir: '' },
  { label: 'Crawl Success', value: '0%', icon: '&#8981;', accent: 'blue', trend: '', trendDir: '' },
  { label: 'Execution Pass', value: '0%', icon: '&#9655;', accent: 'purple', trend: '', trendDir: '' },
])

const quickActions = [
  { label: 'New Asset', desc: 'Create test case manually', icon: '+', path: '/knowledge/edit' },
  { label: 'Start Crawl', desc: 'Auto-crawl page elements', icon: '&#8981;', path: '/crawler/task-list' },
  { label: 'Batch Execute', desc: 'Run regression tests', icon: '&#9655;', path: '/run/batch' },
  { label: 'LLM Playground', desc: 'Test AI script generation', icon: '&#9670;', path: '/llm/test' },
]

onMounted(async () => {
  try {
    const res = await getDashboardStats()
    const d = res.data || {}
    stats.value[0].value = d.assets_total || 0
    stats.value[1].value = d.assets_published || 0
    stats.value[2].value = (d.crawl_success_rate || 0) + '%'
    stats.value[3].value = (d.execution_pass_rate || 0) + '%'
  } catch {}
})
</script>

<style scoped>
.dashboard { max-width: 1200px; margin: 0 auto; }
.dashboard-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 28px; }
.page-title { font-size: 26px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.5px; }
.page-subtitle { font-size: 13px; color: var(--text-muted); margin-top: 4px; }
.header-actions { display: flex; gap: 10px; }
.action-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 9px 18px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-card);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 13px; font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-family: var(--font-sans);
}
.action-btn:hover { border-color: var(--border-active); color: var(--text-primary); background: rgba(0, 230, 180, 0.06); }
.action-btn.primary { background: rgba(0, 230, 180, 0.12); border-color: rgba(0, 230, 180, 0.3); color: var(--accent-primary); }
.action-btn.primary:hover { background: rgba(0, 230, 180, 0.18); box-shadow: 0 0 16px var(--accent-glow); }
.btn-icon { font-size: 14px; }

/* Stat Cards */
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-card);
  transition: all var(--transition-smooth);
}
.stat-card:hover { border-color: var(--border-active); transform: translateY(-1px); }
.stat-card::before {
  content: ''; position: absolute; top: -20px; right: -20px;
  width: 80px; height: 80px; border-radius: 50%;
  opacity: 0.08; filter: blur(20px);
}
.stat-card.cyan::before  { background: var(--accent-primary); }
.stat-card.green::before { background: var(--status-success); }
.stat-card.blue::before  { background: var(--accent-blue); }
.stat-card.purple::before { background: var(--accent-purple); }
.stat-icon { font-size: 28px; opacity: 0.5; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; background: var(--bg-input); border-radius: var(--radius-md); }
.stat-info { flex: 1; }
.stat-value { font-size: 28px; font-weight: 700; color: var(--text-primary); font-family: var(--font-mono); letter-spacing: -0.5px; }
.stat-label { font-size: 12px; color: var(--text-muted); margin-top: 2px; text-transform: uppercase; letter-spacing: 0.5px; }
.stat-trend { font-size: 11px; font-weight: 600; }
.stat-trend .up { color: var(--status-success); }
.stat-trend .down { color: var(--status-danger); }

/* Dashboard Grid */
.dashboard-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

/* Panels */
.panel {
  background: var(--bg-card);
  border: 1px solid var(--border-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}
.panel-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-subtle);
  display: flex; justify-content: space-between; align-items: center;
}
.panel-title { font-weight: 600; color: var(--text-primary); font-size: 14px; letter-spacing: 0.3px; }
.panel-body { padding: 20px; }

/* Quick Actions */
.quick-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.quick-btn {
  display: flex; flex-direction: column; gap: 4px;
  padding: 16px;
  background: var(--bg-input);
  border: 1px solid var(--border-card);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
  font-family: var(--font-sans);
}
.quick-btn:hover { border-color: var(--border-active); background: rgba(0, 230, 180, 0.06); color: var(--text-primary); }
.quick-icon { font-size: 18px; color: var(--accent-primary); }
.quick-label { font-size: 14px; font-weight: 600; color: var(--text-primary); }
.quick-desc { font-size: 12px; color: var(--text-muted); }

/* Status List */
.status-list { display: flex; flex-direction: column; gap: 12px; }
.status-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid var(--border-subtle); }
.status-row:last-child { border-bottom: none; }
.status-label { font-size: 13px; color: var(--text-secondary); font-weight: 500; }
.status-value { font-size: 12px; font-weight: 600; font-family: var(--font-mono); }
.status-value.ok { color: var(--status-success); }
.status-value.warn { color: var(--status-warning); }
.status-value.err { color: var(--status-danger); }

@media (max-width: 900px) {
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
  .dashboard-grid { grid-template-columns: 1fr; }
}
</style>
