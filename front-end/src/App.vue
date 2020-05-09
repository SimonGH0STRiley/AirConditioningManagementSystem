<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <Login></Login>
    <Tenant></Tenant>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Login from "./components/Login";
import Tenant from "./components/Tenant";

export default {
  name: 'app',
  components: {
    Login,
    Tenant
  }
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
