from django.urls import path
from .views import (
    test_api,
    UserListCreateView,
    UserDetailView,
    CardListCreateView,
    CardDetailView,
    DoorListCreateView,
    DoorDetailView,
    PermissionListCreateView,
    PermissionDetailView,
    DeviceListCreateView,
    DeviceDetailView,
    AccessLogListCreateView,
    AccessLogDetailView,
    access_check
)


urlpatterns = [
    path('test/', test_api),

    path('users/', UserListCreateView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),

    path('cards/', CardListCreateView.as_view()),
    path('cards/<int:pk>/', CardDetailView.as_view()),

    path('doors/', DoorListCreateView.as_view()),
    path('doors/<int:pk>/', DoorDetailView.as_view()),
    
    path('permissions/', PermissionListCreateView.as_view()),
    path('permissions/<int:pk>/', PermissionDetailView.as_view()),
    
    path('devices/', DeviceListCreateView.as_view()),
    path('devices/<int:pk>/', DeviceDetailView.as_view()),
    
    path('access-logs/', AccessLogListCreateView.as_view()),
    path('access-logs/<int:pk>/', AccessLogDetailView.as_view()),
    
    path('access/check/', access_check),
]