from rest_framework.decorators import api_view
from apps.system.models import SystemConfig, AuditLog
from apps.system.serializers import SystemConfigSerializer, AuditLogSerializer
from core.response import ApiResponse
from django.contrib.auth.models import User


@api_view(['POST'])
def user_list(request):
    keyword = request.data.get('keyword', '')
    qs = User.objects.all()
    if keyword:
        qs = qs.filter(username__icontains=keyword)
    data = [{'id': u.id, 'username': u.username, 'email': u.email, 'is_active': u.is_active,
             'is_staff': u.is_staff, 'date_joined': str(u.date_joined)} for u in qs]
    return ApiResponse.success(data=data)


@api_view(['POST'])
def user_save(request):
    user_id = request.data.get('id')
    username = request.data.get('username', '')
    email = request.data.get('email', '')
    password = request.data.get('password', '')
    is_active = request.data.get('is_active', True)
    is_staff = request.data.get('is_staff', False)

    if user_id:
        user = User.objects.filter(id=user_id).first()
        if not user:
            return ApiResponse.error(message='用户不存在')
        user.username = username or user.username
        user.email = email or user.email
        user.is_active = is_active
        user.is_staff = is_staff
    else:
        if not username:
            return ApiResponse.error(message='请输入用户名')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password or 'default123',
        )
        user.is_staff = is_staff
        user.is_active = is_active

    if password and user_id:
        user.set_password(password)
    user.save()
    return ApiResponse.success(data={'id': user.id, 'username': user.username}, message='保存成功')


@api_view(['POST'])
def role_list(request):
    from django.contrib.auth.models import Group
    qs = Group.objects.all()
    data = [{'id': g.id, 'name': g.name} for g in qs]
    return ApiResponse.success(data=data)


@api_view(['POST'])
def role_save(request):
    from django.contrib.auth.models import Group
    group_id = request.data.get('id')
    name = request.data.get('name', '')
    if not name:
        return ApiResponse.error(message='请输入角色名称')
    if group_id:
        group = Group.objects.filter(id=group_id).first()
        if group:
            group.name = name
            group.save()
    else:
        group = Group.objects.create(name=name)
    return ApiResponse.success(data={'id': group.id, 'name': group.name}, message='保存成功')


@api_view(['POST'])
def setting_get(request):
    configs = SystemConfig.objects.all()
    data = {c.config_key: c.config_value for c in configs}
    return ApiResponse.success(data=data)


@api_view(['POST'])
def setting_save(request):
    configs_data = request.data.get('configs', {})
    for key, value in configs_data.items():
        SystemConfig.objects.update_or_create(
            config_key=key,
            defaults={'config_value': str(value)},
        )
    return ApiResponse.success(message='配置保存成功')


@api_view(['POST'])
def log_list(request):
    qs = AuditLog.objects.all().order_by('-create_time')
    serializer = AuditLogSerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)
