import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
import * as tf from '@tensorflow/tfjs';
import * as tmPose from '@teachablemachine/pose';
Vue.config.productionTip = false

export const EventBus = new Vue()

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
