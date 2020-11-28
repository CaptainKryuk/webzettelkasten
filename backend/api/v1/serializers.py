from rest_framework import serializers
from minds.models import Idea, Tag

class IdeaSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Idea
        fields = '__all__'

    def get_tags(self, instance):
        return [{'name': tag.name, 'color': tag.color} for tag in instance.tags.all()]

    def update(self, instance, validated_data):
        if 'tags' in validated_data and len(validated_data.get('tags')) != instance.tags.count():
            instance.update_tags(validated_data.get('tags'))
        validated_data.pop('tags')
        return super(IdeaSerializer, self).update(instance, validated_data)