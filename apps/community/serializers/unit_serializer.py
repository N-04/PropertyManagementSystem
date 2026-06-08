from rest_framework import serializers

from apps.community.models import Unit


class UnitSerializer(serializers.ModelSerializer):
    """
    单元序列化器
    """

    building_name = serializers.CharField(
        source="building.name",
        read_only=True,
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Unit

        fields = "__all__"
