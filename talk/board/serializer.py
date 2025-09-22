from rest_framework import serializers
from .models import Board
import json

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'author', 'createdAt', 'isDeleted']
        read_only_fields = ('author', 'createdAt', 'isDeleted')

    def validate_content(self, data) :
        data = json.loads(data)
        if(data['content'] == ""):
            raise serializers.ValidationError("Content cannot be empty")
        if(len(data['content']) > 500):
            raise serializers.ValidationError("Content exceeds maximum length of 500 characters")

    def validate_title(self, data) :
        data = json.loads(data)
        if(data['title'] == ""):
            raise serializers.ValidationError("Title cannot be empty")
        if(len(data['title']) > 50):
            raise serializers.ValidationError("Title exceeds maximum length of 50 characters")

    def create(self, validated_data):
        self.validate_content(validated_data)
        self.validate_title(validated_data)
        
        return Board.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        self.validate_content(validated_data)
        self.validate_title(validated_data)

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    def delete(self, instance):
        instance.isDeleted = 1
        instance.save()
        return instance