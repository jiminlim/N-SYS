<template>
  <div v-bind:style="{ width: `100%`, height: `300px` }">
    <div class="left" v-bind:style="{ width: `50%`, float: `left` }">
      <SnakeGame />
    </div>
    <div class="right" v-bind:style="{ width: `50%`, float: `right` }">
      <SnakeGameAI />
    </div>
  </div>
</template>

<script>
import SnakeGame from "./SnakeGame";
import SnakeGameAI from "./SnakeGameAI";

export default {
  name: "Snake",
  data() {
    return {
      arr: [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
      ],
    };
  },
  methods: {
    ForTest() {
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 5; j++) {
          if (this.arr[i][j] == 9) {
            break;
          }
          console.log(this.arr[i][j]);
        }
      }
    },
  },
  components: {
    SnakeGame,
    SnakeGameAI,
  },
  created() {
    // this.ForTest();
  },
};
</script>
