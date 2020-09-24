import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {

  },
  mutations: {

  },
  actions: {
    login: (context, loginData)=>{
      console.log("store login "+loginData.uid+" "+loginData.upw);
    },
    join: (context, joinData)=>{
      console.log("store join : "+joinData.uid);
      axios
          .post("http://localhost:8080/Userinfo/join", joinData)
          .then(({ data }) => {
            console.log(data);
            console.log(data.Userinfo);
            console.log(data.Userinfo.uid);

          })
          .catch(() => {
            alert("로그인 시 에러가 발생했습니다.");
          });
    }
  },
  modules: {
  }
})
