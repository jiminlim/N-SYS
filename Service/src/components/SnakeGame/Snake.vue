<template>
  <div>
    <div class="aaaacenter">
      <div class="robottext">{{ robotstext }}</div>
      <div class="robot">
        <img
          src="../../assets/images/robot1.png"
          class="robotimg"
          v-if="face == 1"
        />
        <img
          src="../../assets/images/robot2.png"
          class="robotimg"
          v-if="face == 2"
        />
        <img
          src="../../assets/images/robot3.png"
          class="robotimg"
          v-if="face == 3"
        />
      </div>
    </div>
    <div class="aaaacenter">
      <h2 :class="{ deadline: time <= 10 }">남은 시간 : {{ time }}</h2>
    </div>
    <div
      class="aaaacenter"
      v-bind:style="{ width: `50%`, float: `left`, align: `center` }"
    >
      <SnakeGame ref="snakeuser" />
    </div>
    <div
      class="aaaacenter"
      v-bind:style="{ width: `50%`, float: `right`, textalign: `center` }"
    >
      <SnakeGameAI ref="snakeai" />
    </div>

    <div class="aaaacenter">
      <button
        type="button"
        class="snakebutton"
        v-on:click="SnakeStart()"
        v-if="!this.GameStarted"
      >
        시작하기
      </button>
      <button
        v-if="this.GameHasEnded"
        v-on:click="Refresh()"
        type="button"
        class="refreshbutton"
      >
        다시하기
      </button>
    </div>
  </div>
</template>

<style>
div.aaaacenter {
  text-align: center;
}

div.robot {
  width: 15%;
  margin-right: 10%;
  margin-top: 10px;
  margin-bottom: 10px;
  height: 100px;
  float: right;
}

div.robottext {
  margin-left: 10%;
  margin-top: 10px;
  margin-bottom: 10px;
  width: 65%;
  height: 100px;
  line-height: 100px;
  float: left;
  font-size: 20px;

  border: 2px solid white;
}

.deadline {
  color: red;
}

.robotimg {
  height: 90px;
}

button.snakebutton {
  background-color: #8edb62;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  border-radius: 12px;
}
button.refreshbutton {
  background-color: rgb(136, 76, 216);
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  border-radius: 12px;
}
</style>
<script>
// import img1 from
import SnakeGame from "./SnakeGame";
import SnakeGameAI from "./SnakeGameAI";
import axios from "axios";
import EventBus from "./EventBus";

export default {
  name: "Snake",
  data() {
    return {
      face: 1,
      robotstext: "30초 내로 더 많은 점수를 얻은 쪽이 승리!",
      time: 30,
      Uname: null,
      GameStarted: false,
      GameHasEnded: false,
      HumanScore: 0,
      AIScore: 0,
      deadline: {
        color: "red",
      },
    };
  },
  methods: {
    SnakeStart() {
      this.GameStarted = true;
      this.$refs.snakeuser.SnakeStart();
      this.$refs.snakeai.SnakeStart();
      this.SetTimer();
    },
    SubmitGameData() {
      if (this.uiPk != undefined) {
        axios
          .post("https://j3b201.p.ssafy.io:8443/Play/snake/", {
            gaId: 1,
            plLevel: 5,
            plscore: this.score,
            uiPk: this.uiPk,
          })
          .then((res) => {
            alert(`${res.data.rank}위에 랭크인 하셨습니다. 축하드립니다.`);
            //   console.log(res);
          });
      }
      // .catch((e) => {
      //   alert("랭킹 진입에 실패하였습니다.");
      //   //   console.error(err);
      // });
    },
    SetTimer() {
      setTimeout(() => {
        if (this.time <= 0) {
          this.EndGame();
          return;
        }
        this.time -= 1;
        this.SetTimer();
      }, 1000);
    },
    EndGame() {
      //   console.log("경기끝");
      this.$refs.snakeuser.SnakeStop();
      this.$refs.snakeai.SnakeStop();
      //   console.log(this.HumanScore, this.AIScore);
      if (this.HumanScore > this.AIScore) {
        this.robotstext = "AI의 패배. 인간의 승리.";
        this.SubmitGameData();
        this.face = 3;
      } else {
        this.face = 2;
        this.robotstext = "인간의 패배. 다음 기회에..";
      }
      this.GameHasEnded = true;
    },
    Refresh() {
      this.$router.go(0);
    },
  },
  components: {
    SnakeGame,
    SnakeGameAI,
  },
  created() {
    this.uiPk = localStorage.getItem("Now_Upk");
    console.log(this.uiPk);
    // console.log("pk test");
    EventBus.$on("human-completed", (payload) => {
      this.HumanScore = payload[0];
    });
    EventBus.$on("ai-completed", (payload) => {
      this.AIScore = payload[0];
    });
  },
};
</script>
