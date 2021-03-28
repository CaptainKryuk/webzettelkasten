from rest_framework import serializers
from mind.models import Idea, Tag, Article, ContentBlock
from users.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    blocks = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_tags(self, instance):
        return [{'name': tag.name, 'color': tag.color} for tag in instance.tags.all()]

    def get_blocks(self, instance):
        blocks = ContentBlock.objects.filter(article=instance)
        return ContentBlockSerializer(blocks, many=True).data


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = '__all__'


class CreateUserSerializer(serializers.Serializer):
    """
    * serializer for creating user
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, allow_blank=True)

    def create(self, validated_data):
        try:
            user = User.objects.create_user(email=validated_data.get('email'),
                                            password=validated_data.get('password'),
                                            username=validated_data.get('email').split('@')[0])
            return {'email': user.email, 'id': user.id, 'password': validated_data.get('password')}
        except IntegrityError:
            raise serializers.ValidationError({'email': "Пользователь с таким email уже существует"})



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


def get_all_fields_serializer(instance, data, many=False):
    class AllFieldsSerializer(serializers.ModelSerializer):
        class Meta:
            model = instance
            fields = '__all__'

    return AllFieldsSerializer(data, many=many)