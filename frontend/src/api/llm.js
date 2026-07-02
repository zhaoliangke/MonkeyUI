import request from '@/utils/request'

export const saveLLMConfig = (data) => request.post('/llm/config/save', data)
export const testLLMConfig = (data) => request.post('/llm/config/test', data)
export const getTemplateList = (params) => request.post('/llm/template/list', params)
export const saveTemplate = (data) => request.post('/llm/template/save', data)
export const generateScript = (data) => request.post('/llm/generate/script', data)
export const getLLMLogList = (params) => request.post('/llm/log/list', params)
