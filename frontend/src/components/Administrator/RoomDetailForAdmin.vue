<template>
    <div class="modal fade" id="roomInfo" tabindex="-1" role="dialog" aria-labelledby="roomInfoLabel">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <b-button type="button" class="close" data-dismiss="modal" aria-label="Close" aria-hidden="true">
                        <b-icon icon="x-square" aria-hidden="true"></b-icon>
                    </b-button>
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
                            房客设置温度：{{ currentRoom.AC.targetTemperature }}
                            房客设置风速： {{ currentRoom.AC.targetSpeed }}
                        </div>
                    </div>
                    <b-form-checkbox v-model="ACPower" name="check-button" switch @click="switchACPower">
                        空调开关
                    </b-form-checkbox>
                    <div>
                        <label>温度设置滑槽</label>
                        <b-form-input id="temperature-slider" v-model="targetTemperature" type="range" min="18" max="30" step="1"
                                      @change="setACIndex('temperature', targetTemperature)"></b-form-input>
                        <div class="mt-2">温度: {{ targetTemperature }}</div>
                    </div>
                    <div>
                        <label>风速设置滑槽</label>
                        <b-form-input id="speed-slider" v-model="targetSpeed" type="range" min="0" max="2" step="1"
                                      @change="setACIndex('speed', targetSpeed)"></b-form-input>
                        <div class="mt-2">风速: {{ targetSpeed }}</div>
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
        data() {
            return {
                ACPower: null,
                targetTemperature: 18,
                targetSpeed: 0
            }
        },
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
        },
        methods: {
            switchACPower () {
                this.ACPower = !this.ACPower;
                // TODO
            },
            setACIndex (mode, targetValue) {
                if (mode === 'temperature') {
                    //TODO
                    this.targetTemperature = targetValue;
                } else if (mode === 'speed') {
                    //todo
                    this.targetSpeed = targetValue;
                } else {
                    alert('wrong mode!')
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
