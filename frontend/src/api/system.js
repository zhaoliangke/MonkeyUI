import request from '@/utils/request'

export const getUserList = (params) => request.post('/system/user/list', params)
export const saveUser = (data) => request.post('/system/user/save', data)
export const getRoleList = () => request.post('/system/role/list')
export const saveRole = (data) => request.post('/system/role/save', data)
export const getSystemSetting = () => request.post('/system/setting/get')
export const saveSystemSetting = (data) => request.post('/system/setting/save', data)
export const getAuditLogList = () => request.post('/system/log/list')
