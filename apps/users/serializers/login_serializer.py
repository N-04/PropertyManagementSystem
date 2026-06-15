# 文件说明：负责 apps/users/serializers/login_serializer.py 对应接口的数据序列化、反序列化和参数校验。

# 登录序列化器
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):

    # 用户名
    username = serializers.CharField()

    # 密码
    password = serializers.CharField()
