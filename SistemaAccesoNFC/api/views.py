from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from .models import User, Card, Door, Permission, Device, AccessLog
from .serializers import UserSerializer, CardSerializer, DoorSerializer, PermissionSerializer, DeviceSerializer, AccessLogSerializer, AccessCheckSerializer
from .services import check_access


@api_view(['GET'])
def test_api(request):
    return Response({
        'message': 'API funcionando correctamente'
    })


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class CardListCreateView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    
class DoorListCreateView(generics.ListCreateAPIView):
    queryset = Door.objects.all()
    serializer_class = DoorSerializer


class DoorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Door.objects.all()
    serializer_class = DoorSerializer
    
class PermissionListCreateView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    
class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    
class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    
class AccessLogListCreateView(generics.ListCreateAPIView):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer

class AccessLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessLog.objects.all()
    serializer_class = AccessLogSerializer
    

@api_view(['POST'])
def access_check(request):
    serializer = AccessCheckSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=400
        )

    result = check_access(
        card_uid=serializer.validated_data['card_uid'],
        device_id=serializer.validated_data['device_id']
    )

    return Response(result)
