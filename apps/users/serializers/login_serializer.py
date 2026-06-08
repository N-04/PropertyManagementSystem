# 登录序列化器
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):

    # 用户名
    username = serializers.CharField()

    # 密码
    password = serializers.CharField()
