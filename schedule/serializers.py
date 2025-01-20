from rest_framework import serializers
from .models import Room, ScheduleEntry

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ScheduleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleEntry
        fields = '__all__'

