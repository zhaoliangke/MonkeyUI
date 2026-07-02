<template>
  <div class="knowledge-edit">
    <div class="edit-header">
      <div>
        <h1 class="page-title">{{ isNew ? 'New Asset' : 'Edit Asset' }}</h1>
        <p class="page-subtitle">Configure test case with natural language steps and AI-powered automation</p>
      </div>
      <div class="header-actions">
        <button class="action-btn secondary" @click="$router.back()">Cancel</button>
        <button class="action-btn primary" @click="handleSave">
          <span>&#10003;</span> Save Asset
        </button>
      </div>
    </div>

    <div class="edit-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        <span class="tab-number">{{ tab.num }}</span>
        <span>{{ tab.label }}</span>
      </button>
    </div>

    <div class="tab-content">
      <!-- 1. Crawl Configuration -->
      <div v-show="activeTab === 'crawl'" class="panel">
        <div class="panel-header">Crawl Configuration</div>
        <div class="panel-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Target URL</label>
              <input class="tech-input" v-model="formData.crawler_url" placeholder="https://example.com" />
            </div>
            <div class="form-group">
              <label>Environment Type</label>
              <select class="tech-input" v-model="formData.env_type">
                <option value="">Select</option>
                <option value="test">Test</option>
                <option value="staging">Staging</option>
              </select>
            </div>
            <div class="form-group full-width">
              <label>Crawl Rules (CSS Selectors)</label>
              <textarea class="tech-input" v-model="formData.crawler_rule" placeholder=".main-content, #app-root" rows="3"></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Basic Info -->
      <div v-show="activeTab === 'basic'" class="panel">
        <div class="panel-header">Basic Information</div>
        <div class="panel-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Asset Name</label>
              <input class="tech-input" v-model="formData.asset_name" placeholder="e.g. Login Flow Test" />
            </div>
            <div class="form-group">
              <label>Priority</label>
              <select class="tech-input" v-model="formData.priority">
                <option value="P0">P0 - Critical</option>
                <option value="P1">P1 - High</option>
                <option value="P2">P2 - Medium</option>
                <option value="P3">P3 - Low</option>
              </select>
            </div>
            <div class="form-group">
              <label>Execution Engine</label>
              <select class="tech-input" v-model="formData.engine_type">
                <option value="playwright">Playwright</option>
                <option value="selenium">Selenium</option>
                <option value="appium">Appium</option>
              </select>
            </div>
            <div class="form-group">
              <label>Status</label>
              <select class="tech-input" v-model="formData.status">
                <option value="draft">Draft</option>
                <option value="published">Published</option>
              </select>
            </div>
            <div class="form-group full-width">
              <label>Pre-condition</label>
              <textarea class="tech-input" v-model="formData.pre_condition" rows="2" placeholder="e.g. User is on login page"></textarea>
            </div>
            <div class="form-group full-width">
              <label>Post-condition</label>
              <textarea class="tech-input" v-model="formData.post_condition" rows="2" placeholder="e.g. User is redirected to dashboard"></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Natural Language Steps -->
      <div v-show="activeTab === 'steps'" class="panel">
        <div class="panel-header">Test Steps (Natural Language)</div>
        <div class="panel-body">
          <StepEditor v-model="formData.steps" />
        </div>
      </div>

      <!-- 4. Automation Parameters -->
      <div v-show="activeTab === 'params'" class="panel">
        <div class="panel-header">Automation Parameters</div>
        <div class="panel-body">
          <div class="form-grid">
            <div class="form-group full-width">
              <label>Run Parameters (JSON)</label>
              <textarea class="tech-input code" v-model="formData.run_param" rows="4" placeholder='{"timeout": 30, "headless": true}'></textarea>
            </div>
            <div class="form-group full-width">
              <label>Assert Configuration (JSON)</label>
              <textarea class="tech-input code" v-model="formData.assert_config" rows="4" placeholder='{"assert_visible": [".header", ".footer"]}'></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- 5. Script Preview & Edit -->
      <div v-show="activeTab === 'script'" class="panel">
        <div class="panel-header">
          <span>Python Script</span>
          <button class="action-btn primary" @click="handleGenerate" :disabled="generating" style="padding: 6px 14px; font-size: 12px;">
            <span>&#9670;</span> {{ generating ? 'Generating...' : 'AI Generate' }}
          </button>
        </div>
        <div class="panel-body">
          <div v-if="generatedScript" class="script-editor-wrapper">
            <textarea class="tech-input code script-editor" v-model="generatedScript" rows="20" spellcheck="false"></textarea>
            <div class="script-actions">
              <button class="action-btn" @click="handleSave">Save Script</button>
            </div>
          </div>
          <div v-else class="empty-script">
            <span class="empty-icon">&#9670;</span>
            <p>Click "AI Generate" to create automation script from test steps</p>
          </div>
        </div>
      </div>

      <!-- 6. Version Comparison -->
      <div v-show="activeTab === 'version'" class="panel">
        <div class="panel-header">Version History & Comparison</div>
        <div class="panel-body">
          <div class="version-selector">
            <div class="form-group">
              <label>Version A</label>
              <select class="tech-input" v-model="versionA">
                <option v-for="v in versions" :key="v.version_num" :value="v.version_num">v{{ v.version_num }} - {{ v.version_type }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Version B</label>
              <select class="tech-input" v-model="versionB">
                <option v-for="v in versions" :key="v.version_num" :value="v.version_num">v{{ v.version_num }} - {{ v.version_type }}</option>
              </select>
            </div>
            <button class="action-btn" @click="handleVersionDiff" style="align-self: flex-end;">Compare</button>
          </div>
          <div v-if="diffResult" style="margin-top: 16px;">
            <VersionCompare :diffText="diffResult" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getAssetDetail, saveAsset, getVersionDiff } from '@/api/knowledge'
import { generateScript } from '@/api/llm'
import StepEditor from '@/components/stepEditor/StepEditor.vue'
import VersionCompare from '@/components/versionCompare/VersionCompare.vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const isNew = computed(() => !route.params.id)
const activeTab = ref('basic')
const generating = ref(false)
const generatedScript = ref('')
const versions = ref([])
const versionA = ref(null)
const versionB = ref(null)
const diffResult = ref('')

const tabs = [
  { key: 'crawl', num: '01', label: 'Crawl Config' },
  { key: 'basic', num: '02', label: 'Basic Info' },
  { key: 'steps', num: '03', label: 'Test Steps' },
  { key: 'params', num: '04', label: 'Auto Params' },
  { key: 'script', num: '05', label: 'Script' },
  { key: 'version', num: '06', label: 'Versions' },
]

const formData = ref({
  asset_name: '', priority: 'P2', engine_type: 'playwright',
  pre_condition: '', post_condition: '', crawler_url: '',
  env_type: '', crawler_rule: '', run_param: '',
  assert_config: '', status: 'draft', steps: [],
})

onMounted(async () => {
  if (!isNew.value) {
    try {
      const res = await getAssetDetail(route.params.id)
      const data = res.data || {}
      formData.value = { ...formData.value, ...data }
      if (!formData.value.steps) formData.value.steps = []
      if (data.versions) versions.value = data.versions
    } catch {}
  }
})

async function handleGenerate() {
  const stepsText = formData.value.steps.map((s, i) => `${i + 1}. ${s.step_content}`).join('\n')
  if (!stepsText) { ElMessage.warning('No test steps defined'); return }
  generating.value = true
  try {
    const res = await generateScript({ steps_text: stepsText, asset_id: route.params.id || undefined, template_type: 'script_gen' })
    generatedScript.value = res.data?.script_content || ''
    ElMessage.success('Script generated')
  } finally { generating.value = false }
}

async function handleSave() {
  await saveAsset({ ...formData.value, id: route.params.id || undefined })
  ElMessage.success('Asset saved')
}

async function handleVersionDiff() {
  if (!versionA.value || !versionB.value) { ElMessage.warning('Select two versions'); return }
  try {
    const res = await getVersionDiff({ asset_id: route.params.id, version_a: versionA.value, version_b: versionB.value })
    const va = JSON.stringify(JSON.parse(res.data?.version_a || '{}'), null, 2)
    const vb = JSON.stringify(JSON.parse(res.data?.version_b || '{}'), null, 2)
    diffResult.value = `--- Version ${versionA.value}\n+++ Version ${versionB.value}\n@@ -1 +1 @@\n-${va.replace(/\n/g, '\n-')}\n+${vb.replace(/\n/g, '\n+')}`
  } catch {}
}
</script>

<style scoped>
.knowledge-edit { max-width: 1100px; margin: 0 auto; }
.edit-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.page-title { font-size: 24px; font-weight: 700; color: var(--text-primary); }
.page-subtitle { font-size: 13px; color: var(--text-muted); margin-top: 4px; }

.edit-tabs { display: flex; gap: 4px; margin-bottom: 0; background: var(--bg-secondary); border-radius: var(--radius-lg) var(--radius-lg) 0 0; padding: 6px; border: 1px solid var(--border-card); border-bottom: none; }
.tab-btn {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px;
  padding: 10px 12px;
  background: transparent; border: none; border-radius: var(--radius-md);
  color: var(--text-muted); font-size: 13px; font-weight: 500; cursor: pointer;
  transition: all var(--transition-fast);
  font-family: var(--font-sans);
}
.tab-btn:hover { color: var(--text-secondary); background: rgba(0, 230, 180, 0.04); }
.tab-btn.active { background: rgba(0, 230, 180, 0.1); color: var(--accent-primary); font-weight: 600; box-shadow: 0 0 8px var(--accent-glow); }
.tab-number { font-family: var(--font-mono); font-size: 11px; opacity: 0.6; }

.tab-content { background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 0 0 var(--radius-lg) var(--radius-lg); box-shadow: var(--shadow-card); }

.panel-header {
  padding: 16px 24px; border-bottom: 1px solid var(--border-subtle);
  font-weight: 600; color: var(--text-primary); font-size: 14px;
  display: flex; justify-content: space-between; align-items: center;
}
.panel-body { padding: 24px; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group.full-width { grid-column: 1 / -1; }
.form-group label { font-size: 12px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }

.tech-input {
  background: var(--bg-input); border: 1px solid var(--border-card);
  border-radius: var(--radius-md); padding: 10px 14px;
  color: var(--text-primary); font-size: 14px; font-family: var(--font-sans);
  box-shadow: var(--shadow-input);
  transition: all var(--transition-fast);
  outline: none;
}
.tech-input:focus { border-color: var(--accent-primary); box-shadow: 0 0 0 1px var(--accent-primary), var(--shadow-input); }
.tech-input.code { font-family: var(--font-mono); font-size: 13px; }
select.tech-input { cursor: pointer; appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23556580' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; padding-right: 36px; }

.empty-script { text-align: center; padding: 60px 20px; color: var(--text-muted); }
.empty-icon { font-size: 40px; display: block; margin-bottom: 12px; color: var(--text-muted); }

.script-editor-wrapper { }
.script-editor { width: 100%; resize: vertical; }
.script-actions { display: flex; justify-content: flex-end; margin-top: 12px; }

.version-selector { display: flex; gap: 16px; align-items: flex-end; }
</style>
