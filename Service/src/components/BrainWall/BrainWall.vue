<template>
  <div>
    <h1>두뇌의 벽</h1>
    <v-container >

    </v-container>
    <div v-if="gameStartFlag">
      <div>{{countDown}}</div>
      <div v-if="!roundFinishFlag">
        round - {{round}}/5
        <div>score - {{score}}</div>
        <button @click="generateRandomNumber()">포즈 바꾸기 버튼</button>
        <div>현재 포즈 이름 - {{getCurrentPose}}</div>
        <random-pose></random-pose>
      </div>
      <div v-else-if="roundFinishFlag">
      </div>
    </div>
    <button @click="clickStart()" >START</button>
    <v-btn color="green darken-3" @click="clickStart">Login</v-btn>

    <div style="border-style:solid"><canvas id="canvas"></canvas></div>
    <div style="border-style:solid" id="label-container" >
      <h2>good</h2>
      <h2>bad</h2>
    </div>
  </div>
</template>

<script>
import '@tensorflow/tfjs'
import RandomPose from "@/components/BrainWall/RandomPose";
import * as tmPose from "@teachablemachine/pose"
import {mapGetters} from "vuex";

let model, webcam, ctx, labelContainer, maxPredictions;

export default {
  name : 'BrainWall',
  data(){
    return {
      startBtn:true,
      requestId: undefined,
      score:0,
      round:0,
      roundFinishFlag: false,
      scoreFlag:false,
      gameStartFlag:false,
      countDown:10,

    }
  },
  components:{
    RandomPose,
  },
  computed:{
    ...mapGetters(['getCurrentPose'])
  }
,
  methods:{clickStart() {
      // this.startDateTime = new Date();
      // this.$cookies.set('startDateTime', this.startDateTime)
      this.init()
      this.roundFinishFlag=false
      this.gameStartFlag=true
    },
    countDownTimer() {
      if(this.countDown > 0) {
        setTimeout(() => {
          this.countDown -= 1
          this.countDownTimer()
        }, 1000)
      }
    },
    generateRandomNumber(){
    let tempRandomNumber = Math.floor(Math.random()*3+1) // 숫자 바꾸면 됨
      this.changeCurrentPoseM(tempRandomNumber)
      this.round++
      this.countDown=10
      this.countDownTimer()
      if(this.round==5){
        this.roundFinishFlag = true
        this.round = 0
        this.score=0
      }
      this.scoreFlag = false

      console.log(tempRandomNumber)
    },
    changeCurrentPoseM: function(x){
      this.$store.commit("changeCurrentPose",x)
    },
    async init() {
      this.startBtn = false;

      const URL ="https://teachablemachine.withgoogle.com/models/sV2phcmJ-/";
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
      for (let i = 0; i < maxPredictions; i++) { // and class labels
        labelContainer.appendChild(document.createElement("div"));
      }
    },
    async loop() {
    //timestamp
      webcam.update(); // update the webcam frame
      await this.predict(); //this.predict();
      if(this.requestId){
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
        console.log(this.$store.state.currentPose)
        // console.log(prediction[i].className)
        if(this.$store.state.currentPose == prediction[i].className && !this.scoreFlag && prediction[i].probability.toFixed(2)>=0.9){
          if(this.countDown>0){
          this.score++
          this.scoreFlag = true
        }

        }

        const classPrediction =
            prediction[i].className + ": " + prediction[i].probability.toFixed(2);
        labelContainer.childNodes[i].innerHTML = classPrediction;
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

  }
}
</script>