<template>
    <div id="app">
        <Administrator :roomList="roomList"></Administrator>
    </div>
</template>

<script>
    import Login from "./components/Login";
    import Administrator from "./components/Administrator/Administrator";
    import Manager from "./components/Manager/Manager";
    import Tenant from "./components/Tenant/Tenant";
    import Waiter from "./components/Waiter/Waiter";
    // import roomAPI from "../api/roomAPI";
    import router from "./router/index"

    export default {
        name: 'app',
        components: {
            // eslint-disable-next-line vue/no-unused-components
            Login, Administrator, Manager, Tenant, Waiter
        },
        data() {
            const RoomCapacity = 128;
            let roomList = [];
            for (let i = 0; i < RoomCapacity; i++) {
                let room = {
                    roomNumber: i,
                    isActive: Math.random() > 0.5,
                    currentTemperature: Math.floor(18 + Math.random() * (30 - 18)),
                    currentSpeed: Math.floor(Math.random() * 3),
                    AC: {
                        isACActive: Math.random() > 0.5,
                        targetTemperature: Math.floor(18 + Math.random() * (30 - 18)),
                        targetSpeed: Math.floor(Math.random() * 3),
                        requestStatus: ['ready', 'pending', 'resolved', 'rejected'][Math.floor(Math.random() * 4)]
                    },
                    updateTime: null, //该设备更新的时间戳
                };
                roomList.push(room);
            }
            return {
                roomList: roomList
            };
        },
        // created() {
        //     roomAPI.updateRoomList();
        // },
        // beforeDestroy() {
        //     roomAPI.releaseAPI();
        // },
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }
</style>
