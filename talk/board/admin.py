from django.contrib import admin
from .models import Board

@admin.register(Board)
class UserBoardAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'author']