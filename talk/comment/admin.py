from django.contrib import admin

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ['board', 'author', 'content', 'isDeleted', 'createdAt']
    readonly_fields = ['createdAt', 'isDeleted']
# Register your models here.
