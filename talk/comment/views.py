from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

from .serializer import CommentSerializer

from .models import Comment

import logging

logger = logging.getLogger(__name__)

class BoardCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, board_id):
        try:
            comments = Comment.objects.filter(board_id=board_id, isDeleted=0)
            serializer = CommentSerializer(comments, many=True)
            return Response({
                "message": "get comments success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"error_msg : {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, board_id):
        try:
            serializer = CommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                comment = serializer.save(author=request.user, board_id=board_id)
                return Response({
                    "message": "comment created successfully",
                    "data": CommentSerializer(comment).data
                }, status=status.HTTP_201_CREATED)
            logger.error(f"error_msg : {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"error_msg : {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)