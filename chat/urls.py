from django.urls import path, include
from . import views
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:room_id>/', consumers.ChatConsumer.as_asgi()),
]

urlpatterns = [ 
    # Include the WebSocket URL pattern
    path('', include(websocket_urlpatterns)),
    path('rooms/', views.RoomListView.as_view(), name='room-list'),
    path('rooms/<int:room_id>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:room_id>/messages/', views.MessageListView.as_view(), name='message-list'),
    path('rooms/<int:room_id>/messages/<int:message_id>/', views.MessageDetailView.as_view(), name='message-detail'),
    path('roomCreate/',views.RoomCreateAPIView.as_view(), name='room-create'),

 
]

