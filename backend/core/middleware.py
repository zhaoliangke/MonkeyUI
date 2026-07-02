import threading
import json
import logging
from django.utils.deprecation import MiddlewareMixin
from core.exception import ForbiddenException

_thread_locals = threading.local()

audit_logger = logging.getLogger('audit')


def get_current_project_id():
    return getattr(_thread_locals, 'project_id', None)


def set_current_project_id(project_id):
    _thread_locals.project_id = project_id


class ProjectIsolationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        project_id = request.headers.get('X-Project-ID') or request.GET.get('project_id')
        if project_id:
            try:
                set_current_project_id(int(project_id))
            except (ValueError, TypeError):
                set_current_project_id(None)
        else:
            set_current_project_id(None)

    def process_response(self, request, response):
        set_current_project_id(None)
        return response


class AuditLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            audit_logger.info(
                'user=%s method=%s path=%s status=%s project_id=%s',
                getattr(request, 'user', 'anonymous'),
                request.method,
                request.path,
                response.status_code,
                get_current_project_id(),
            )
        return response
