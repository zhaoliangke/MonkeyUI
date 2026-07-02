import request from '@/utils/request'

export const getRefluxList = (params) => request.post('/reflux/list', params)
export const getRefluxDetail = (data) => request.post('/reflux/detail', data)
export const auditReflux = (data) => request.post('/reflux/audit', data)
export const rollbackReflux = (data) => request.post('/reflux/rollback', data)
export const triggerReflux = (data) => request.post('/reflux/trigger', data)
export const getRefluxStats = () => request.post('/reflux/stats', {})
