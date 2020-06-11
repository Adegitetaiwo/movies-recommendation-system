from rest_framework import serializers
from .models import movieInputModel

class movieInputSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = movieInputModel
        fields = '__all__'

