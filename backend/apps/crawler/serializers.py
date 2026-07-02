from rest_framework import serializers
from apps.crawler.models import KbCrawlerTask


class KbCrawlerTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = KbCrawlerTask
        fields = '__all__'
        read_only_fields = ('create_time', 'element_count', 'step_count', 'auto_asset_id')
