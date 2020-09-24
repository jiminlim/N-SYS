import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    SERVER_URL: 'http://localhost:8080', // 차후 aws로 바꿔야함
    poses:['ready','left','stand','right'], // poseList - 디비에 넣을지 고민중
    currentPose: 'ready' // default pose
  },
  mutations: {
    changeCurrentPose(state, payload){ // 현재 포즈를 바꿔줌
      state.currentPose = this.state.poses[payload]
    }
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
  getters:{
    getCurrentPose(state){
      return state.currentPose
    },
  },
  modules: {
  }
})
