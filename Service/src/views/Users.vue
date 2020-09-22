<template>
  <v-container grid-list-xl>
    <v-layout row wrap>
      <v-flex xs6>
        <AllUsers></AllUsers>
      </v-flex>
      <v-flex xs6>
        <SignUp></SignUp>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import AllUsers from "@/components/Users/AllUsers";
import SignUp from "@/components/Users/SignUp";
import axios from "axios";
import {mapGetters} from "vuex";
export default {
  data() {
    return {
      useremail: "",
      userpwd: "",
      U_id: "",
      U_email: "",
      U_password1: "",
      U_password2: "",
      // avatarImage: require("../../assets/img/person.png"),
      usercomment: "Hi, Nice to meet you.",
      // usertoken: '',
      item: {},
    };
  },
  components: {
    AllUsers,
    SignUp,
  },
  computed: {
    ...mapGetters(["token"]),
  },
  methods: {
    loginHandler() {
      axios
          .post("http://localhost:8080/user/login", {
            email: this.useremail,
            password: this.userpwd,
          })
          .then(({ data }) => {
            this.item = data;
            // alert(this.item);
            // alert(this.item.email);
            let msg = "로그인 정보가 정확하지 않습니다.";
            if (this.item.email != null) {
              msg = "로그인이 완료되었습니다.";
            }
            alert(msg);
            if (this.item.email != null) {
              localStorage.setItem("nowUid", this.item.uid);
              localStorage.setItem("nowEmail", this.useremail);
              // 실제 유저프로필 이미지. avatarImage.
              localStorage.setItem("avatarImage", this.item.avatarImage);
              // 유저프로필 이미지의 저장경로. avatarImageSrc.
              localStorage.setItem("avatarImageSrc", this.item.avatarImageSrc);
              localStorage.setItem("usercomment", this.item.usercomment);
              // alert('토큰 정보'+this.item.token);
              // this.usertoken = this.item.token;
              localStorage.setItem("nowToken", this.item.token);
              alert("토큰 생성이 완료됐습니다.");
              window.location.href = "/main";
            }
          })
          .catch(() => {
            alert("로그인 시 에러가 발생했습니다.");
            window.location.href = "/";
          });
    },
    registerHandler() {
      axios
          .post("http://localhost:8080/user/signUp", {
            uid: this.U_id,
            email: this.U_email,
            password: this.U_password1,
            interest1: "",
            interest2: "",
            interest3: "",
            avatarImage: this.avatarImage,
            imgtype: "image/png",
            usercomment: "Hi, Nice to meet you.",
          })
          .then(({ data }) => {
            this.isok = data;
            // alert(this.isok);
            let msg = "회원가입실패.";
            if (this.isok != null) {
              msg = "회원가입성공.";
            }
            alert(msg);
            if (this.isok != null) {
              window.location.href = "/";
            }
          })
          .catch(() => {
            alert("회원가입 시 에러가 발생했습니다.");
            window.location.href = "/";
          });
    },
  },
};
</script>