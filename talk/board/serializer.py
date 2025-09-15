from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'author', 'createdAt', 'isDeleted']
        read_only_fields = ('author', 'createdAt', 'isDeleted')

    def create(self, validated_data):
        return Board.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    def delete(self, instance):
        instance.isDeleted = 1
        instance.save()
        return instance