import request from '@/utils/request'

export const getCategoryList = () => request.post('/knowledge/category/list')
export const saveCategory = (data) => request.post('/knowledge/category/save', data)
export const getAssetList = (params) => request.post('/knowledge/asset/list', params)
export const saveAsset = (data) => request.post('/knowledge/asset/save', data)
export const getAssetDetail = (id) => request.get(`/knowledge/asset/detail/${id}`)
export const batchAssets = (data) => request.post('/knowledge/asset/batch', data)
export const saveScript = (data) => request.post('/knowledge/script/save', data)
export const getVersionDiff = (data) => request.post('/knowledge/version/diff', data)
export const getDashboardStats = () => request.post('/knowledge/dashboard/stats')
