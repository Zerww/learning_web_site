"""Custom API response helpers — return DRF Response objects."""

from rest_framework.response import Response


def success(data=None, message='success', code=200):
    """Build a success Response."""
    result = {'code': code, 'message': message}
    if data is not None:
        result['data'] = data
    return Response(result, status=code)


def success_list(items, pagination=None, message='success', code=200):
    """Build a paginated list success Response."""
    payload = {
        'code': code,
        'message': message,
        'data': {'list': items},
    }
    if pagination:
        payload['data']['pagination'] = pagination
    return Response(payload, status=code)


def created(data=None, message='创建成功'):
    """Build a created success Response (HTTP 201)."""
    result = {'code': 201, 'message': message}
    if data is not None:
        result['data'] = data
    return Response(result, status=201)


def error(message='请求失败', code=400, errors=None):
    """Build an error Response."""
    result = {'code': code, 'message': message}
    if errors:
        result['errors'] = errors
    return Response(result, status=code)
