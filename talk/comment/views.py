from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

from .serializer import CommentSerializer

from .models import Comment
from ..board.models import Board

import logging

logger = logging.getLogger(__name__)

class BoardCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            comments = Comment.objects.filter(board_id=id, isDeleted=0)
            serializer = CommentSerializer(comments, many=True)
            return Response({
                "message": "get comments success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"error_msg : {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def post(self, request, id):
        try:
            board = Board.objects.get(id=id)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=404)
        try:

            serializer = CommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                comment = serializer.save(author=request.user, board=board)
                return Response({
                    "message": "comment created successfully",
                    "data": CommentSerializer(comment).data
                }, status=201)
        except Exception as e:
            logger.error(f"error_msg : {e}")
            return Response(f"err_msg : {e}", status=400)
