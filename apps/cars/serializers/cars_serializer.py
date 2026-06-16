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

    car_type_text = serializers.CharField(source="get_car_type_display", read_only=True)

    status_text = serializers.CharField(source="get_status_display", read_only=True)

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Car

        fields = "__all__"
