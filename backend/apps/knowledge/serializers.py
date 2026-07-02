from rest_framework import serializers
from apps.knowledge.models import KbCategory, KbAsset, KbAssetStep, KbAssetScript, KbAssetVersion


class KbCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = KbCategory
        fields = '__all__'

    def get_children(self, obj):
        children = KbCategory.objects.filter(parent_id=obj.id).order_by('sort')
        return KbCategorySerializer(children, many=True).data


class KbAssetStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = KbAssetStep
        fields = '__all__'


class KbAssetScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = KbAssetScript
        fields = '__all__'


class KbAssetVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KbAssetVersion
        fields = '__all__'


class KbAssetSerializer(serializers.ModelSerializer):
    steps = KbAssetStepSerializer(many=True, read_only=True)
    scripts = KbAssetScriptSerializer(many=True, read_only=True)

    class Meta:
        model = KbAsset
        fields = '__all__'
        read_only_fields = ('create_time', 'update_time', 'version')
