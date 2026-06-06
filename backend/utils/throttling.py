"""Custom throttling rates."""
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    scope = 'login'


class UploadRateThrottle(UserRateThrottle):
    scope = 'upload'


class CommentRateThrottle(UserRateThrottle):
    scope = 'comment'
