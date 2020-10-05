import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import emailjs from "emailjs-com";
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    SERVER_URL: 'http://localhost:8080', // 차후 aws로 바꿔야함
    poses:['ready','left','stand','right'], // poseList - 디비에 넣을지 고민중
    currentPose: 'ready', // default pose,
    bar : "내가 승리한 것이지 인간이 승리한 것이 아니야"
  },
  mutations: {
    changeCurrentPose(state, payload){ // 현재 포즈를 바꿔줌
      state.currentPose = this.state.poses[payload]
    },
    changebar(state, payload){
      console.log("payload "+payload);
      state.bar = payload;
    }
  },
  actions: {
    login: (context, loginData) => {
      console.log("store login " + loginData.uid + " " + loginData.upw);
      axios
        .post("http://localhost:8080/Userinfo/login", loginData)
        .then(({ data }) => {
          if (data != null) {
            alert("로그인 성공");
            localStorage.setItem("NowID", loginData.uid);
          }
        })
        .catch(() => {
          alert("로그인 시 에러가 발생했습니다.");
        });
    },
    join: (context, joinData) => {
      console.log("store join : " + joinData.uid);
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
    },
    findpw: (context, findpwData) => {
      console.log("store findpw [email] : " + findpwData.target_email);
      // axios를 통해서 백엔드와 통신. [사용자가 입력한 이메일을 인자로 넘기고, 그걸 받은 백엔드에서 DB와 비교. 가입된 이메일인지 체크.]
      // 가입된 이메일이라면 true, 아니라면 false 값 반환. 숫자 0 또는 1로 반환해도 가능.

      // 반환된 값을 기준으로 가입된 이메일이라면 비밀번호찾는 이메일을 입력된 이메일에 보내고,
      // 가입된 이메일이 아니라면 가입한 이메일을 입력하라는 경고창 팝업.

      emailjs
        .send(
          "service_AI",
          "template_r1n19h8",
          findpwData,
          "user_5j1guKc2v1FQ1OJzyA1rf"
        )
        .then(
          function(response) {
            console.log("SUCCESS!", response.status, response.text);
          },
          function(err) {
            console.log("FAILED...", err);
          }
        );

      axios
        .post("http://localhost:8080/mmlmlml", {
          email: findpwData.target_email,
        })
        .then(({ data }) => {
          this.item = data;
          let msg = "가입된 이메일이 아닙니다.";
          if (this.item.email != null) {
            msg = "입력하신 이메일로 접속해 Code를 확인해주세요.";
          }
          // alert(this.item.email);
          // alert(this.item);
          alert(msg);
          let ranNum = "" + Math.floor(Math.random() * 1000);
          if (this.item.email != null) {
            localStorage.setItem("email", this.item.email);
            this.findpwData.message_html += ranNum;
            localStorage.setItem("code", ranNum);
            emailjs
              .send("service_AI", "template_r1n19h8", this.findpwData)
              .then(
                function(response) {
                  console.log("SUCCESS!", response.status, response.text);
                },
                function(err) {
                  console.log("FAILED...", err);
                }
              );
            alert("메일전송");
            this.$router.push("/");

            var myWindow = window.open("", "_self");
            myWindow.document.write("");
            setTimeout(function() {
              myWindow.close();
            }, 1000);
          }
        })
        .catch(() => {
          alert("진행 중 에러가 발생했습니다.");
          window.location.href = "/";
        });
    },
  },
  getters:{
    getCurrentPose(state){
      return state.currentPose
    },
    getBar(state){
      return state.bar
    }
  },
  modules: {
  }
});
