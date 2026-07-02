import request from '@/utils/request'

export const getEnvList = () => request.post('/env/env/list')
export const saveEnv = (data) => request.post('/env/env/save', data)
export const getCredentialList = (params) => request.post('/env/credential/list', params)
export const saveCredential = (data) => request.post('/env/credential/save', data)
