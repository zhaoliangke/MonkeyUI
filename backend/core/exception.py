from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated, PermissionDenied, NotFound
from core.response import ApiResponse


class BusinessException(Exception):
    def __init__(self, message='业务异常', code=400):
        self.message = message
        self.code = code
        super().__init__(message)


class AuthException(Exception):
    def __init__(self, message='认证失败'):
        self.message = message
        self.code = 401
        super().__init__(message)


class NotFoundException(Exception):
    def __init__(self, message='资源不存在'):
        self.message = message
        self.code = 404
        super().__init__(message)


class ForbiddenException(Exception):
    def __init__(self, message='无权限访问'):
        self.message = message
        self.code = 403
        super().__init__(message)


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is not None:
        return ApiResponse.error(
            message=str(exc.detail) if hasattr(exc, 'detail') else str(exc),
            code=response.status_code,
            http_status=response.status_code,
        )

    if isinstance(exc, BusinessException):
        return ApiResponse.error(message=exc.message, code=exc.code)
    if isinstance(exc, AuthException):
        return ApiResponse.error(message=exc.message, code=exc.code, http_status=401)
    if isinstance(exc, NotFoundException):
        return ApiResponse.error(message=exc.message, code=exc.code, http_status=404)
    if isinstance(exc, ForbiddenException):
        return ApiResponse.error(message=exc.message, code=exc.code, http_status=403)

    return ApiResponse.error(message='服务器内部错误', code=500, http_status=500)
