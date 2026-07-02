import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useProjectStore = defineStore('project', () => {
  const currentProjectId = ref(sessionStorage.getItem('projectId') || '')
  const currentProjectName = ref(sessionStorage.getItem('projectName') || '')

  function setProject(id, name) {
    currentProjectId.value = id
    currentProjectName.value = name
    sessionStorage.setItem('projectId', id)
    sessionStorage.setItem('projectName', name)
  }

  return { currentProjectId, currentProjectName, setProject }
})
