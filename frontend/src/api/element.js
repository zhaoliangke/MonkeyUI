import request from '@/utils/request'

export const getElementList = (params) => request.post('/element/list', params)
export const saveElement = (data) => request.post('/element/save', data)
export const repairElement = (data) => request.post('/element/repair', data)
export const getRelatedCases = (data) => request.post('/element/related-cases', data)
