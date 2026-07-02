from rest_framework import serializers
from apps.environment.models import KbEnv, KbCredential
from core.security import aes_encrypt, aes_decrypt, mask_string


class KbEnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = KbEnv
        fields = '__all__'
        read_only_fields = ('create_time', 'update_time')


class KbCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = KbCredential
        fields = '__all__'
        read_only_fields = ('create_time',)


class KbCredentialListSerializer(serializers.ModelSerializer):
    password = serializers.SerializerMethodField()
    cookie = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    class Meta:
        model = KbCredential
        fields = '__all__'

    def get_password(self, obj):
        return mask_string(aes_decrypt(obj.password)) if obj.password else ''

    def get_cookie(self, obj):
        return mask_string(aes_decrypt(obj.cookie)) if obj.cookie else ''

    def get_token(self, obj):
        return mask_string(aes_decrypt(obj.token)) if obj.token else ''
