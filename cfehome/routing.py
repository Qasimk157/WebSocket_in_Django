from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.consumer import AsyncConsumer
# from . import consumers
from chat.consumers import ChatConsumer
# myclass=consumers.ChatConsumer(AsyncConsumer)
# from cfehome.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    # url(r"(ws/orders /)", ChatConsumer)
                    url(r"orders/(?P<username>[\w.@+-]+)/$",ChatConsumer)
                ]
            )
        )
    )
    #empty now for http responce
})
# ws:/ourdomain/<username>
