<template>
  <v-container>
    <h1>Games</h1>

    <!-- 게임 모든 리스트  v-for 돌려서 출력 && axios-->
    <game-container></game-container>
    <button @click="getGames">hhhhhhhhhhhhhh</button>
  </v-container>
</template>

<script>
import GameContainer from '@/components/Game/GameContainer'
import axios from 'axios'
export default {
  name: "Games",
  data() {
    return {

    }
  },
  methods : {
    getGames(){
      axios.get('http://localhost:8080/game/list')
          .then((res)=>{
            console.log(res)
          })
          .catch((err)=>{
            console.log(err)
          })
    }
  },
  components : {
    GameContainer,
  },
  actions:{

  }
}
</script>

<style scoped>

</style>