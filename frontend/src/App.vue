<template>
  <div class="platform-root">
    <!-- Top Global Bar -->
    <header class="top-bar">
      <div class="top-bar-left">
        <span class="brand-icon">&#9670;</span>
        <span class="brand-text">UI Automation Platform</span>
        <span class="brand-divider">/</span>
        <span class="brand-module">Control Center</span>
      </div>
      <div class="top-bar-center">
        <project-switcher />
      </div>
      <div class="top-bar-right">
        <span class="status-dot online"></span>
        <span class="status-text">System Online</span>
        <span class="top-separator"></span>
        <span class="top-time">{{ currentTime }}</span>
      </div>
    </header>

    <!-- Main Layout -->
    <div class="main-layout">
      <!-- Left Navigation -->
      <aside class="side-nav">
        <nav class="nav-section" v-for="group in navGroups" :key="group.label">
          <div class="nav-group-label">{{ group.label }}</div>
          <router-link
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <span class="nav-icon" v-html="item.icon"></span>
            <span class="nav-text">{{ item.name }}</span>
            <span class="nav-indicator" v-if="isActive(item.path)"></span>
          </router-link>
        </nav>
        <div class="nav-footer">
          <span class="nav-footer-text">Platform v2.0</span>
        </div>
      </aside>

      <!-- Content Area -->
      <main class="content-area">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import ProjectSwitcher from '@/components/projectConfig/ProjectSwitcher.vue'

const route = useRoute()
const currentTime = ref('')

let timer
onMounted(() => {
  timer = setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString('zh-CN', { hour12: false })
  }, 1000)
})
onUnmounted(() => clearInterval(timer))

function isActive(path) {
  return route.path === path || route.path.startsWith(path + '/')
}

const navGroups = [
  {
    label: 'OVERVIEW',
    items: [
      { path: '/dashboard', name: 'Dashboard', icon: '&#9632;' },
    ],
  },
  {
    label: 'CONFIGURATION',
    items: [
      { path: '/project/list', name: 'Projects', icon: '&#9633;' },
      { path: '/llm/setting', name: 'LLM Models', icon: '&#9670;' },
      { path: '/llm/prompt', name: 'Prompts', icon: '&#9638;' },
      { path: '/llm/test', name: 'AI Playground', icon: '&#9654;' },
      { path: '/llm/log', name: 'AI Logs', icon: '&#9776;' },
    ],
  },
  {
    label: 'BUSINESS',
    items: [
      { path: '/knowledge/list', name: 'Assets', icon: '&#9000;' },
      { path: '/crawler/task-list', name: 'Crawler', icon: '&#8981;' },
      { path: '/element/list', name: 'Elements', icon: '&#8982;' },
      { path: '/env/list', name: 'Environments', icon: '&#9881;' },
    ],
  },
  {
    label: 'EXECUTION',
    items: [
      { path: '/run/record', name: 'Run Records', icon: '&#9655;' },
      { path: '/run/batch', name: 'Batch Tasks', icon: '&#9635;' },
      { path: '/reflux/center', name: 'Reflux Center', icon: '&#8635;' },
    ],
  },
  {
    label: 'ADMINISTRATION',
    items: [
      { path: '/system/user', name: 'Users', icon: '&#9787;' },
      { path: '/system/role', name: 'Roles', icon: '&#9733;' },
      { path: '/system/setting', name: 'Settings', icon: '&#9874;' },
    ],
  },
]
</script>

<style>
/* ====== CSS Variables / Design Tokens ====== */
:root {
  --bg-deep: #0a0e17;
  --bg-primary: #0f1623;
  --bg-secondary: #151d2e;
  --bg-card: rgba(21, 29, 46, 0.85);
  --bg-card-hover: rgba(26, 36, 54, 0.95);
  --bg-input: rgba(10, 14, 23, 0.7);
  --bg-glass: rgba(15, 22, 35, 0.6);
  --border-subtle: rgba(64, 128, 255, 0.08);
  --border-card: rgba(64, 128, 255, 0.12);
  --border-active: rgba(0, 230, 180, 0.35);
  --accent-primary: #00e6b4;
  --accent-cyan: #00d4ff;
  --accent-blue: #4d94ff;
  --accent-purple: #8b5cf6;
  --accent-glow: rgba(0, 230, 180, 0.25);
  --accent-glow-strong: rgba(0, 230, 180, 0.45);
  --text-primary: #e8edf5;
  --text-secondary: #8899b4;
  --text-muted: #556580;
  --text-accent: #00e6b4;
  --status-success: #00e6b4;
  --status-warning: #ffb347;
  --status-danger: #ff5c72;
  --status-info: #4d94ff;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(64, 128, 255, 0.06);
  --shadow-glow: 0 0 20px var(--accent-glow), 0 0 0 1px var(--border-active);
  --shadow-input: inset 0 2px 8px rgba(0, 0, 0, 0.4);
  --font-mono: 'SF Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
  --font-sans: 'Inter', 'SF Pro Display', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-smooth: 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* ====== Global Reset ====== */
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; overflow: hidden; }
body {
  font-family: var(--font-sans);
  background: var(--bg-deep);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  font-size: 14px;
  line-height: 1.5;
}
#app { height: 100%; }

/* ====== Element Plus Dark Override ====== */
/* These override Element Plus CSS variables */
.el-card {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-card) !important;
  border-radius: var(--radius-lg) !important;
  box-shadow: var(--shadow-card) !important;
  color: var(--text-primary) !important;
}
.el-card__header {
  border-bottom: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
  font-weight: 600 !important;
}
.el-card__body { color: var(--text-secondary) !important; }

.el-table {
  background: transparent !important;
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: rgba(10, 14, 23, 0.6);
  --el-table-row-hover-bg-color: rgba(0, 230, 180, 0.04);
  --el-table-border-color: var(--border-subtle);
  --el-table-text-color: var(--text-primary);
  --el-table-header-text-color: var(--text-secondary);
  color: var(--text-primary) !important;
}
.el-table th.el-table__cell {
  background: rgba(10, 14, 23, 0.6) !important;
  border-bottom: 2px solid var(--border-card) !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.5px;
  padding: 10px 12px !important;
}
.el-table td.el-table__cell {
  border-bottom: 1px solid var(--border-subtle) !important;
  padding: 10px 12px !important;
}
.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
  background: rgba(15, 22, 35, 0.4) !important;
}

.el-button--primary {
  --el-button-bg-color: var(--accent-primary) !important;
  --el-button-border-color: var(--accent-primary) !important;
  --el-button-text-color: #0a0e17 !important;
  --el-button-hover-bg-color: #33f0c8 !important;
  box-shadow: 0 0 16px var(--accent-glow) !important;
  font-weight: 600 !important;
  border-radius: var(--radius-md) !important;
}
.el-button--success { --el-button-bg-color: rgba(0, 230, 180, 0.2); --el-button-border-color: var(--accent-primary); }
.el-button--warning { --el-button-bg-color: rgba(255, 179, 71, 0.2); --el-button-border-color: var(--status-warning); }
.el-button--danger { --el-button-bg-color: rgba(255, 92, 114, 0.2); --el-button-border-color: var(--status-danger); }
.el-button {
  border-radius: var(--radius-md) !important;
  transition: all var(--transition-fast) !important;
}

.el-input__wrapper {
  background: var(--bg-input) !important;
  border: 1px solid var(--border-card) !important;
  border-radius: var(--radius-md) !important;
  box-shadow: var(--shadow-input) !important;
  transition: all var(--transition-fast) !important;
}
.el-input__inner { color: var(--text-primary) !important; }
.el-input__wrapper:hover { border-color: var(--border-active) !important; }
.el-input__wrapper.is-focus {
  border-color: var(--accent-primary) !important;
  box-shadow: 0 0 0 1px var(--accent-primary), var(--shadow-input) !important;
}

.el-select .el-input__wrapper { background: var(--bg-input) !important; }
.el-select-dropdown { background: var(--bg-secondary) !important; border: 1px solid var(--border-card) !important; }
.el-select-dropdown__item {
  color: var(--text-secondary) !important;
}
.el-select-dropdown__item.hover,
.el-select-dropdown__item:hover { background: rgba(0, 230, 180, 0.1) !important; color: var(--accent-primary) !important; }
.el-select-dropdown__item.selected { color: var(--accent-primary) !important; font-weight: 600 !important; }

.el-tag {
  border-radius: var(--radius-sm) !important;
  border: 1px solid !important;
  font-weight: 500 !important;
}
.el-tag--success { background: rgba(0, 230, 180, 0.12) !important; border-color: rgba(0, 230, 180, 0.3) !important; color: var(--accent-primary) !important; }
.el-tag--warning { background: rgba(255, 179, 71, 0.12) !important; border-color: rgba(255, 179, 71, 0.3) !important; color: var(--status-warning) !important; }
.el-tag--danger { background: rgba(255, 92, 114, 0.12) !important; border-color: rgba(255, 92, 114, 0.3) !important; color: var(--status-danger) !important; }
.el-tag--info { background: rgba(85, 101, 128, 0.12) !important; border-color: rgba(85, 101, 128, 0.3) !important; color: var(--text-muted) !important; }

.el-tabs__header { border-bottom-color: var(--border-subtle) !important; }
.el-tabs__item {
  color: var(--text-secondary) !important;
  font-weight: 500 !important;
}
.el-tabs__item.is-active { color: var(--accent-primary) !important; }
.el-tabs__active-bar { background: var(--accent-primary) !important; box-shadow: 0 0 10px var(--accent-glow); }

.el-dialog {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-card) !important;
  border-radius: var(--radius-xl) !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(64, 128, 255, 0.08) !important;
}
.el-dialog__header { border-bottom: 1px solid var(--border-subtle) !important; }
.el-dialog__title { color: var(--text-primary) !important; font-weight: 600 !important; }

.el-descriptions__title { color: var(--text-primary) !important; }

.el-pagination button,
.el-pager li {
  background: var(--bg-input) !important;
  color: var(--text-secondary) !important;
  border-radius: var(--radius-sm) !important;
}
.el-pager li.is-active { background: var(--accent-primary) !important; color: #0a0e17 !important; }

.el-switch.is-checked .el-switch__core {
  background: var(--accent-primary) !important;
  border-color: var(--accent-primary) !important;
}

/* ====== Platform Layout ====== */
.platform-root { height: 100vh; display: flex; flex-direction: column; background: var(--bg-deep); }

/* Top Bar */
.top-bar {
  height: 52px;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-card);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  z-index: 100;
  backdrop-filter: blur(12px);
}
.top-bar-left { display: flex; align-items: center; gap: 10px; }
.brand-icon { color: var(--accent-primary); font-size: 20px; filter: drop-shadow(0 0 8px var(--accent-glow)); }
.brand-text { color: var(--text-primary); font-weight: 700; font-size: 15px; letter-spacing: 0.5px; }
.brand-divider { color: var(--text-muted); margin: 0 4px; }
.brand-module { color: var(--text-secondary); font-size: 13px; font-weight: 500; letter-spacing: 1px; }
.top-bar-center { display: flex; align-items: center; }
.top-bar-right { display: flex; align-items: center; gap: 8px; }
.status-dot { width: 7px; height: 7px; border-radius: 50%; }
.status-dot.online { background: var(--accent-primary); box-shadow: 0 0 8px var(--accent-glow); }
.status-text { color: var(--text-secondary); font-size: 12px; }
.top-separator { width: 1px; height: 16px; background: var(--border-card); margin: 0 8px; }
.top-time { color: var(--text-muted); font-size: 12px; font-family: var(--font-mono); }

/* Main Layout */
.main-layout { flex: 1; display: flex; overflow: hidden; }

/* Side Navigation */
.side-nav {
  width: 240px;
  background: var(--bg-primary);
  border-right: 1px solid var(--border-card);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 16px 0;
}
.nav-section { margin-bottom: 8px; }
.nav-group-label {
  padding: 8px 20px 4px;
  font-size: 10px;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 1.5px;
  text-transform: uppercase;
}
.nav-item {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  margin: 2px 10px;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 13.5px;
  font-weight: 500;
  transition: all var(--transition-fast);
  position: relative;
  overflow: hidden;
}
.nav-item:hover {
  background: rgba(0, 230, 180, 0.06);
  color: var(--text-primary);
}
.nav-item.active {
  background: rgba(0, 230, 180, 0.1);
  color: var(--accent-primary);
  font-weight: 600;
  box-shadow: inset 0 0 0 1px rgba(0, 230, 180, 0.15);
}
.nav-indicator {
  position: absolute;
  right: 12px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent-primary);
  box-shadow: 0 0 8px var(--accent-glow-strong);
}
.nav-icon { width: 20px; text-align: center; margin-right: 10px; font-size: 14px; opacity: 0.7; }
.nav-item.active .nav-icon { opacity: 1; color: var(--accent-primary); }
.nav-footer {
  margin-top: auto;
  padding: 16px 20px;
  border-top: 1px solid var(--border-card);
}
.nav-footer-text { color: var(--text-muted); font-size: 11px; font-family: var(--font-mono); }

/* Content Area */
.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(0, 230, 180, 0.02) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(77, 148, 255, 0.02) 0%, transparent 50%),
    var(--bg-deep);
}

/* Transitions */
.fade-slide-enter-active { transition: all 0.25s ease-out; }
.fade-slide-leave-active { transition: all 0.15s ease-in; }
.fade-slide-enter-from { opacity: 0; transform: translateY(8px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-4px); }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(64, 128, 255, 0.15); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(64, 128, 255, 0.25); }
</style>
