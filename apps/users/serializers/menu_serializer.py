from rest_framework import serializers

from apps.users.models.menu import Menu


class MenuSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            'id',
            'title',
            'icon',
            'path',
            'component',
            'sort',
            'hidden',
            'children'
        ]

    # 形成树结构
    def get_children(self, obj):

        children = Menu.objects.filter(
            parent = obj
        ).order_by('sort')

        return MenuSerializer(
            children,
            many = True
        ).data