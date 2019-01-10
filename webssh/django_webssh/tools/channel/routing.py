from django.urls import path
from django_webssh.tools.channel import websocket, websocket_pod

websocket_urlpatterns = [
    path('webssh/', websocket.WebSSH),
path('webssh_pod/', websocket_pod.WebSSHPOD),
]