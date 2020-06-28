<template>
    <div class="room-info" v-bind:class="{'inactive': room.isActive===false}">
        <div style="min-width: 25px">{{ room.roomNumber }}</div>
        <div>{{ room.currentTemperature }}℃</div>
        <div :class="{'glyphicon glyphicon-fan':(room.isActive && room.AC.isACActive)}"
             style="min-width: 15px"></div>
        <div>{{ readyType }}</div>

    </div>
</template>

<script>
    export default {
        name: "Room",
        props: ["room"],
        computed: {
            readyType: function() {
                if(!this.room.isActive) {
                    return "房间未入住";
                } else {
                    if(this.room.AC.isACActive) {
                        return "空调使用中";
                    } else {
                        return "空调未使用";
                    }
                }
            }
        }
    }
</script>

<style scoped>
    .room-info {
        padding: 5px 15px;
        border-bottom: 1px solid #a3a3a3;
        margin: 15px;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-between;
    }
    .inactive{
        color: darkred;
    }
</style>
