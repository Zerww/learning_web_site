from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.users.models import User


class LoginSerializer(serializers.Serializer):
    """User login serializer."""
    username = serializers.CharField(label='用户名')
    password = serializers.CharField(label='密码', style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            if user.status == 0:
                raise serializers.ValidationError('账号已被禁用')
            data['user'] = user
        else:
            raise serializers.ValidationError('请输入用户名和密码')
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    password_confirm = serializers.CharField(label='确认密码', style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def validate_username(self, value):
        if len(value) < 4 or len(value) > 20:
            raise serializers.ValidationError('用户名长度需要在4-20字符之间')
        return value

    def validate_password(self, value):
        if len(value) < 6 or len(value) > 20:
            raise serializers.ValidationError('密码长度需要在6-20字符之间')
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('两次密码输入不一致')
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer for update."""

    class Meta:
        model = User
        fields = ['nickname', 'avatar', 'bio', 'github_url', 'website_url']


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer."""
    old_password = serializers.CharField(label='旧密码', style={'input_type': 'password'})
    new_password = serializers.CharField(label='新密码', style={'input_type': 'password'})
    new_password_confirm = serializers.CharField(label='确认新密码', style={'input_type': 'password'})

    def validate_new_password(self, value):
        if len(value) < 6 or len(value) > 20:
            raise serializers.ValidationError('密码长度需要在6-20字符之间')
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError('两次密码输入不一致')
        return data


class UserPublicSerializer(serializers.ModelSerializer):
    """Public user info serializer."""
    article_count = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'avatar', 'bio',
                  'github_url', 'website_url', 'article_count', 'project_count']

    def get_article_count(self, obj):
        return obj.articles.filter(status=1).count()

    def get_project_count(self, obj):
        return obj.projects.filter(status=1).count()


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user info serializer (authenticated)."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'avatar', 'bio',
                  'role', 'github_url', 'website_url', 'created_at', 'last_login_at']
        read_only_fields = ['id', 'username', 'role', 'created_at']


class UserListSerializer(serializers.ModelSerializer):
    """Admin user list serializer."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'role',
                  'status', 'last_login_at', 'created_at']
