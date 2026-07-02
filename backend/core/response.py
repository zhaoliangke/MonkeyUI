from rest_framework.response import Response
from rest_framework import status


class ApiResponse:
    @staticmethod
    def success(data=None, message='success', code=200):
        return Response({
            'code': code,
            'message': message,
            'data': data,
        }, status=status.HTTP_200_OK)

    @staticmethod
    def error(message='error', code=400, http_status=None):
        return Response({
            'code': code,
            'message': message,
            'data': None,
        }, status=http_status or status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def created(data=None, message='created'):
        return Response({
            'code': 201,
            'message': message,
            'data': data,
        }, status=status.HTTP_201_CREATED)

    @staticmethod
    def not_found(message='not found'):
        return Response({
            'code': 404,
            'message': message,
            'data': None,
        }, status=status.HTTP_404_NOT_FOUND)
