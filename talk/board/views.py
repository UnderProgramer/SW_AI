from django.http import HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import permissions

import logging

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializer import BoardSerializer
from .models import Board

logger = logging.getLogger(__name__)

class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class BoardView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="board 생성",
        request_body=BoardSerializer,
        responses={200: BoardSerializer}
    )
    def post(self, request):
        try:
            serializer = BoardSerializer(data = request.data, context={'request': request})
            if serializer.is_valid() :
                board = serializer.save(author=request.user)

                return Response({
                    "message":"create success",
                    "data" : BoardSerializer(board).data
                }, status=200)
        except Exception as e:
            logger.error(f"error_msg : {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    



    @swagger_auto_schema(
        operation_description="board 전체 불러오기",
        responses={200: BoardSerializer(many=True)}
    )
    def get(self, request) :
        try:
            boards = Board.objects.filter(isDeleted=0)
            serializer = BoardSerializer(boards, many=True)
            return Response({
                "message" : "get board success",
                "data" : serializer.data
            })
        except Exception as e:
            logger.error(f"error_msg : {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



class BoardWithId(APIView):
    permission_classes = [IsAuthenticated, IsAuthor]

    @swagger_auto_schema(
        operation_description="board 하나 불러오기",
        responses={200: BoardSerializer}
    )
    def get(self, request, board_id) :
        try:
            board = Board.objects.get(id=board_id, isDeleted=0)
            serializer = BoardSerializer(board)
            return Response({
                "message" : "get board success",
                "data" : serializer.data
            })
        except Board.DoesNotExist:
            logger.error(f"error_msg : Board is not exist")
            return Response({"error_msg" : "Board not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"error_msg : {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




    @swagger_auto_schema(
        operation_description="board 업데이트",
        request_body=openapi.Schema(                     # ✅ request_body는 여기
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="게시판 제목"),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description="게시판 내용"),
        },
            required=['title', 'content']
        ),
        responses={200: openapi.Response(
            description="업데이트 성공 응답",
            examples={"message": "update board success"}
        )}
    )
    def patch(self, request, board_id) :
        board = get_object_or_404(Board, id=board_id, isDeleted=0)
        if not IsAuthor().has_object_permission(request, self, board):
            return HttpResponseForbidden("You are not the author.")
        serializer = BoardSerializer(board, data=request.data, partial=True)  # partial=True는 부분 업데이트 허용
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if serializer:
            return Response({
                "message" : "update board success",
                "data" : BoardSerializer(board).data
            })
    



    @swagger_auto_schema(
        operation_description="board 삭제하기",
        responses={200: openapi.Response(
            description="삭제 성공 응답",
            examples={"message": "delete board success"}
        )}
    )
    def delete(self, request, board_id) :
        board = get_object_or_404(Board, id=board_id, isDeleted=0)
        if not IsAuthor().has_object_permission(request, self, board):
            return HttpResponseForbidden("You are not the author.")
        board.isDeleted = 1
        board.save()
        return Response({
            "message" : "delete board success" 
        })
