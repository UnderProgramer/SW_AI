from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializer import UserRegisterSerializer, UserLoginSerializer, ChangePasswordSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import logging

logger = logging.getLogger(__name__)

class SignUpView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="계정 생성",
        request_body=UserRegisterSerializer,
        responses={status.HTTP_200_OK: "생성 성공"}
    )
    def post(self, request):
        try :
            serial = UserRegisterSerializer(data = request.data)

            if serial.is_valid():
                serial.save()
                return Response({"message":"success"}, status = status.HTTP_201_CREATED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            logger.error(f"error_msg : {e}")
            return Response(f"err_msg : {e}", status = status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="로그인",
        request_body=UserLoginSerializer,
        responses={status.HTTP_200_OK: "로그인성공"}
    )
    def post(self, request):
        try :
            serializer = UserLoginSerializer(data=request.data)

            if serializer.is_valid():
                return Response({
                    "message":"login success",
                    "data" : {
                        "refresh_token": serializer.validated_data['refresh'],
                        "access_token": serializer.validated_data['access']
                    }
                }, status=200)
        except Exception as e :
            logger.error(f"error_msg : {e}")
            return Response({f'err_msg : {e}'}, status = status.HTTP_400_BAD_REQUEST)

class ResetPassword(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="비번 초기화",
        request_body=ChangePasswordSerializer,
        responses={status.HTTP_200_OK: "초기화 성공"}
    )
    def post(self, request):
        try :
            serializer = ChangePasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({"detail": "기존 비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
            user.set_password(new_password)
            user.save()

            return Response({"detail": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e :
            logger.error(f"error_msg : {e}")
            return Response({f'err_msg : {e}'}, status = status.HTTP_400_BAD_REQUEST)