from django.db import models
from django.utils import timezone

class Chart(models.Model):
    user=models.ForeignKey('api.UserReg', on_delete=models.CASCADE)
    sad = models.IntegerField()
    nervous = models.IntegerField()
    happy = models.IntegerField()
    angry = models.IntegerField()
    good = models.IntegerField()
    createdAt = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'chart'
        ordering = ['-createdAt']