<template>
    <div id="app">
        <Login></Login>
        <Tenant></Tenant>
    </div>
</template>

<script>
    import Login from "./components/Login";
    import Tenant from "./components/Tenant/Tenant";
    import Administrator from "./components/Administrator/Administrator";
    import Manager from "./components/Manager/Manager";
    import roomAPI from "../api/roomAPI";

    export default {
        name: 'app',
        components: {
            Login,
            Tenant
        },
        data() {
            let rooms = roomAPI.getRoomList();
            return {
                roomList: rooms
            };
        },
        created() {
            roomAPI.updateRoomList();
        },
        beforeDestroy() {
            roomAPI.releaseAPI();
        },
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
