<template>
  <v-container>
    <brain-wall></brain-wall>
    <h1>Games</h1>

    <!-- 게임 모든 리스트  v-for 돌려서 출력 && axios-->
<!--    <game-container v-for="game in gameList" :key="game.gid">-->
    <div v-for="game in gameList" :key="game.gid">
      <game-container :game="game"/>
<!--    {{game.gtitle}}-->

    </div>
    <button @click="getGames">hhhhhhhhhhhhhh</button>
  </v-container>
</template>

<script>
import GameContainer from '@/components/Game/GameContainer'
import BrainWall from "@/components/BrainWall/BrainWall";
import axios from 'axios'


export default {
  name: "Games",
  data() {
    return {
      gameList : [],
    }
  },
  methods : {
    getGames(){
      axios.get(this.$store.state.SERVER_URL+'/game/list')
          .then((res)=>{
            this.gameList = res.data
            console.log(res)
          })
          .catch((err)=>{
            console.log(err)
          })
    }
  },
  components : {
    GameContainer,
    BrainWall,
  },
  actions:{

  }
}
</script>

<style scoped>

</style>