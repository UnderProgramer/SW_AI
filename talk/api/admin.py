from django.contrib import admin
from .models import UserReg,UserToken

@admin.register(UserReg)
class UserRegAdmin(admin.ModelAdmin):
    fields = ['username', 'call_number'] 

@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    fields = ['user','refreshToken', 'created_at', 'is_blacklisted']
