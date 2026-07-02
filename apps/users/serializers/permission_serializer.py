# 文件说明：负责 apps/users/serializers/permission_serializer.py 对应接口的数据序列化、反序列化和参数校验。

# =====================================================
# 导入 DRF 序列化器
# =====================================================

from rest_framework import serializers

# =====================================================
# 导入权限模型
# =====================================================
from apps.users.models.permission import Permission

# =====================================================
# 权限序列化器
# =====================================================


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:

        # 权限模型
        model = Permission

        # 所有字段
        fields = "__all__"
