# 文件说明：负责 apps/cars/serializers/cars_serializer.py 对应接口的数据序列化、反序列化和参数校验。

from rest_framework import serializers

from apps.cars.models import Car


class CarSerializer(serializers.ModelSerializer):
    """
    车辆序列化器
    """

    owner_name = serializers.CharField(
        source="owner.name",
        read_only=True,
    )

    parking_no = serializers.CharField(
        source="parking.parking_no",
        read_only=True,
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", input_formats=["%Y-%m-%d %H:%M:%S"], allow_null=True
    )

    class Meta:
        model = Car

        fields = "__all__"
