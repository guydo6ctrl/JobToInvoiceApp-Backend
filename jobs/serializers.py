from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Job
        fields = ['client', 'title', 'description', 'date_created', 'completed']

    