"""Custom exception handler."""
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Custom exception handler that returns structured error responses."""
    response = exception_handler(exc, context)

    if response is not None:
        errors = []
        if isinstance(response.data, dict):
            for field, messages in response.data.items():
                if isinstance(messages, list):
                    for msg in messages:
                        errors.append({'field': field, 'message': str(msg)})
                else:
                    errors.append({'field': field, 'message': str(messages)})
        elif isinstance(response.data, list):
            for msg in response.data:
                errors.append({'field': 'detail', 'message': str(msg)})
        else:
            errors.append({'field': 'detail', 'message': str(response.data)})

        response.data = {
            'code': response.status_code,
            'message': errors[0]['message'] if errors else '请求失败',
            'errors': errors,
        }

    return response
