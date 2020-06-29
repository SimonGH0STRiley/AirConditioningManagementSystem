<template>
    <b-container>
        <b-row class="header">
            <div>开启房间数量: {{ roomActiveNumber }}</div>
            <div>剩余房间数量: {{ 128 - roomActiveNumber}}</div>
        </b-row>
        <b-row v-for="col in 8" :key="col">
            <div v-for="row in 16" :key="row">
                <div @click="getCurrentRoom(col, row)"
                     data-toggle="modal"
                     data-target="#roomInfo">
                    <Room :room="roomList[(col - 1) * 16 + (row - 1)]"></Room>
                </div>
            </div>
        </b-row>

    </b-container>
</template>

<script>
    import Room from "../Room/Room";
    import roomAPI from "../../../api/roomAPI";

    export default {
        name: "Waiter",
        components: {
            Room
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
                    count = room.isACActive ? count + 1 : count;
                });
                return count;
            }
        },
        methods: {
            getCurrentRoom: function(col, row) {
                this.currentRoom = this.roomList[(col - 1) * 16 + (row - 1)];
                console.log(this.currentRoom);
                return(this.currentRoom);
            }
        }
    }
</script>

<style scoped>

</style>
