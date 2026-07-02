import request from '@/utils/request'

export const testCrawlerConnect = (data) => request.post('/crawler/test-connect', data)
export const startCrawl = (data) => request.post('/crawler/start', data)
export const getCrawlProgress = (data) => request.post('/crawler/progress', data)
export const getCrawlerTaskList = (data) => request.post('/crawler/task/list', data)
export const saveCrawlResult = (data) => request.post('/crawler/result/save', data)
