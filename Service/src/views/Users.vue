<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <userLoginAJoin></userLoginAJoin>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import userLoginAJoin from "@/components/Users/newlog";
import axios from "axios";
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      useremail: "",
      userpwd: "",
      U_nickname: "",
      U_email: "",
      U_password1: "",
      U_password2: "",
      item1: {},
      item2: {},
    };
  },
  components: {
    userLoginAJoin,
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
          this.item1 = data;
          let msg = "로그인 정보가 정확하지 않습니다.";
          if (this.item1.email != null) {
            msg = "로그인이 완료되었습니다.";
          }
          alert(msg);
          if (this.item1.email != null) {
            localStorage.setItem("nowNickName", this.item1.uid);
            localStorage.setItem("nowEmail", this.useremail);
            window.location.href = "/";
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
          nickname: this.U_nickname,
          email: this.U_email,
          password1: this.U_password1,
          password2: this.U_password2,
        })
        .then(({ data }) => {
          this.item2 = data;
          let msg = "회원가입실패.";
          if (this.item2 != null) {
            msg = "회원가입성공.";
          }
          alert(msg);
          if (this.item2 != null) {
            window.location.href = "/users";
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