import request from '@/utils/request'

export const getProjectList = (params) => request.post('/project/list', params)
export const saveProject = (data) => request.post('/project/save', data)
export const setDefaultProject = (id) => request.post('/project/set-default', { id })
export const saveProjectPermission = (data) => request.post('/project/permission/save', data)
export const deleteProject = (id) => request.post('/project/delete', { id })
