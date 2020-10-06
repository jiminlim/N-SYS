import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../components/Main/MainPage"),
    // component:()=> import('@/components/Main/new')
  },
  {
    path: "/users",
    name: "users",
    component: () =>
      import(/* webpackChunkName: "users" */ "../views/Users.vue"),
  },
  {
    path: "/games",
    name: "games",
    component: () =>
      import(
        /* webpackChunkName: "games" */ "../components/BrainWall/webRTC.vue"
      ),
    // component: () => import(/* webpackChunkName: "games" */ '../views/Games.vue')
  },
  {
    path: "/wall1",
    name: "wall1",
    component: () =>
        import(
             "../components/BrainWall/BrainWall.vue"
            ),
    // component: () => import(/* webpackChunkName: "games" */ '../views/Games.vue')
  },
  {
    path: "/webcam",
    name: "webcam",
    component: () => import("../views/WebCam.vue"),
  },
  {
    path: "/step5",
    name: "step5",
    component: () => import("@/components/Main/step5.vue"),
  },
  {
    path: "/myprofile",
    name: "myprofile",
    component: () =>
      import(/* webpackChunkName: "myprofile" */ "../views/Myprofile.vue"),
  },
  {
    path: "/changenickname",
    name: "changenickname",
    component: () =>
      import(
        /* webpackChunkName: "changenickname" */ "../views/changenickname.vue"
      ),
  },
  {
    path: "/changepw",
    name: "changepw",
    component: () =>
      import(/* webpackChunkName: "changepw" */ "../views/changepw.vue"),
  },
  {
    path: "/changepwbyemailjs",
    name: "changepwbyemailjs",
    component: () =>
      import(
        /* webpackChunkName: "changepwbyemailjs" */ "../views/changepwbyemailjs.vue"
      ),
  },
];

export default new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});
