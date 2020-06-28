from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .msg import *
from .databasectrl import *
import logging
logger = logging.getLogger('')

#Django Channel 的Consumer类，用于web socket 通信和信号分发
class MonitorConsumer(AsyncWebsocketConsumer):

    clientIP = ''
    clientPort = ''

    async def connect(self):
        '''
        这里要记录下 device(主要是IP绑定) 和channel_name的对应关系
        '''
        self.clientIP = self.scope['client'][0]
        self.clientPort = self.scope['client'][1]
        logger.info(' [ws] client: {} connected '.format(self.scope['client']))
        await saveIPChannelObj(self.clientIP, self.clientPort, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'groupName'):
            await self.channel_layer.group_discard(
                self.groupName,
                self.channel_name
            )
        logger.info(' [ws] client: {} disconnected '.format(self.scope['client']))
        await deleteIPChannelObj(self.clientIP, self.clientPort)

    async def receive(self, text_data):
        actions = {
            ADD_GROUP: self.joinGroup,
            MESSAGE_BROCAST:  self.brocastDeviceStatus,
            COMMAND:  self.sendCmdToDevices,
            MSG_HEART_BEATS: self.heartBeats
        }
        textDataJson = json.loads(text_data)
        
        msgType = textDataJson['msgType']
        message = textDataJson['message']
        logger.debug(' [ws] receive wsmsg from: {0}:{1}, msgType:{2}'.format(  self.clientIP, self.clientPort,msgType))
        if msgType in actions:
            await actions[msgType](message)

    async def heartBeats(self,message):
        print("heart beats!")
        await self.send(text_data=json.dumps({
            'msgType': MSG_HEART_BEATS,
            'message': 'Beats'  
        }))

    async def joinGroup(self, groupName):
        self.groupName = groupName
        await self.channel_layer.group_add(
            self.groupName,
            self.channel_name
        )
        logger.info('join group ' + self.groupName)
        await self.send(text_data=json.dumps({
            'msgType': OK,
            'message': 'join group ' + self.groupName
        }))

    async def brocastDeviceStatus(self, message):
        toGroup = message['to']
        status = message['content']

        #print('start update database')
        '''
        updata database here
        '''
        await updateDeviceStatus(status)
       # status['ip'] = await getDeviceIP(status['deviceID'])
        status_msg = {
            'msgType': MSG_DEVICE_STATUS,
            'message': status

        }

        await self.channel_layer.group_send(toGroup, {
            'type': 'deployMessage',
            'message': status_msg
        })

    async def sendCmdToDevices(self, message):
        target = message['to']
        content = message['content']
        cmd_msg = {
            'msgType': COMMAND,
            'message': content
        }
        if str.lower(target) == 'group':
            toGroup = message['groupName']
            await self.channel_layer.group_send(toGroup, {
                'type': 'deployMessage',
                'message': cmd_msg
            })
        else:
            # 根据ip查询对应的channel_name
            targetIP = message['ip']
            targetChannel = await getChannelName(targetIP)
            if targetChannel == '':
                logger.warn(' [ws] commend sended failed, no target {}'.format(targetIP))
            else:    
                await self.channel_layer.send(targetChannel, {'type': 'deployMessage',
                                                          'message': cmd_msg})

    async def deployMessage(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
