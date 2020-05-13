<template>
    <b-col md="6" class="mb-3">
        <b-button pill variant="outline-light">
            <b-iconstack id="ac-power">
                <b-icon stacked icon="circle" variant="danger"></b-icon>
                <b-icon stacked icon="power" variant="danger" scale="0.75"></b-icon>
            </b-iconstack>
        </b-button>
    </b-col>
</template>

<script>
    export default {
        name: "Tenant"
    }
</script>

<style scoped>
    #ac-power {
        width: 300px;
        height: 300px;
    }
</style>
