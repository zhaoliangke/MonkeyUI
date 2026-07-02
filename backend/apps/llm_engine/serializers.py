from rest_framework import serializers
from apps.llm_engine.models import LlmGlobalConfig, LlmPromptTemplate, LlmGenerateLog


class LlmGlobalConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LlmGlobalConfig
        fields = '__all__'
        read_only_fields = ('create_time', 'update_time')


class LlmPromptTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LlmPromptTemplate
        fields = '__all__'
        read_only_fields = ('create_time',)


class LlmGenerateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LlmGenerateLog
        fields = '__all__'
        read_only_fields = ('create_time',)
