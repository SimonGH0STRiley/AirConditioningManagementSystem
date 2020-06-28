<template>
    <div id="app">
        <Login></Login>
    </div>
</template>

<script>
    import Login from "./components/Login";
    import roomAPI from "../api/roomAPI";
    import router from "./router/index"

    export default {
        name: 'app',
        components: {
            Login,
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
