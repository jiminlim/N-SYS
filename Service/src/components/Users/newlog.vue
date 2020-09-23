<template>
  <v-container>
    <v-card class="elevation-12">
      <v-bottom-navigation
          :value="activeBtn"
          color="yellow accent-2"
          horizontal
      >
        <v-btn @click="clicklogin">
          <span>Login</span>
          <v-icon>mdi-heart</v-icon>
        </v-btn>
        <v-btn @click="clickjoin">
          <span>Join</span>
          <v-icon>mdi-heart</v-icon>
        </v-btn>
      </v-bottom-navigation>
      <v-container :class="loginview">
        <v-row justify="center">
        <v-card-text >
          <v-form>
            <v-text-field
                label="Email"
                v-model="email"
                name="email"
                prepend-icon="mdi-account"
                type="text"
                :error-messages="emailErrors"
                @input="$v.email.$touch()"
                @blur="$v.email.$touch()"
                required
            ></v-text-field>
            <v-text-field
                v-model="password"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                :error-messages="passwordErrors"
                @input="$v.password.$touch()"
                @blur="$v.password.$touch()"
                required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="yellow accent-4" @click="submitlogin">Login</v-btn>
        </v-card-actions>
        </v-row>
      </v-container>

      <v-container :class="joinview">
        <v-row justify="center">
        <v-card-text>
          <v-form>
            <v-text-field
                label="Email"
                v-model="email"
                name="email"
                prepend-icon="mdi-account"
                type="text"
                :error-messages="emailErrors"
                @input="$v.email.$touch()"
                @blur="$v.email.$touch()"
                required
            ></v-text-field>
            <v-text-field
                v-model="password"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                :error-messages="passwordErrors"
                @input="$v.password.$touch()"
                @blur="$v.password.$touch()"
                required
            ></v-text-field>
            <v-text-field
                v-model="repeatPassword"
                label="repeatPassword"
                name="repeatPassword"
                prepend-icon="mdi-lock"
                type="password"
                :error-messages="repeatPasswordErrors"
                @input="$v.repeatPassword.$touch()"
                @blur="$v.repeatPassword.$touch()"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="yellow accent-4" @click="submitjoin">Join</v-btn>
        </v-card-actions>
        </v-row>
      </v-container>
    </v-card>
  </v-container>

</template>
<script>
import { mapActions } from 'vuex'
import { required, sameAs, email, minLength } from 'vuelidate/lib/validators'
export default {
  validations: {
    email: { required, email },
    password: { required, minLength: minLength(4)},
    repeatPassword: { sameAsPassword : sameAs('password')}
  },

  data () {
    return {
      activeBtn: 0,
      loginview: "d-flex",
      joinview:"d-none",
      email:'',
      password : '',
      repeatPassword:''
    }
  },
  methods:{
    clicklogin(){
      this.clear();
      this.loginview="d-flex";
      this.joinview="d-none";
    },
    clickjoin(){
      this.clear();
      this.loginview="d-none";
      this.joinview="d-flex";
    },
    ...mapActions(['login']),
    submitlogin(){
      this.$v.$touch()
      if(this.$v.$invalid){
        alert('모든 값을 입력해 주세요!')
      } else
        {
        let loginData = {
          u_email: this.email,
          u_pw: this.password
        }
        console.log(loginData+" "+loginData.u_email);
        this.$store.dispatch('login', loginData);
      }
    },
    ...mapActions(['join']),
    submitjoin() {
      this.$v.$touch()
      if(this.$v.$invalid){
        alert('모든 값을 입력해 주세요!')
      } else
      {
        let joinData = {
          u_email: this.email,
          u_pw: this.password
        }
        console.log(joinData+"  "+joinData.u_email);
        this.$store.dispatch('join', joinData);
      }
    },
    clear() {
      this.$v.$reset()
      this.email = ''
      this.password = ''
      this.repeatPassword= ''
    }

  },
  computed: {
    emailErrors() {
      const errors = []
      if (!this.$v.email.$dirty) return errors
      !this.$v.email.email && errors.push('이메일 형식을 바르게 입력해주세요.')
      !this.$v.email.required && errors.push('이메일을 입력해주세요.')
      return errors
    },
    passwordErrors() {
      const errors = []
      if (!this.$v.password.$dirty) return errors
      !this.$v.password.minLength && errors.push(`비밀번호는 최소 4자 이상 입력해야 합니다.`)
      !this.$v.password.required && errors.push('비밀번호를 입력해주세요.')
      return errors
    },
    repeatPasswordErrors() {
      const errors = []
      if (!this.$v.repeatPassword.$dirty) return errors
      !this.$v.repeatPassword.sameAsPassword && errors.push('비밀번호가 다릅니다')
      return errors
    }
  }

}
</script>
