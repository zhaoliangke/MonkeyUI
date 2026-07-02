from rest_framework import serializers
from apps.element_lib.models import KbElement


class KbElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = KbElement
        fields = '__all__'
        read_only_fields = ('create_time', 'update_time')
