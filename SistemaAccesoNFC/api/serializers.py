from rest_framework import serializers
from .models import User, Card, Door, Permission, Device, AccessLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'email', 'role', 'active']
        
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'uid', 'user', 'active']
        
class DoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = ['id', 'name', 'location', 'active']
        
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'user', 'door', 'day', 'start_time', 'end_time', 'active']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'device_id', 'door', 'active', 'last_seen']
        
class AccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLog
        fields = ['id', 'user', 'card', 'door', 'timestamp', 'result', 'reason'
        ]
        read_only_fields = ['timestamp']
        
class AccessCheckSerializer(serializers.Serializer):
    card_uid = serializers.CharField(max_length=50)
    device_id = serializers.CharField(max_length=100)