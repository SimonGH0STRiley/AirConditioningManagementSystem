import Vue from 'vue';
import Router from 'vue-router';
import Login from "../components/Login";
import Administrator from "../components/Administrator/Administrator";
import Manager from "../components/Manager/Manager";
import Tenant from "../components/Tenant/Tenant";
import Waiter from "../components/Waiter/Waiter";

Vue.use(Router);

const router = new Router({
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login',
            name: 'login',
            component: Login
        },
        {
            path: '/admin',
            name: 'admin',
            component: Administrator
        },
        {
            path: '/manager',
            name: 'manager',
            component: Manager
        },
        {
            path: '/tenant',
            name: 'tenant',
            component: Tenant
        },
        {
            path: '/waiter',
            name: 'waiter',
            component: Waiter
        }
    ]
});

// 导航守卫
// 使用 router.beforeEach 注册一个全局前置守卫，判断用户是否登陆
router.beforeEach((to, from, next) => {
    if (to.path === '/login') {
        next();
    } else {
        let token = localStorage.getItem('Authorization');

        if (token === 'null' || token === '') {
            next('/login');
        } else {
            next();
        }
    }
});

export default router;
