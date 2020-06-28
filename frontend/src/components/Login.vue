<template>
    <div class="container">
        <div class="col-lg-6 offset-lg-3">
            <div class="row">
                <b-input-group>
                    <b-form-input placeholder="请输入用户名" required autofocus v-model="loginForm.username"></b-form-input>
                    <b-input-group-append>
                        <b-button variant="outline-warning" @click="clearUsername">清除</b-button>
                    </b-input-group-append>
                </b-input-group>
            </div>
            <p></p>
            <div class="row">
                <b-input-group>
                    <b-form-input type="password" placeholder="请输入密码" required v-model="loginForm.password"></b-form-input>
<!--                    <b-input-group-append>
                        <b-button variant="outline-info">查看</b-button>
                    </b-input-group-append>-->
                </b-input-group>
            </div>
            <p></p>
<!--            <div class="row">
                <b-checkbox class=" mb-3" value="remember-me">Remember me</b-checkbox>
            </div>-->
            <div class="row">
                <b-button variant="outline-primary" class="col-lg-2 offset-lg-5" @click="login">登陆</b-button>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Login",
        data() {
            return {
                loginForm: {
                    username: '',
                    password: ''
                }
            }
        },
        methods: {
            login () {
                let that = this;
                if (this.loginForm.username === '' || this.loginForm.password === '') {
                    alert('账号或密码不能为空');
                } else {
                    this.axios({
                        method: 'post',
                        url: '/user/login',
                        data: that.loginForm
                    }).then(res => {
                        console.log(res.data);
                        that.userToken = 'Bearer ' + res.data.data.body.token;
                        // 将用户token保存到vuex中
                        that.changeLogin({Authorization: that.userToken});
                        that.$router.push('/home');
                        alert('登陆成功');
                    }).catch(error => {
                        alert('账号或密码错误');
                        console.log(error);
                    });
                }
            },
            clearUsername () {
                this.LoginForm.username = '';
            }
        }
    }
</script>

<style scoped>

</style>
