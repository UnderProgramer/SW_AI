from rest_framework import serializers

from .models import Comment
import json

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'board', 'author', 'content', 'createdAt', 'isDeleted']
        read_only_fields = ('author', 'createdAt', 'isDeleted', 'board')

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        if len(value) > 500:
            raise serializers.ValidationError("Content exceeds 500 characters.")
        return value