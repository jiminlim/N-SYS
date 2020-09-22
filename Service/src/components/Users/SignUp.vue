<template>
  <div>
    <h1>MyPage</h1>
    <v-text-field
        label="userID123"
        v-model="userId"
    ></v-text-field>
    <v-btn @click="signUp">회원정보수정</v-btn>
    <h1>History</h1>
  </div>
</template>

<script>
import { EventBus } from '@/main.js'
import { mapActions } from 'vuex'
//import {mapMutations }from 'vuex'

  export default {
    data() {
      return {
        userId: null,
        password: null,
        name: null,
        address: null,
        src: null
      }
    },
    methods: {
      
      //...mapMutations(['addUsers']), //mapmutation s
      ...mapActions(['addUsers']) , //mapActions
      signUp() {
        console.log('here')
        let userObj = {
          userId: this.userId,
          password: this.password,
          name: this.name,
          address: this.address,
          src: this.src
        }
        // this.$store.commit('addUsers', userObj) //mutation 불러옴
        //this.addUsers(userObj) //mapmutation 
        // this.$store.dispatch('addUsers', userObj) //action 불러옴

        this.addUsers(userObj) //mapactions
        this.clearForm()
      },
      clearForm() {
        this.userId = null,
        this.password = null,
        this.name = null,
        this.address = null,
        this.src = null
      }
    }
  }
</script>