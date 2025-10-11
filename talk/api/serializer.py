from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserToken,UserReg

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username','password','call_number']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            call_number = validated_data['call_number']
        )   
        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    call_number = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        call_number = attrs.get('call_number')

        try:
            user = UserReg.objects.get(username=username)
        except UserReg.DoesNotExist:
            raise serializers.ValidationError("Invaild crendentials")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid crendentials")
        if user.call_number != call_number:
            raise serializers.ValidationError("Invalid Call Number")
        
        refresh = RefreshToken.for_user(user)

        UserToken.objects.create(
            user=user,
            refreshToken=str(refresh)
        )

        attrs['refresh'] = str(refresh)
        attrs['access']= str(refresh.access_token)
        return attrs
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)