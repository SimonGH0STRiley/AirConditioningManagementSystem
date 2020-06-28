'''
typs for websocket message
CMD - command
MSG - message

Channel Group Name:
Devices
Clients

websocket msg form:
simple msg:
{
    msgType:int,
    message:str
}

device status msg:
{
    msgType:int,
    message:{
        to:"groupName",
        content:{
            trackerID:xxx,
            ip:xxsad,
            name:dd,
            power:0.8,
            position:x,y,z,
            rotation:w,x,y,z,
            softwareVer:1.0,
            playing_scene:2
        }
    }
}

command msg:
{
    msgType:int,
    message:{
        to:'group' / 'single' ,
        ip: xx,
        groupName:xx,
        content:{
            cmd:201,
            cmdInfo:xxx
        }
    }
}

'''

# 特殊指令
ADD_GROUP = 101
LEAVE_GROUP = 102
ADD_WHITELIST = 103
QUERY_DEVICE_STATUS = 104

# 命令类型
COMMAND = 200
CMD_CHANGE_SCENE = COMMAND + 1
CMD_OPENOPTITRACK = COMMAND + 2
CMD_CLOSEOPTITRACK = COMMAND + 3
CMD_CLOSESERVER = COMMAND + 10

# 消息类型
MESSAGE = 300
MESSAGE_BROCAST = MESSAGE + 1
MSG_DEVICE_STATUS = MESSAGE + 2
MSG_DEVICE_STATUS_ALL = MESSAGE + 3
MSG_HEART_BEATS = MESSAGE + 4


OK = 403
ERROR = 404
