import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {

  },
  mutations: {

  },
  actions: {
    login: (loginData)=>{
      console.log("store login "+loginData.u_email+" "+loginData.u_pw);
    },
    join: (joinData)=>{
      console.log("store join"+joinData.u_email);
    }
  },
  modules: {
  }
})
