import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../components/Main/MainPage"),
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
      import(/* webpackChunkName: "games" */ "../views/Games.vue"),
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
