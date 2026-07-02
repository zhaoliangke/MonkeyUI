from rest_framework import serializers
from apps.reflux.models import KbRefluxRecord


class KbRefluxRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KbRefluxRecord
        fields = '__all__'
        read_only_fields = ('create_time',)
