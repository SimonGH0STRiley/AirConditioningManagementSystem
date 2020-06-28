/* Http Restful Api 接口，访问服务器获取设备列表和状态 */

import axios from "axios";

const METHOD = {
    http: 0,
    websocket: 1
};

const MESSAGE = {
    ADD_GROUP: 101,
    LEAVE_GROUP: 102,
    ADD_WHITELIST: 103,
    QUERY_DEVICE_STATUS: 104,

    COMMAND: 200,
    CMD_CLOSE_SERVER: 210,

    MESSAGE: 300,
    MESSAGE_BROAD_CAST: 301,
    MSG_ROOM_STATUS: 302,
    MSG_ROOM_STATUS_ALL: 303,
    MSG_HEART_BEATS: 304,

    OK: 403,
    ERROR: 404
}

const serverUrl = '192.168.0.183:8000';

let roomList = [];
let roomMap = new Map();
let updateMethod = METHOD.http;
let websocket = null;
let interval = null;


//设置更新模式
function setUpdateMode(mode) {
    if (mode in METHOD) {
        updateMethod = METHOD[mode];
    }
}

//初始化设备列表，主要是初始化 逻辑ID和名称之间的对应关系
function initialList() {
    clear();
    axios.get("http://" + serverUrl + "/api/rooms/")
        .then(response => {
            for (let index = 0; index < response.data.length; index++) {
                let room = {
                    roomNumber: response.data[index].roomNumber,
                    isActive: response.data[index].isActive,
                    currentTemperature: 20,
                    currentSpeed: 0,
                    AC: {
                        isACActive: false,
                        targetTemperature: 20,
                        targetSpeed: 0,
                        requestStatus: 'ready'
                    },
                    updateTime: null, //该设备更新的时间戳
                };

                roomMap.set(room.roomNumber, room);
                roomList.push(room)
            }
        })
        .catch(error => {
            alert("从服务器获取房间列表失败");
            window.console.log("error: " + error);
        });
}

//获取整个房间列表
function getRoomList() {
    return roomList;
}

//根据房间号来获取对应的设备信息
function getRoomByNumber(targetRoomNumber) {
    if (roomList.length === 0) {
        return null;
    }
    for (let currentRoom in roomList) {
        if (currentRoom.roomNumber === targetRoomNumber) {
            return currentRoom;
        }
    }
    return null;
}


//Http 请求更新房间列表状态信息
function updateRoomList(){
    if (updateMethod === METHOD.websocket) {
        updateRoomListByWS();
    } else {
        updateRoomListByHttp();
    }
}

//通过http轮询的方式监听和更新房间状态
function updateRoomListByHttp() {
    interval = window.setInterval(() => {
        window.console.log("update by http");
        axios.get("http://" + serverUrl + "/api/room_status/")
            .then(response => {
                for (let index = 0; index < response.data.length; index++) {
                    let roomStatus = response.data[index];
                    if (roomMap.get(roomStatus.roomNumber)) {
                        let room = roomMap.get(roomStatus.roomNumber);
                        room.isActive = roomStatus.isActive;
                        room.currentTemperature = roomStatus.currentTemperature;
                        room.currentSpeed = roomStatus.currentSpeed;
                        room.AC.isACActive = roomStatus.AC.isACActive;
                        room.AC.targetTemperature = roomStatus.AC.targetTemperature;
                        room.AC.targetSpeed = roomStatus.AC.targetSpeed;
                        room.AC.requestStatus = roomStatus.AC.requestStatus;
                        room.updateTime = new Date().getTime();
                    }
                }
            })
            .catch(error => {
                window.console.log("error: " + error);
            });
    }, 2000);
}

//通过websocket的方式监听和更新设备状态
function updateRoomListByWS() {
    if (websocket != null) {
        websocket.close();
    }
    websocket = new WebSocket("ws://" + serverUrl + "/ws/monitor/");
    websocket.onmessage = onMessageReceived;
    websocket.onopen = event => {

        webSocketPulse.reset().start();
        let addGroup = {
            msgType: 101,
            message: "Clients"
        };

        if (websocket.readyState === websocket.OPEN) {
            //若是ws开启状态
            websocket.send(JSON.stringify(addGroup));
        } else if (websocket.readyState === websocket.CONNECTING) {
            // 若是正在开启状态，则等待1s后重新调用
            window.setTimeout(() => {
                websocket.send(JSON.stringify(addGroup));
            }, 1000);
        }
    };
    websocket.onclose = event => {
        alert("连接关闭");
        window.console.log(event);
    };
    websocket.onerror = error => {
        alert("获取房间信息失败，连接出错");
        window.console.log(error);
        websocket.reconnect();
    };

    //处理重连
    websocket.reconnect = function () {
        // Set request interval time to avoid congest
        let reconnectTimeout = 5000;
        let reconnectTimer = setTimeout(function () {
            // Avoid duplicated connection
            if (websocket.readyState === 1) {
                clearTimeout(reconnectTimer);
            }
            // Recreate WebSocket Object and reestablish link
            else if (websocket.readyState === 2 || websocket.readyState === 3) {
                websocket = new WebSocket("ws://" + serverUrl + "/ws/monitor/");
            }
        }, reconnectTimeout)
    };

    //每隔一段时间检查房间的连接情况，太久没有更新状态的，视为离线
    interval = window.setInterval(() => {
        let currentTime = new Date().getTime();
        for (let i = 0; i < roomList.length; i++) {
            if (currentTime - roomList[i].updateTime > 3000) {
                roomList[i].isActive = false;
            }
        }
    }, 4000);
}

//处理接收到的数据
function onMessageReceived(event) {
    webSocketPulse.reset().start();
    let data = JSON.parse(event.data);
    let dataType = data.msgType;
    if (dataType === MESSAGE.MSG_ROOM_STATUS) {
        let roomStatus = data.message;
        if (roomMap.get(roomStatus.roomNumber)) {
            let room = roomMap.get(roomStatus.roomNumber);
            room.isActive = true;
            room.currentTemperature = roomStatus.currentTemperature;
            room.currentSpeed = roomStatus.currentSpeed;
            room.AC.isACActive = roomStatus.AC.isACActive;
            room.AC.targetTemperature = roomStatus.AC.targetTemperature;
            room.AC.targetSpeed = roomStatus.AC.targetSpeed;
            room.AC.requestStatus = roomStatus.AC.requestStatus;
            room.updateTime = new Date().getTime();
        }
    }
    else {
        window.console.log(data.message);
    }
}


// Websocket Pulse instance
let webSocketPulse = {
    pulseTimeout: 30000,
    pulseTimer: null,
    serverPulseTimer: null,
    reset: function () {
        clearTimeout(this.pulseTimer);
        clearTimeout(this.serverPulseTimer);
        return this;
    },
    start: function () {
        this.pulseTimer = setTimeout(function () {
            // Send a pulse to server, and wait for service reply a pulse
            wsSendPulse();
            // No response from server, then reconnect to server
            //this.serverPulseTimer = setTimeout(function () {
            //    websocket.close();
            //}, self.pulseTimeout)
        }, this.pulseTimeout)
    }
};

// 心跳包发送函数
function wsSendPulse() {
    let req = {
        msgType: 304,
        message: "echo",
    };
    let json = JSON.stringify(req);
    websocket.send(json)
}

//清空列表
function clear() {
    roomList = [];
    roomMap = new Map();
}

//Api释放
function releaseAPI() {
    clear();
    if (websocket != null)
        websocket.close();
    window.clearInterval(interval);
}

export default {
    setUpdateMode,
    initialList,
    getRoomList,
    getRoomByNumber,
    updateRoomList,
    releaseAPI
}
