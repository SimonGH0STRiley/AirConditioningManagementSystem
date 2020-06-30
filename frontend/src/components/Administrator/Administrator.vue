<template>
    <b-container>
        <b-row class="header">
            <b-col lg="3" offset-lg="3">
                开启房间数量: {{ roomActiveNumber }}
            </b-col>
            <b-col lg="3" offset-lg="1">
                空调开启房间数量: {{ ACActiveNumber }}
            </b-col>
        </b-row>
        <b-row v-for="col in 26" :key="col">
            <div v-for="row in 5" :key="row">
                <div @click="getCurrentRoom(col, row)"
                     data-toggle="modal"
                     data-target="#room-detail-for-admin"
                     v-b-modal.room-detail-for-admin>
                    <Room :room="roomList[(col - 1) * 5 + (row - 1)]"></Room>
                </div>
            </div>
        </b-row>
        <room-detail-for-admin :currentRoom="currentRoom" v-if="currentRoom"></room-detail-for-admin>
    </b-container>
</template>

<script>
    import Room from "../Room/Room";
    import RoomDetailForAdmin from "./RoomDetailForAdmin";
    import roomAPI from "../../../api/roomAPI";

    export default {
        name: "Administrator",
        components: {
            Room,
            RoomDetailForAdmin
        },
        props:["roomList"],
        data() {
            return {
                currentRoom: null
            }
        },
        computed: {
            roomActiveNumber: function() {
                let count = 0;
                this.roomList.forEach(room => {
                    count = room.isActive ? count + 1 : count;
                });
                return count;
            },
            ACActiveNumber: function() {
                let count = 0;
                this.roomList.forEach(room => {
                    count = (room.isActive && room.AC.isACActive) ? count + 1 : count;
                });
                return count;
            }
        },
        methods: {
            getCurrentRoom: function(col, row) {
                this.currentRoom = this.roomList[(col - 1) * 5 + (row - 1)];
                console.log(this.currentRoom);
                return(this.currentRoom);
            }
        }
    }
</script>

<style scoped>

</style>
