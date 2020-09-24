import Vue from 'vue'
import Vuex from 'vuex'

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
  },
  getters:{
    getCurrentPose(state){
      return state.currentPose
    },
  },
  modules: {
  }
})
