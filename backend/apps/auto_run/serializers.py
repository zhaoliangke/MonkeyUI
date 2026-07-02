from rest_framework import serializers
from apps.auto_run.models import KbRunRecord


class KbRunRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KbRunRecord
        fields = '__all__'
        read_only_fields = ('run_time',)
