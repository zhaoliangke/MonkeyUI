import threading
from rest_framework.decorators import api_view
from apps.crawler.models import KbCrawlerTask
from apps.crawler.serializers import KbCrawlerTaskSerializer
from apps.crawler.service import CrawlerService
from core.response import ApiResponse
from core.middleware import get_current_project_id


@api_view(['POST'])
def test_connect(request):
    env_id = request.data.get('env_id')
    credential_id = request.data.get('credential_id')
    result = CrawlerService.test_connectivity(env_id, credential_id)
    return ApiResponse.success(data=result)


@api_view(['POST'])
def start_crawl(request):
    data = request.data.copy()
    data['project_id'] = get_current_project_id()
    data['status'] = 'pending'
    serializer = KbCrawlerTaskSerializer(data=data)
    if not serializer.is_valid():
        return ApiResponse.error(message=str(serializer.errors))
    task = serializer.save()

    thread = threading.Thread(target=CrawlerService.execute_crawl, args=(task.id,), daemon=True)
    thread.start()

    return ApiResponse.success(data=KbCrawlerTaskSerializer(task).data, message='爬取任务已启动')


@api_view(['POST'])
def task_progress(request):
    task_id = request.data.get('id')
    if not task_id:
        return ApiResponse.error(message='请提供任务ID')
    task = KbCrawlerTask.objects.filter(id=task_id).first()
    if not task:
        return ApiResponse.error(message='任务不存在')
    return ApiResponse.success(data=KbCrawlerTaskSerializer(task).data)


@api_view(['POST'])
def task_list(request):
    project_id = get_current_project_id()
    qs = KbCrawlerTask.objects.all()
    if project_id:
        qs = qs.filter(project_id=project_id)
    qs = qs.order_by('-create_time')
    serializer = KbCrawlerTaskSerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def result_save(request):
    task_id = request.data.get('task_id')
    if not task_id:
        return ApiResponse.error(message='请提供任务ID')
    task = KbCrawlerTask.objects.filter(id=task_id).first()
    if not task:
        return ApiResponse.error(message='任务不存在')
    return ApiResponse.success(data={
        'asset_id': task.auto_asset_id,
        'element_count': task.element_count,
        'step_count': task.step_count,
    }, message='爬取结果已关联资产')
