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
