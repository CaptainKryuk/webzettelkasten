from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from minds.models import Idea, Tag
from . import serializers
from rest_framework.decorators import action
# Create your views here.

class IdeaViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Idea.objects.all()
        serialized_data = serializers.IdeaSerializer(queryset, many=True).data
        return Response(serialized_data)

    @action(detail=False, methods=['get'])
    def get_tags_ideas(self, request):
        tags = Tag.objects.all()
        ideas = [{
                  'name': tag.name, 
                  'ideas': serializers.IdeaSerializer(tag.idea_set.all(), many=True).data
                } for tag in tags if len(tag.idea_set.all())]
        return Response(ideas)


    def retrieve(self, request, pk=None):
        queryset = Idea.objects.get(id=pk)
        serialized_data = serializers.IdeaSerializer(queryset).data
        return Response(serialized_data)

    def create(self, request):
        serializer = serializers.IdeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if pk != 'undefined':
            queryset = Idea.objects.get(id=pk)
            serializer = serializers.IdeaSerializer(queryset, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(tags=request.data['tags'])
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response('no id')

    @action(detail=True, methods=['put'])
    def add_tag(self, request, pk=None):
        queryset = Idea.objects.get(id=pk)
        queryset.add_tag(request.data['name'])
        return Response(request.data['name'])

    @action(detail=True, methods=['put'])
    def delete_tag(self, request, pk=None):
        queryset = Idea.objects.get(id=pk)
        queryset.remove_tag(request.data['name'])
        return Response(status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        queryset = Idea.objects.get(id=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)