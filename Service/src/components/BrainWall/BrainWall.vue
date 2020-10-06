<template>
  <div>
    <h1 align="center">두뇌의 벽</h1>
    <!--    <button @click="clickStart()">START</button>-->
    <v-card-actions class="justify-center">
      <v-btn
          :disabled="gameStartFlag"
          @click="clickStart()"
          color="light-green lighten-1"
          elevation="2"
          tile
          x-large
      >START</v-btn>
    </v-card-actions>


    <div v-if="gameStartFlag">
      <div v-if="!roundFinishFlag">
        <h1 align="center">카운트 다운</h1>
        <h1 align="center" color="red" >{{ countDown }}</h1>
        <h2 align="center">round - {{ round }}/5</h2>
        <h2 align="center">score - {{ score }}</h2>
        <h1 align="center" id="label-container"></h1>

        <v-card-actions class="justify-center">
          <v-btn
              :disabled="countFlag" @click="generateRandomNumber()"
              color="light-green lighten-1"
              elevation="2"
              tile
              x-large
          >포즈 바꾸기 버튼</v-btn>
        </v-card-actions>
        <!--        <button :disabled="countFlag" @click="generateRandomNumber()">-->
        <!--          포즈 바꾸기 버튼-->
        <!--        </button>-->
        <!--        <div>현재 포즈 이름 - {{ getCurrentPose }}</div>-->
        <div>
          <random-pose class="temp"></random-pose>
          <div class="temp"><canvas id="canvas"></canvas></div>
        </div>
      </div>

      <!--    <v-btn color="green darken-3" @click="clickStart">Login</v-btn>-->


      <!--      <h2>good</h2>-->
      <!--      <h2>bad</h2>-->
    </div>
  </div>
</template>

<script>
import "@tensorflow/tfjs";
import RandomPose from "@/components/BrainWall/RandomPose";
import * as tmPose from "@teachablemachine/pose";
import { mapGetters } from "vuex";

let model, webcam, ctx, labelContainer, maxPredictions;

export default {
  name: "BrainWall",
  data() {
    return {
      startBtn: true,
      requestId: undefined,
      score: 0,
      round: 0,
      roundFinishFlag: false,
      scoreFlag: false,
      gameStartFlag: false,
      countDown: 5,
      countFlag: false, //카운트 다운 버튼 비활성화
    };
  },
  components: {
    RandomPose,
  },
  computed: {
    ...mapGetters(["getCurrentPose"]),
  },
  methods: {
    clickStart() {
      // this.startDateTime = new Date();
      // this.$cookies.set('startDateTime', this.startDateTime)
      this.init();
      this.roundFinishFlag = false
      this.gameStartFlag = true
    },
    countDownTimer() {
      if (this.countDown > 0) {
        setTimeout(() => {
          this.countDown -= 1
          this.countDownTimer()
        }, 1000)
      } else if (this.countDown == 0) {
        this.countFlag = false
        if (this.round == 5) {
          alert("게임이 종료되었습니다.");
          this.gameStartFlag=false
          this.roundFinishFlag = true
          this.round = 0
          this.score = 0
        }
      }
    },
    generateRandomNumber() {
      let tempRandomNumber = Math.floor(Math.random() * 9 + 1); // 숫자 바꾸면 됨
      this.changeCurrentPoseM(tempRandomNumber);
      this.round++;
      this.countDown = 5;
      this.countFlag = true;
      this.countDownTimer();
      // if(this.round==5){
      //   this.roundFinishFlag = true
      //   this.round = 0
      //   this.score=0
      // }
      this.scoreFlag = false;

      console.log(tempRandomNumber);
    },
    changeCurrentPoseM: function(x) {
      this.$store.commit("changeCurrentPose", x);
    },
    async init() {
      this.startBtn = false;

      // const URL = "https://teachablemachine.withgoogle.com/models/sV2phcmJ-/";
      const URL = "https://teachablemachine.withgoogle.com/models/1tX6vs5hQ/";
      const modelURL = URL + "model.json";
      const metadataURL = URL + "metadata.json";

      // load the model and metadata
      // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
      // Note: the pose library adds a tmPose object to your window (window.tmPose)
      model = await tmPose.load(modelURL, metadataURL);
      maxPredictions = model.getTotalClasses();

      // Convenience function to setup a webcam
      const size = 400;
      const flip = true; // whether to flip the webcam
      webcam = new tmPose.Webcam(size, size, flip); // width, height, flip
      await webcam.setup(); // request access to the webcam
      await webcam.play();
      this.requestId = window.requestAnimationFrame(this.loop);

      // append/get elements to the DOM
      const canvas = document.getElementById("canvas");

      canvas.width = size;
      canvas.height = size;

      ctx = canvas.getContext("2d");
      labelContainer = document.getElementById("label-container");
      for (let i = 0; i < maxPredictions; i++) {
        // and class labels
        labelContainer.appendChild(document.createElement("div"));
      }
    },
    async loop() {
      //timestamp
      webcam.update(); // update the webcam frame
      await this.predict(); //this.predict();
      if (this.requestId) {
        // console.log(this.requestId);
        window.requestAnimationFrame(this.loop);
      }
    },
    async predict() {
      // Prediction #1: run input through posenet
      // estimatePose can take in an image, video or canvas html element
      const { pose, posenetOutput } = await model.estimatePose(webcam.canvas);
      // Prediction 2: run input through teachable machine classification model
      const prediction = await model.predict(posenetOutput);
      // if(prediction[0].probability.toFixed(2)>0.90){
      //   if(status=="squat"){
      //     count++
      //     cnt(count)
      //   }
      //   status = "stand"
      // } else if(prediction[1].probability.toFixed(2)==1.00){
      //   status = "squat"
      // } else if(prediction[2].probability.toFixed(2)>=0.9){
      //   if(status =="squat"|| status=="stand "){
      //     fail()
      //   }
      //   status = "bent"
      // }

      for (let i = 0; i < maxPredictions; i++) {
        console.log(this.$store.state.currentPose);
        // console.log(prediction[i].className)

        if (this.$store.state.currentPose == prediction[i].className) {
          // labelContainer.childNodes[0].innerHTML = prediction[i].className + ": " + prediction[i].probability.toFixed(2);
          labelContainer.childNodes[0].innerHTML = "정확도: " + prediction[i].probability.toFixed(2);
        }

        if (
            this.$store.state.currentPose == prediction[i].className &&
            !this.scoreFlag &&
            prediction[i].probability.toFixed(2) >= 0.9
        ) {
          if (this.countDown > 0) {
            this.score++;
            this.scoreFlag = true;
          }
        }

        // const classPrediction =
        //     prediction[i].className + ": " + prediction[i].probability.toFixed(2);
        // labelContainer.childNodes[i].innerHTML = classPrediction;
      }

      // finally draw the poses
      this.drawPose(pose);
    },
    drawPose(pose) {
      if (webcam.canvas) {
        // console.log("drawPose method");
        ctx.drawImage(webcam.canvas, 0, 0);
        // draw the keypoints and skeleton
        if (pose) {
          const minPartConfidence = 0.5;
          tmPose.drawKeypoints(pose.keypoints, minPartConfidence, ctx);
          tmPose.drawSkeleton(pose.keypoints, minPartConfidence, ctx);
        }
      }
    },
  },
};
</script>
<style>

.temp{
  float: left;
  width:50%;
}

</style>
