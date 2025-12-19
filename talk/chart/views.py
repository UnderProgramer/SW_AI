from django.http import HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializer import chartSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

from .models import Chart

class ChartView(APIView) :
    permission_classes = [IsAuthenticated]

    @method_decorator(
        name='post',
        decorator=swagger_auto_schema(
            operation_summary="차트 생성",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["sad", "nervous", "happy", "angry", "good"],
                properties={
                    "sad": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "nervous": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "happy": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "angry": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "good": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                },
            ),
            responses={
                200: openapi.Response(
                    description="create success",
                    examples={
                        "application/json": {
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
                    }
                )
            }
        )
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

    @method_decorator(
        name='get',
        decorator=swagger_auto_schema(
            operation_summary="차트 조회",
            responses={
                200: openapi.Response(
                    description="get success",
                    examples={
                        "application/json": {
                            "message": "get success",
                            "data": [
                                {
                                    "id": 3,
                                    "sad": 1,
                                    "nervous": 1,
                                    "happy": 1,
                                    "angry": 1,
                                    "good": 2,
                                    "createdAt": "2025-12-20T02:43:11.763055+09:00",
                                    "user": 1
                                },
                                {
                                    "id": 2,
                                    "sad": 1,
                                    "nervous": 1,
                                    "happy": 1,
                                    "angry": 1,
                                    "good": 1,
                                    "createdAt": "2025-12-20T02:25:51.707610+09:00",
                                    "user": 1
                                }
                            ]
                        }
                    }
                )
            }
        )
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