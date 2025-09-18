from django.db import models
from django.utils import timezone

class Comment(models.Model):
    title = models.TextField()
    content = models.TextField()
    board = models.ForeignKey('api.Board', on_delete=models.CASCADE)
    isDeleted = models.SmallIntegerField(default=0)
    createdAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"title : {self.title} / content : {self.content} --- author : {self.author if self.author else 'Unknown'}"
    
    class Meta:
        db_table = 'comment'
        ordering = ['-createdAt']
        