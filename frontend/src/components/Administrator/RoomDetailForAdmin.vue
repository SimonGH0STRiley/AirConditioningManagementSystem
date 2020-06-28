<template>
    <div class="modal fade" id="roomInfo" tabindex="-1" role="dialog" aria-labelledby="roomInfoLabel">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close" aria-hidden="true">
                        <span class="glyphicon glyphicon-remove"></span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-lg-2 col-lg-offset-2 col-md-3 col-xs-3">
                            房间号：#{{ currentRoom.roomNumber }}
                            房间是否入住：{{ currentRoom.isActive }}
                        </div>
                        <div class="col-lg-2 col-lg-offset-1 col-md-2 col-xs-2" style="text-align: center">
                            房间当前温度：{{ currentRoom.currentTemperature }}℃
                        </div>
                        <div class="col-lg-1 col-md-2 col-xs-2">
                            <div :class="{'glyphicon glyphicon-fan' :currentRoom.AC.isACActive}" style="min-width:15px;"></div>
                        </div>
                        <div class="col-lg-2 col-md-5 col-xs-5" style="text-align: right">{{ readyType }}</div>
                    </div>
                    <div class="row" v-if="currentRoom.AC.isACActive">
                        <div class="col-lg-2 col-lg-offset-2 col-md-4 col-xs-6">房间空调设置</div>
                        <div class="col-lg-4 col-lg-offset-2 col-md-4 col-md-offset-4 col-xs-6" style="text-align: right">
                            设置温度：{{ currentRoom.AC.targetTemperature }}
                            设置风速： {{ currentRoom.AC.targetSpeed }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "RoomDetailForAdmin",
        props: ["currentRoom"],
        computed: {
            readyType: function() {
                if(!this.currentRoom.isActive) {
                    return "房间未入住";
                } else {
                    if(this.currentRoom.AC.isACActive) {
                        return "空调使用中";
                    } else {
                        return "空调未使用";
                    }
                }
            }
        }
    };
</script>

<style scoped>
    .modal-body {
        text-align: left;
    }
</style>
