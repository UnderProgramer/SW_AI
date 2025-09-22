from rest_framework import serializers

from .models import Comment
import json

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'board', 'author', 'content', 'createdAt', 'isDeleted']
        read_only_fields = ('author', 'createdAt', 'isDeleted', 'board')

    def validate(self, value):
        if value == "":
            raise serializers.ValidationError("Title cannot be empty")
        if len(value) > 500:
            raise serializers.ValidationError("Title exceeds maximum length of 50 characters")

    def create(self, validated_data):
        self.validate(validated_data)
        return Comment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        self.validate(validated_data)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    def delete(self, instance):
        instance.isDeleted = 1
        instance.save()
        return instance
