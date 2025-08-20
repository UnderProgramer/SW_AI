from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers.serializer import UserRegisterSerializer,UserLoginSerializer
from .serializers.boardSerializer import BoardSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

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

class CreateBoardView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        auth_header = request.headers.get('Authorization')
        if not auth_header:
                raise AuthenticationFailed("Authorization 헤더가 없습니다.")
        
        serializer = BoardSerializer(data = request.data, context={'request': request})
        if serializer.is_valid() :
            board = serializer.save(author=request.user)
            return Response({
                "message":"create success",
                "data" : BoardSerializer(board).data
            }, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ViewBoard(APIView) :
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            "message" : "get board success",
            "data" : "hi"
        })