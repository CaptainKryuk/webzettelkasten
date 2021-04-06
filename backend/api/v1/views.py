from django.shortcuts import render
from mind.models import Idea, Tag, Article, ContentBlock, BlockImage
from rest_framework import status, viewsets
from rest_framework.decorators import (action, api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from users.models import User
from . import serializers
from django.contrib.auth import login, authenticate
from django.db.models import Q


class SecurityViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )


class UserViewSet(viewsets.ViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)

    
    def create(self, request):
        """
        * user registration
        """
        serializer = serializers.CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            auth = self.jwt_authenticate_user(request, user_data.get('email'), user_data.get('password'))

            if auth['token']:
                # authenticate user
                return Response({'email': user_data.get('email'), 'id': user_data.get('id'), 'token': auth.get('token')})
            return Response("Ошибка при создании пользователя", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        * user registration
        """

        auth = self.jwt_authenticate_user(request, request.data.get('email'), request.data.get('password'))

        if auth['token']:
            # authenticate user
            return Response({'email': auth['user'].get('email'), 'id': auth['user'].get('id'), 'token': auth.get('token')})
        return Response("Пользователь с такой электронной почтой или паролем не найден", status=status.HTTP_400_BAD_REQUEST)


    def jwt_authenticate_user(self, request, email, password):
        """
        * login and get token user after registration or during login function
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        base_user = User.objects.filter(username=email.split('@')[0]).first()
        if not base_user:
            base_user = User.objects.filter(email=email).first()
        user = authenticate(request, username=base_user.username if base_user else 'daun', password=password)

        if user is not None:
            login(request, user)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            user_serializer = serializers.UserSerializer(user)
            return {"token": token, "user": user_serializer.data}
        return {"token": None, "error": "Can't authenticate user."}


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def authentication(self, request):
        """ 
        * check user loged in 
        """
        return Response('success')


class ArticleViewSet(SecurityViewSet):

    def list(self, request):
        """
        * get recent articles
        """
        articles = Article.objects.filter(user=request.user).order_by('-modified')
        serialized_articles = serializers.ArticlesListSerializer(articles, many=True)
        return Response(serialized_articles.data)


    @action(detail=False, methods=['get'])
    def all_articles(self, request):
        articles = Article.objects.filter(user=request.user).order_by('order_number')
        serialized_articles = serializers.ArticlesListSerializer(articles, many=True)
        return Response(serialized_articles.data)
        

    @action(detail=False, methods=['get'])
    def tags_articles(self, request):
        articles = Article.objects.filter(user=request.user)
        tags_dict = {}
        for a in articles:
            for tag in a.tags.all():
                if tag.name in tags_dict:
                    serializer = serializers.ArticlesListSerializer(a)
                    tags_dict[tag.name].append(serializer.data)
                else:
                    serializer = serializers.ArticlesListSerializer(a)
                    tags_dict[tag.name] = [serializer.data]

        return Response(tags_dict)

    

    def create(self, request):
        """
        create artcle and return id
        """
        request.data['user'] = request.user.id
        serializer = serializers.ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """
        update article
        """
        article = Article.objects.filter(id=pk, user=request.user).first()
        if article:
            if 'order_number' in request.data and request.data['order_number'] != article.order_number:
                data_num = request.data['order_number']
                ar_num = article.order_number

                if int(data_num) > int(ar_num):
                    position_holders = Article.objects.filter(order_number__lte=data_num, order_number__gte=article.order_number)
                    for a in position_holders:
                        a.order_number -= 1
                        a.save()
                elif int(data_num) < int(ar_num):
                    position_holders = Article.objects.filter(order_number__gte=data_num, order_number__lte=article.order_number)
                    for a in position_holders:
                        a.order_number += 1
                        a.save()

                article.order_number = data_num
                article.save()
                return Response('success')

            serializer = serializers.ArticleSerializer(article, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('no access', status=status.HTTP_403_FORBIDDEN)
        

    def retrieve(self, request, pk=None):
        """
        get detail article
        """
        article = Article.objects.filter(id=pk, user=request.user).first()
        serialized_data = serializers.ArticleSerializer(article)
        return Response(serialized_data.data)


    def destroy(self, request, pk=None):
        """
        delete article
        """
        article = Article.objects.filter(id=pk, user=request.user).first()
        if article:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('no article', status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=True, methods=['post'])
    def add_tag(self, request, pk=None):
        article = Article.objects.filter(id=pk).first()
        if article:
            article.add_tag(name=request.data['name'], color=request.data['color'])
            article.save()
            tags = [{'name': tag.name, 'color': tag.color} for tag in article.tags.all()]
            return Response(tags)
        return Response(status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['put'])
    def delete_tag(self, request, pk=None):
        article = Article.objects.filter(id=pk, user=request.user).first()
        if article:
            article.remove_tag(request.data['name'])
            article.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    


class ContentBlockViewSet(SecurityViewSet):

    def create(self, request):
        """
        create new block
        """
        serializer = serializers.ContentBlockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, pk=None):
        """
        update content block by id
        """
        block = ContentBlock.objects.filter(id=pk).first()
        if block and block.article.user.id == request.user.id:

            if 'order_number' in request.data and request.data['order_number'] != block.order_number:
                data_num = request.data['order_number']
                b_num = block.order_number

                if int(data_num) > int(b_num):
                    position_holders = ContentBlock.objects.filter(order_number__lte=data_num, order_number__gte=block.order_number)
                    for a in position_holders:
                        a.order_number -= 1
                        a.save()
                elif int(data_num) < int(b_num):
                    position_holders = ContentBlock.objects.filter(order_number__gte=data_num, order_number__lte=block.order_number)
                    for a in position_holders:
                        a.order_number += 1
                        a.save()

                block.order_number = data_num
                block.save()
                return Response('success')


            serializer = serializers.ContentBlockSerializer(block, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('no access', status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        block = ContentBlock.objects.filter(id=pk).first()
        if block:
            block.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)


class BlockImageViewSet(SecurityViewSet):

    def create(self, request):
        serializer = serializers.BlockImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)