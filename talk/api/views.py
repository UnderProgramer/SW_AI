from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializer import UserRegisterSerializer,UserLoginSerializer

class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serial = UserRegisterSerializer(data = request.data)

        if serial.is_valid():
            serial.save()
            return Response({"message":"success"}, status = status.HTTP_201_CREATED)
        
        return Response(serial.errors, status = status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response({
                "message":"login success",
                "data" : {
                    "refresh_token": serializer.validated_data['refresh'],
                    "access_token": serializer.validated_data['access']
                }
            }, status=200)
        
        return Response({'ERROR':serializer.errors}, status=400)

