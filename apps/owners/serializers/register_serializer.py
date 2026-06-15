# 文件说明：负责 apps/owners/serializers/register_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    """
    业主注册
    """

    # 姓名
    name = serializers.CharField(
        required=True,  # required必填
        min_length=2,
        max_length=20,
        error_messages={"required": "请输入姓名", "blank": "姓名不能为空"},
    )

    # 手机号
    phone = serializers.CharField(
        required=True,
    )
    id_card = serializers.CharField(
        required=True,
    )
    password = serializers.CharField(write_only=True)  # 隐藏密码
    # 确认密码
    confirm_password = serializers.CharField(write_only=True)
    # 短信验证码
    sms_code = serializers.CharField()
    # 房屋
    house_id = serializers.CharField()
