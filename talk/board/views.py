from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status

import logging

from .serializer import BoardSerializer
from .models import Board

logger = logging.getLogger(__name__)

class CreateBoardView(APIView):
    permission_classes = [IsAuthenticated]
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
        
class ViewBoard(APIView) :
    permission_classes = [IsAuthenticated]
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
        
class OnceViewBoard(APIView) :
    permission_classes = [IsAuthenticated]
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
        
class UpdateBoard(APIView) :
    permission_classes = [IsAuthenticated]
    def patch(self, request, board_id) :
        board = get_object_or_404(Board, id=board_id, isDeleted=0)
        serializer = BoardSerializer(board, data=request.data, partial=True)  # partial=True는 부분 업데이트 허용
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if serializer:
            return Response({
                "message" : "update board success",
                "data" : BoardSerializer(board).data
            })
        
class DeleteBoard(APIView) :
    permission_classes = [IsAuthenticated]
    def delete(self, request, board_id) :
        board = get_object_or_404(Board, id=board_id, isDeleted=0)
        board.isDeleted = 1
        board.save()

        serializer = BoardSerializer.delete(board)
        if serializer:
            return Response({
                "message" : "delete board success",
                "data" : BoardSerializer(board).data
            })
