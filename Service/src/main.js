import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import store from './store/index'
import vuetify from './plugins/vuetify'
import Vuelidate from 'vuelidate'

//socket 설정
import io from 'socket.io-client';
const socket = io('https://j3b201.p.ssafy.io:3001');
Vue.prototype.$socket= socket;
console.log('socket'+socket);

Vue.config.productionTip = false
Vue.use(Vuelidate)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
