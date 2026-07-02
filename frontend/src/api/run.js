import request from '@/utils/request'

export const executeRun = (data) => request.post('/run/execute', data)
export const executeBatch = (data) => request.post('/run/batch', data)
export const getRecordList = (params) => request.post('/run/record/list', params)
export const getRecordDetail = (data) => request.post('/run/record/detail', data)
