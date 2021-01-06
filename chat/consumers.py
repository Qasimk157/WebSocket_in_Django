import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from chat.models import Thread, ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event): # connection created with client
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        other_user = self.scope['url_route']['kwargs']['username'] # username that login
        me = self.scope['user'] # root user mean admin login user
        thread_obj = await self.get_thread(me,other_user)
        self.thread_obj = thread_obj

        # print(other_user,me)
        # print(thread_obj.id)
        # await asyncio.sleep(8)

    async def websocket_receive(self, event):
        print("receive", event) # recieving data here from server
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            print(msg)

            user = self.scope['user']
            username: 'default'
            if user.is_authenticated:
                username = user.username
            myResponce = {
                'message': msg,
                'username': username
            }
            await self.create_chat_message(user, msg)

            await self.send({
                "type": "websocket.send",
                "text": json.dumps(myResponce)
            })


    async def websocket_disconnect(self,event): ## connection ended
        print("disconnected",event)

    @ database_sync_to_async  ## storing user and root user in db
    def get_thread(self,user,other_username):
        return Thread.objects.get_or_new(user,other_username)[0]

    @ database_sync_to_async
    def create_chat_message(self, me, msg): ## messaging other these things storing into database
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj,user=me,message=msg)
