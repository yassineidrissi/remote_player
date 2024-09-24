from django.urls import path, re_path
from .consumers import RoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/rooms/$', RoomConsumer.as_asgi()),
    # path('tournament/<str:room_name>/', TournamentConsumer.as_asgi()),
    # path('tournament/', RoomConsumer.as_asgi()),
]