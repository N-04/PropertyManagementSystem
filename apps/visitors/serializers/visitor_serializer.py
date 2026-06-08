from rest_framework import serializers
from apps.visitors.models import Visitor


class VisitorSerializer(serializers.ModelSerializer):

    owner_name = serializers.CharField(source="owner.name", read_only=True)

    visit_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )

    class Meta:
        model = Visitor

        fields = "__all__"
