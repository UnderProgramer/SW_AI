from rest_framework import serializers
from .models import Chart

class chartSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Chart
        fields = '__all__'
        read_only_fields = ['user', 'createdAt']

        