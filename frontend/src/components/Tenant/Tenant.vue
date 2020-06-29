<template>
    <b-container>
        <b-row>
            <b-col class="col-lg-8">
                <b-button pill variant="outline-light">
                    <b-iconstack id="ac-power" :variant="buttonStyle">
                        <b-icon stacked icon="circle" ></b-icon>
                        <b-icon stacked icon="power" scale="0.75"></b-icon>
                    </b-iconstack>
                </b-button>
            </b-col>
            <b-col class="col-lg-4">
                <b-row>
                    <div>温度：{{ room.AC.targetTemperature }}      </div>
                </b-row>
                <b-row>
                    <b-button-group>
                        <b-button size="md" class="h2 mb-2" variant="outline-primary" @mousedown="temperatureChangeHandler('-')" @mouseup="clearMouseTimeout">
                            <b-icon icon="arrow-left" aria-hidden="true"></b-icon>
                        </b-button>
                        <b-button size="md" class="h2 mb-2" variant="outline-primary" @mousedown="temperatureChangeHandler('+')" @mouseup="clearMouseTimeout">
                            <b-icon icon="arrow-right" aria-hidden="true"></b-icon>
                        </b-button>
                    </b-button-group>
                </b-row>
                <p></p>
                <b-row>
                    <div>风速：{{ room.AC.targetSpeed }}     </div>
                </b-row>
                <b-row>
                    <b-button-group>
                        <b-button size="md" class="h2 mb-2" variant="outline-primary" @mousedown="speedChangeHandler('-')" @mouseup="clearMouseTimeout">
                            <b-icon icon="arrow-left" aria-hidden="true"></b-icon>
                        </b-button>
                        <b-button size="md" class="h2 mb-2" variant="outline-primary" @mousedown="temperatureChangeHandler('+')" @mouseup="clearMouseTimeout">
                            <b-icon icon="arrow-right" aria-hidden="true"></b-icon>
                        </b-button>
                    </b-button-group>
                </b-row>
            </b-col>
        </b-row>
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
