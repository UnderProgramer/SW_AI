from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'author', 'createdAt', 'isDeleted']
        read_only_fields = ('author', 'createdAt', 'isDeleted')

    # title 검증
    def validate_title(self, value):
        if value == "":
            raise serializers.ValidationError("Title cannot be empty")
        if len(value) > 50:
            raise serializers.ValidationError("Title exceeds maximum length of 50 characters")
        return value

    # content 검증
    def validate_content(self, value):
        if value == "":
            raise serializers.ValidationError("Content cannot be empty")
        if len(value) > 500:
            raise serializers.ValidationError("Content exceeds maximum length of 500 characters")
        return value