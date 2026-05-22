from rest_framework import serializers

from apps.repairs.models import Repair


class RepairSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:
        model = Repair
        fields = [
            'id',
            'title',
            'content',
            'status',
            'created_at',
            'user'
        ]
        read_only_fields = ['status']

    def get_status(self, obj):
        return obj.get_status_display()