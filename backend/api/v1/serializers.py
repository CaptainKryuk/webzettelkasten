from rest_framework import serializers
from mind.models import Idea, Tag, Article, ContentBlock, BlockImage
from users.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
import datetime


class ArticlesListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    hm_modified = serializers.SerializerMethodField()
    hm_created = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = '__all__'

    def get_hm_modified(self, instance):
        now = datetime.datetime.now()
        delta = now-instance.modified.replace(tzinfo=None)
        return self.valid_date(delta, action="update")

    def get_hm_created(self, instance):
        now = datetime.datetime.now()
        delta = now - instance.created.replace(tzinfo=None)
        return self.valid_date(delta)

    def get_tags(self, instance): 
        return [{'name': tag.name, 'color': tag.color} for tag in instance.tags.all()]

    def valid_date(self, delta, action='created'):
        if delta.seconds < 100:
            return f'{"Создано" if action == "created" else "Изменено"} {delta.seconds if delta.seconds > 0 else 1} секунд назад'
        if delta.seconds / 60 < 60:
            return f'{"Создано" if action == "created" else "Изменено"} {round(delta.seconds / 60)} минут назад'
        if delta.seconds / 3600 < 24:
            return f'{"Создано" if action == "created" else "Изменено"} {round(delta.seconds / 3600)} часов назад'
        return f'{"Создано" if action == "created" else "Изменено"} {delta.days} дней назад'


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
    images = serializers.SerializerMethodField()

    class Meta:
        model = ContentBlock
        fields = '__all__'

    def get_images(self, instance):
        if instance.block_type == 'img':
            queryset = instance.blockimage_set.all()
            return get_all_fields_serializer(BlockImage, queryset, many=True).data
        return []



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


class BlockImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockImage
        fields = '__all__'


def get_all_fields_serializer(instance, data, many=False):
    class AllFieldsSerializer(serializers.ModelSerializer):
        class Meta:
            model = instance
            fields = '__all__'

    return AllFieldsSerializer(data, many=many)

