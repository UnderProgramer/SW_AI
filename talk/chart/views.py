from django.http import HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializer import chartSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Chart

class ChartView(APIView) :
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="감정 차트 생성",
        operation_description="사용자의 감정 점수를 저장합니다.",
        request_body=chartSerializer,
        description="""
            성공 응답 예시:

            {
                "message": "create success",
                "data": {
                    "id": 3,
                    "sad": 1,
                    "nervous": 1,
                    "happy": 1,
                    "angry": 1,
                    "good": 2,
                    "createdAt": "2025-12-20T02:43:11.763055+09:00",
                    "user": 1
                }
            }
            """
    )
    def post(self, request):
        try:
            serializer = chartSerializer(data=request.data)
            if serializer.is_valid() :
                chart = serializer.save(user=request.user)

                return Response({
                    "message":"create success",
                    "data" : chartSerializer(chart).data
                }, status=200)
        except Exception as e :
            return Response({"error": str(e)})
        

    @swagger_auto_schema(
        operation_summary="감정 차트 조회",
        operation_description="로그인한 사용자의 감정 차트 목록을 조회합니다.",
        description="""
            성공 응답 예시:

            {
                "message": "get success",
                "data": [
                    {
                        "id": 1,
                        "sad": 1,
                        "nervous": 2,
                        "happy": 3,
                        "angry": 4,
                        "good": 5,
                        "createdAt": "2025-12-20T02:25:17+09:00",
                        "user": 1
                    }
                ]
            }
            """
    )
    def get(self, request) :
        try:
            charts = Chart.objects.filter(user=request.user)
            return Response({
                "message":"get success",
                "data" : chartSerializer(charts, many=True).data
            })
        except Exception as e :
            return Response({"error": str(e)})