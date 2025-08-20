from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'author']
        read_only_fields = ('author', 'createdAt')

    def create(self, validated_data):
        # request = self.context.get('request')
        # jwt_auth = JWTAuthentication()

        # try:
        #     auth_header = request.headers.get('Authorization')
        #     if not auth_header:
        #         raise AuthenticationFailed("Authorization 헤더가 없습니다.")

        #     token = auth_header.split()[1] 
        #     validated_token = jwt_auth.get_validated_token(token)
        #     user = jwt_auth.get_user(validated_token)
        # except Exception:
        #     raise AuthenticationFailed("JWT 인증 실패")

        return Board.objects.create(**validated_data)