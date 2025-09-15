from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from datetime import timedelta

class UserToken(models.Model):
    user = models.ForeignKey('api.UserReg', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    refreshToken = models.TextField()
    is_blacklisted = models.BooleanField(default=False)
    blackListed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at :
            self.expires_at = timezone.now() + timedelta(days = 7)

        if self.is_blacklisted and self.blackListed_at is None:
            self.blackListed_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} --- Blacklisted: {self.is_blacklisted} AT {self.blackListed_at}"
    
    class Meta:
        db_table = 'usertoken'
        ordering = ['-created_at']


class UserReg(AbstractUser):
    call_number = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.username}"
    
    class Meta:
        db_table = 'userreg'
        ordering = ['-id']
