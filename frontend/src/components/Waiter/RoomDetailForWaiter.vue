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
                    </div>
                    <b-button @click="printACBill(currentRoom.roomNumber)">打印房间详单</b-button>
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
                    return "房间已入住";
                }
            }
        },
        methods: {
            printACBill: function (roomNumber) {
                //TODO : 填写打印详单API
            }
        }
    };
</script>

<style scoped>
    .modal-body {
        text-align: left;
    }
</style>
