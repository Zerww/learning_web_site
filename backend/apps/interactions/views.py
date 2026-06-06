from django.db import models
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.interactions.models import Favorite, Like
from apps.interactions.serializers import FavoriteSerializer, LikeSerializer
from utils.response import error, success


class LikeViewSet(viewsets.ViewSet):
    """Like/unlike endpoints."""

    def get_permissions(self):
        if self.action in ['status', 'create', 'destroy']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_likes(self, request):
        """List current user's liked items."""
        likes = Like.objects.filter(user=request.user).order_by('-created_at')[:50]
        data = []
        for like in likes:
            content = self._liked_content(like.content_type, like.object_id)
            data.append({
                'id': like.id,
                'content_type': like.content_type,
                'object_id': like.object_id,
                'content': content,
                'created_at': like.created_at,
            })
        return success({'list': data})

    def _liked_content(self, ct, oid):
        model_map = {
            1: ('articles', 'Article', ['id', 'title', 'cover_image', 'summary']),
            2: ('projects', 'Project', ['id', 'title', 'cover_image', 'description']),
            3: ('notes', 'Note', ['id', 'title']),
        }
        if ct in model_map:
            app, model_name, fields = model_map[ct]
            model = self._get_model(app, model_name)
            if model:
                obj = model.objects.filter(id=oid).values(*fields).first()
                return obj
        return None

    def create(self, request):
        serializer = LikeSerializer(data=request.data)
        if not serializer.is_valid():
            return error('参数错误', code=400, errors=serializer.errors)

        ct = serializer.validated_data['content_type']
        oid = serializer.validated_data['object_id']

        user = request.user if request.user.is_authenticated else None
        anonymous_id = request.META.get('REMOTE_ADDR') if not user else None

        like, created = Like.objects.get_or_create(
            content_type=ct, object_id=oid,
            user=user, anonymous_id=anonymous_id,
            defaults={'ip_address': request.META.get('REMOTE_ADDR')},
        )

        if created:
            self._increment_count(ct, oid, 'like_count')
            return success({'like_count': self._get_count(ct, oid, 'like_count'),
                           'is_liked': True}, message='点赞成功')
        return success({'like_count': self._get_count(ct, oid, 'like_count'),
                       'is_liked': True}, message='已点赞')

    def destroy(self, request):
        serializer = LikeSerializer(data=request.data)
        if not serializer.is_valid():
            return error('参数错误', code=400, errors=serializer.errors)

        ct = serializer.validated_data['content_type']
        oid = serializer.validated_data['object_id']

        user = request.user if request.user.is_authenticated else None
        anonymous_id = request.META.get('REMOTE_ADDR') if not user else None

        deleted, _ = Like.objects.filter(
            content_type=ct, object_id=oid,
            user=user, anonymous_id=anonymous_id,
        ).delete()

        if deleted:
            self._decrement_count(ct, oid, 'like_count')
            return success({'like_count': self._get_count(ct, oid, 'like_count'),
                           'is_liked': False}, message='取消点赞成功')
        return success({'like_count': self._get_count(ct, oid, 'like_count'),
                       'is_liked': False}, message='未点赞')

    @action(detail=False, methods=['get'])
    def status(self, request):
        content_type = request.query_params.get('content_type')
        object_id = request.query_params.get('object_id')
        if not content_type or not object_id:
            return error('缺少参数', code=400)
        is_liked = False
        user = request.user if request.user.is_authenticated else None
        if user:
            is_liked = Like.objects.filter(
                content_type=content_type, object_id=object_id, user=user
            ).exists()
        return success({
            'is_liked': is_liked,
            'like_count': self._get_count(content_type, object_id, 'like_count'),
        })

    def _increment_count(self, ct, oid, field):
        self._update_count(ct, oid, field, 1)

    def _decrement_count(self, ct, oid, field):
        self._update_count(ct, oid, field, -1)

    def _update_count(self, ct, oid, field, delta):
        model_map = {1: ('articles', 'Article'), 2: ('projects', 'Project'),
                     3: ('notes', 'Note'), 4: ('comments', 'Comment')}
        if ct in model_map:
            app, model_name = model_map[ct]
            model = self._get_model(app, model_name)
            if model:
                model.objects.filter(id=oid).update(**{field: models.F(field) + delta})

    def _get_model(self, app, model_name):
        from django.apps import apps
        try:
            return apps.get_model(app, model_name)
        except LookupError:
            return None

    def _get_count(self, ct, oid, field):
        model_map = {1: ('articles', 'Article'), 2: ('projects', 'Project'),
                     3: ('notes', 'Note')}
        if int(ct) in model_map:
            app, model_name = model_map[int(ct)]
            model = self._get_model(app, model_name)
            if model:
                obj = model.objects.filter(id=oid).first()
                if obj:
                    return getattr(obj, field, 0)
        return 0


class FavoriteViewSet(viewsets.ViewSet):
    """Favorite/unfavorite endpoints."""
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error('参数错误', code=400, errors=serializer.errors)

        ct = serializer.validated_data['content_type']
        oid = serializer.validated_data['object_id']
        folder = serializer.validated_data.get('folder_name')

        favorite, created = Favorite.objects.get_or_create(
            content_type=ct, object_id=oid, user=request.user,
            defaults={'folder_name': folder},
        )

        if created:
            self._increment_count(ct, oid)
            return success({
                'favorite_count': self._get_count(ct, oid),
                'is_favorited': True,
            }, message='收藏成功')
        return success({
            'favorite_count': self._get_count(ct, oid),
            'is_favorited': True,
        }, message='已收藏')

    def destroy(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error('参数错误', code=400, errors=serializer.errors)

        ct = serializer.validated_data['content_type']
        oid = serializer.validated_data['object_id']

        deleted, _ = Favorite.objects.filter(
            content_type=ct, object_id=oid, user=request.user
        ).delete()

        if deleted:
            self._decrement_count(ct, oid)
            return success({
                'favorite_count': self._get_count(ct, oid),
                'is_favorited': False,
            }, message='取消收藏成功')
        return success({
            'favorite_count': self._get_count(ct, oid),
            'is_favorited': False,
        }, message='未收藏')

    def list(self, request):
        content_type = request.query_params.get('content_type')
        folder_name = request.query_params.get('folder_name')

        qs = Favorite.objects.filter(user=request.user)
        if content_type:
            qs = qs.filter(content_type=content_type)
        if folder_name:
            qs = qs.filter(folder_name=folder_name)

        qs = qs.order_by('-created_at')[:50]

        results = []
        for fav in qs:
            content = self._get_content(fav.content_type, fav.object_id)
            results.append({
                'id': fav.id,
                'content_type': fav.content_type,
                'object_id': fav.object_id,
                'folder_name': fav.folder_name,
                'content': content,
                'created_at': fav.created_at,
            })
        return success({'list': results})

    def _get_content(self, ct, oid):
        model_map = {1: ('articles', 'Article', ['id', 'title', 'cover_image', 'summary']),
                     2: ('projects', 'Project', ['id', 'title', 'cover_image', 'description']),
                     3: ('notes', 'Note', ['id', 'title'])}
        if ct in model_map:
            app, model_name, fields = model_map[ct]
            model = self._get_model(app, model_name)
            if model:
                obj = model.objects.filter(id=oid).values(*fields).first()
                return obj
        return None

    def _get_model(self, app, model_name):
        from django.apps import apps
        try:
            return apps.get_model(app, model_name)
        except LookupError:
            return None

    def _increment_count(self, ct, oid):
        self._update_count(ct, oid, 1)

    def _decrement_count(self, ct, oid):
        self._update_count(ct, oid, -1)

    def _update_count(self, ct, oid, delta):
        model_map = {1: ('articles', 'Article'), 2: ('projects', 'Project'),
                     3: ('notes', 'Note')}
        if ct in model_map:
            app, model_name = model_map[ct]
            model = self._get_model(app, model_name)
            if model:
                model.objects.filter(id=oid).update(
                    **{'favorite_count': models.F('favorite_count') + delta}
                )

    def _get_count(self, ct, oid):
        model_map = {1: ('articles', 'Article'), 2: ('projects', 'Project'),
                     3: ('notes', 'Note')}
        if ct in model_map:
            app, model_name = model_map[ct]
            model = self._get_model(app, model_name)
            if model:
                obj = model.objects.filter(id=oid).first()
                return getattr(obj, 'favorite_count', 0) if obj else 0
        return 0
