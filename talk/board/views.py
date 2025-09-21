from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

import logging

from .serializer import BoardSerializer
from .models import Board

logger = logging.getLogger(__name__)

class CreateBoardView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = BoardSerializer.create(data = request.data, context={'request': request})
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
    def put(self, request, board_id) :
        try:
            board = Board.objects.get(id=board_id, isDeleted=0)
            serializer = BoardSerializer.update(board, data=request.data)
            if serializer:
                return Response({
                    "message" : "update board success",
                    "data" : BoardSerializer(board).data
                })
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteBoard(APIView) :
    permission_classes = [IsAuthenticated]
    def delete(self, request, board_id) :
        try:
            board = Board.objects.get(id=board_id, isDeleted=0)
            serializer = BoardSerializer.delete(board)
            if serializer:
                return Response({
                    "message" : "delete board success",
                    "data" : BoardSerializer(board).data
                })
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
