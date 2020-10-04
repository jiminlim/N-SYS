import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../components/Main/MainPage')
    // component:()=> import('@/components/Main/new')
  },
  {
    path: '/users',
    name: 'users',
    component: () => import(/* webpackChunkName: "users" */ '../views/Users.vue')
  },
  {
    path: '/games',
    name: 'games',
    component: () => import(/* webpackChunkName: "games" */ '../views/Games.vue')
  },
  {
    path: '/webcam',
    name:'webcam',
    component : ()=>import('../views/WebCam.vue')
  },
  {
    path:'/step5',
    name:'step5',
    component : ()=>import('@/components/Main/step5.vue')
  }
]

export default new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

