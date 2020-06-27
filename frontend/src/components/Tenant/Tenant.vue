<template>
    <b-container>
        <b-col md="6" class="mb-3">
            <b-button pill variant="outline-light">
                <b-iconstack id="ac-power" :variant="buttonStyle">
                    <b-icon stacked icon="circle" ></b-icon>
                    <b-icon stacked icon="power" scale="0.75"></b-icon>
                </b-iconstack>
            </b-button>
        </b-col>
        <b-col md="6">
            <p>温度：{{ room.AC.targetTemperature }}</p>
            <p>
                <button type="button" class="btn btn-default" @mousedown="temperatureChangeHandler('-')" @mouseup="clearMouseTimeout">
                    <span class="glyphicon glyphicon-chevron-left"></span>
                </button>
                <button type="button" class="btn btn-default" @mousedown="temperatureChangeHandler('+')" @mouseup="clearMouseTimeout">
                    <span class="glyphicon glyphicon-chevron-right"></span>
                </button>
            </p>
            <p></p>
            <p>风俗：{{ room.AC.targetSpeed }}</p>
            <p>
                <button type="button" class="btn btn-default" @mousedown="speedChangeHandler('-')" @mouseup="clearMouseTimeout">
                    <span class="glyphicon glyphicon-chevron-left"></span>
                </button>
                <button type="button" class="btn btn-default" @mousedown="speedChangeHandler('+')" @mouseup="clearMouseTimeout">
                    <span class="glyphicon glyphicon-chevron-right"></span>
                </button>
            </p>
        </b-col>
    </b-container>
</template>

<script>
    export default {
        name: "Tenant",
        props: ["room"],
        computed: {
            buttonStyle: function() {
                if (this.room.AC.requestStatus === "ready") {
                    return "primary";
                } else if (this.room.AC.requestStatus === "pending") {
                    return "warning";
                } else if (this.room.AC.requestStatus === "resolved") {
                    return "success";
                } else if (this.room.AC.requestStatus === "rejected") {
                    return "danger";
                } else {
                    return "dark"
                }
            }
        },
        methods: {
            temperatureChangeHandler: function (currentOperation) {
                let that = this;
                let flag = 0;
                clearTimeout(this.pressTimeout);
                clearTimeout(this.pressTimer);
                this.pressTimeout = setTimeout(function () {
                    that.pressTimer = setInterval(function () {
                        // TODO: 调整温度接口
                        that.$emit('temperatureChange', currentOperation);
                        flag++;
                    }, 100);
                }, 1000);
                if (flag === 0) {
                    this.$emit('temperatureChange', currentOperation);
                }
            },
            speedChangeHandler: function (currentOperation) {
                let that = this;
                let flag = 0;
                clearTimeout(this.pressTimeout);
                clearTimeout(this.pressTimer);
                this.pressTimeout = setTimeout(function () {
                    that.pressTimer = setInterval(function () {
                        // TODO: 调整风速接口
                        that.$emit('speedChange', currentOperation);
                        flag++;
                    }, 100);
                }, 1000);
                if (flag === 0) {
                    this.$emit('speedChange', currentOperation);
                }
            },
            clearMouseTimeout: function () {
                clearTimeout(this.pressTimeout);
                clearTimeout(this.pressTimer);
            },
        }
    }
</script>

<style scoped>
    #ac-power {
        width: 300px;
        height: 300px;
    }
</style>
