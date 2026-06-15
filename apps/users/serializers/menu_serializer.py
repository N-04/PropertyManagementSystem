# 文件说明：负责 apps/users/serializers/menu_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.users.models.menu import Menu


class MenuSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()
    parent_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Menu
        fields = [
            "id",
            "title",
            "icon",
            "path",
            "component",
            "sort",
            "hidden",
            "menu_type",
            "parent",
            "parent_id",
            "children",
        ]
        extra_kwargs = {"parent": {"write_only": True, "required": False}}

    # 形成树结构
    def get_children(self, obj):

        children = Menu.objects.filter(parent=obj).order_by("sort")

        return MenuSerializer(children, many=True).data
