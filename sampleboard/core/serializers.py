from rest_framework import serializers
from .models import Marker, SampleBoard, Type


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']


class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = ['id', 'latitude', 'longitude', 'number', 'type']


class SampleBoardSerializer(serializers.ModelSerializer):
    marker = serializers.PrimaryKeyRelatedField(queryset=Marker.objects.all())
    
    class Meta:
        model = SampleBoard
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']