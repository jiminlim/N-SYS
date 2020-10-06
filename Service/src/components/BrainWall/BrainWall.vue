<template>
  <div style="display: block; position: relative; margin: 10px; margin-top: 2%">
    <v-card class="item" style="float: left ;
     margin-left: 5%;  width: 40%; ">
      <div>
        <v-card style="height: 250px; margin-top: 20px; margin-left:10%; margin-right: 10% ">
          <!--          <v-img src="@/assets/images/insertcoin.png" >-->
          <div v-if="gameStartFlag" style="text-align: center; margin: 5%">
            <div v-if="!roundFinishFlag">
              <div><h1>{{ countDown }}</h1></div>
              <div><h2> round : {{ round }}/5</h2></div>
              <div><h2> score : {{ score }} </h2></div>
              <div style="font-size: 30px" id="label-container"></div>
              <v-btn :disabled="countFlag" color="green darken-3" @click="generateRandomNumber">
                포즈 바꾸기
              </v-btn>
            </div>
          </div>
          <div v-if="!gameStartFlag" style=" text-align: center; align-content: center">
            <v-btn color="green darken-3" @click="clickStart" style="margin-top: 20%">START</v-btn>
          </div>
          <!--          </v-img>-->
        </v-card>
        <div style="height: 370px;  margin: 10px">
          <div class="container">
            <v-card class="item" style="width: 47%; height: auto; margin: 5px;">
              <random-pose></random-pose>
            </v-card>
            <div class="item" style="float: left ; width: 3% ;background-color: transparent">
              <img>
            </div>
            <v-card class="item" style="width: 47%; height: auto; text-align: center">
              <video style="width: 100%; height: 100%; background-color: black " id='remoteVideo' ref="remoteVideo"
                     autoplay muted></video>
            </v-card>
          </div>
        </div>


      </div>
    </v-card>
    <div class="item" style="float: left ; width: 5% ;background-color: transparent">
      <img>
    </div>
    <v-card class="item" style="float: left ;background-color: black; margin-right:5% ;width: 35%; height: 650px">
      <div style="margin-top: 15% ;margin-bottom: 15%; ">
        <video style="width: 100%; height: auto" id='localVideo' ref="localVideo" autoplay
               muted></video>
      </div>
    </v-card>

  </div>

</template>

<style scoped>
.container {
  display: flex;
  justify-content: space-around;
  align-content: center;
}

</style>

<script>
import "@tensorflow/tfjs";
import RandomPose from "@/components/BrainWall/RandomPose";
import * as tmPose from "@teachablemachine/pose";
import {mapGetters} from "vuex";

let model, labelContainer, maxPredictions;

const mediaOption = {
  // audio: true,
  video: {
    mandatory: {
      maxWidth: 300,
      maxHeight: 300,
      maxFrameRate: 5,
    },
    optional: [
      {googNoiseReduction: true}, // Likely removes the noise in the captured video stream at the expense of computational effort.
      {facingMode: 'user'}, // Select the front/user facing camera or the rear/environment facing camera if available (on Phone)
    ],
  },
};

export default {
  name: 'BrainWall',

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

      countFlag: false, //카운트 다운 버튼

      ///////////////////////webRTC////////////////////////////////
      startbtnvalue: 'START',
      room: 'foo',
      isInitiator: false,
      isStarted: false,
      isChannelReady: false,
      turnReady: false,
      localStream: {type: Object},
      remoteStream: {type: Object},
      pc: {type: Object},
      pc_config: {
        'iceServers': [{
          'url': 'stun:stun.l.google.com:19302'
        }]
      },
      sdpConstraints: {
        'mandatory': {
          // 'OfferToReceiveAudio': true,
          'OfferToReceiveVideo': true
        }
      },
      constraints: {
        video: true
      },
      makeroom: false

    }
  },
  components: {
    RandomPose,
  },
  computed: {
    ...mapGetters(['getCurrentPose'])
  },
  created() {

    this.$store.commit("changebar", "두뇌의벽");
    //
    // if (this.room !== '') {
    //   console.log('Create or join room', this.room);
    //   this.$socket.emit('create or join', this.room);
    // }
    // this.$socket.on('roommk', function(room){
    //   console.log('room',room);
    //   this.room=room;
    // }.bind(this));


    if (this.room !== '') {
      console.log('Message from client: Asking to join room ' + this.room);
      this.$socket.emit('create or join', this.room);
    }
    // else{
    //   window.room = prompt("방이름을 적어주세용:");
    //   this.room = window.room;
    //   this.$socket.emit('roommk', this.room);
    //   console.log('roomname',this.room);

    this.$socket.on('created', function (room) {
      console.log('Created room ' + room);
      this.isInitiator = true;
    }.bind(this));

    this.$socket.on('full', function (room) {
      console.log('Room ' + room + ' is full');
    });
    let _this = this;
    this.$socket.on('join', function (room) {
      console.log('Another peer made a request to join room ' + room);
      console.log('This peer is the initiator of room ' + room + '!');
      _this.isChannelReady = true;
      console.log('ischannel - join  체크 ' + _this.isChannelReady);

    });

    this.$socket.on('joined', function (room) {
      console.log('This peer has joined room ' + room);
      _this.isChannelReady = true;
      console.log('ischannel - joined 체크 ' + _this.isChannelReady);
    });

    this.$socket.on('log', function (array) {
      console.log.apply(console, array);
    });

    this.$socket.on('message', function (message) {
      console.log('Client received message:', message);
      if (message === 'got user media') {
        this.maybeStart2();
      } else if (message.type === 'offer') {
        if (!this.isInitiator && !_this.isStarted) {
          this.maybeStart2();
        }
        this.pc.setRemoteDescription(new RTCSessionDescription(message));
        this.doAnswer();
      } else if (message.type === 'answer' && this.isStarted) {
        this.pc.setRemoteDescription(new RTCSessionDescription(message));
      } else if (message.type === 'candidate' && this.isStarted) {
        let candidate = new RTCIceCandidate({
          sdpMLineIndex: message.label,
          candidate: message.candidate
        });
        this.pc.addIceCandidate(candidate);
      } else if (message === 'bye' && this.isStarted) {
        this.handleRemoteHangup();
      }
    }.bind(this));


    navigator.mediaDevices.getUserMedia(mediaOption)
        .then(this.gotStream)
        .catch(function (e) {
          alert('getUserMedia() error: ' + e.name);
        });


    this.$socket.on('changepose', (data) => {
      console.log(data.tempRandomNumber, data.round);
      this.changeCurrentPoseM(data.tempRandomNumber);
      this.round = data.round;
      console.log(data.tempRandomNumber, this.round);
    }).bind(this);

    if (location.hostname !== "localhost") {
      this.requestTurn('https://computeengineondemand.appspot.com/turn?username=41784574&key=4080218913');
    }
    window.onbeforeunload = function () {
      this.sendMessage('bye');
    }
  },

  methods: {
    sendMessage(message) {
      console.log('Client sending message: ', message);
      this.$socket.emit('message', message);
    },
    maybeStart2() {
      console.log('>>>>>>> maybeStart() ', this.isStarted,
          this.localStream, this.isChannelReady);
      console.log('ddddddd ' + this.isChannelReady);
      if (!this.isStarted && this.localStream.active === true
          && this.isChannelReady) {
        console.log('crestepeerconnection')
        this.createPeerConnection();
        this.pc.addStream(this.localStream);
        this.isStarted = true;
        console.log('isInitiator' + this.isInitiator);
        if (this.isInitiator) {
          this.doCall();
        }
      }
    },
    gotStream(stream) {
      console.log('Adding local stream.');
      this.localStream = stream;
      // this.$refs.localVideo.src = window.URL.createObjectURL(stream);
      this.$refs.localVideo.srcObject = stream;
      this.sendMessage('got user media');
      if (this.isInitiator) {
        this.maybeStart2();
      }
    },
    createPeerConnection() {
      try {
        this.pc = new RTCPeerConnection(null);
        this.pc.onicecandidate = this.handleIceCandidate;
        this.pc.onaddstream = this.handleRemoteStreamAdded;
        this.pc.onremovestream = this.handleRemoteStreamRemoved;
        console.log('Created RTCPeerConnnection');
      } catch (e) {
        console.log('Failed to create PeerConnection, exception: ' + e.message);
        alert('Cannot create RTCPeerConnection object.');
        // return;
      }
    },
    handleIceCandidate(event) {
      console.log('handleIceCandidate event: ', event);
      if (event.candidate) {
        this.sendMessage({
          type: 'candidate',
          label: event.candidate.sdpMLineIndex,
          id: event.candidate.sdpMid,
          candidate: event.candidate.candidate
        });
      } else {
        console.log('End of candidates.');
      }
    },
    handleCreateOfferError(event) {
      console.log('createOffer() error: ', event);
    },
    doCall() {
      console.log('Sending offer to peer');
      this.pc.createOffer(this.setLocalAndSendMessage,
          this.handleCreateOfferError);
    },
    doAnswer() {
      console.log('Sending answer to peer.');
      this.pc.createAnswer().then(
          this.setLocalAndSendMessage,
          this.onCreateSessionDescriptionError
      );
    },
    setLocalAndSendMessage(sessionDescription) {
      this.pc.setLocalDescription(sessionDescription);
      console.log('setLocalAndSendMessage sending message', sessionDescription);
      this.sendMessage(sessionDescription);
    },
    onCreateSessionDescriptionError(error) {
      console.log('Failed to create session description: ' + error.toString());
    },
    requestTurn(turn_url) {
      let turnExists = false;
      console.log(turn_url);
      for (let i in this.pc_config.iceServers) {
        if (this.pc_config.iceServers[i].url.substr(0, 5) === 'turn:') {
          turnExists = true;
          this.turnReady = true;
          break;
        }
      }
      if (!turnExists) {
        console.log('Getting TURN server from ', turn_url);
        // No TURN server. Get one from computeengineondemand.appspot.com:
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4 && xhr.status === 200) {
            let turnServer = JSON.parse(xhr.responseText);
            console.log('Got TURN server: ', turnServer);
            this.pc_config.iceServers.push({
              'urls': 'turn:' + turnServer.username + '@' + turnServer.turn,
              'credential': turnServer.password
            });
            this.turnReady = true;
          }
        };
        xhr.open('GET', turn_url, true);
        xhr.send();
      }
    },
    handleRemoteStreamAdded(event) {
      console.log('Remote stream added.');
      this.remoteStream = event.stream;
      this.$refs.remoteVideo.srcObject = event.stream;
      this.$refs.remoteVideo.classList.add("remoteVideoInChatting");
      this.$refs.localVideo.classList.add("localVideoInChatting");


    },
    handleRemoteStreamRemoved(event) {
      console.log('Remote stream removed. Event: ', event);
    },
    hangup() {
      console.log('Hanging up.');
      this.stop();
      this.sendMessage('bye');
    },
    handleRemoteHangup() {
      this.$refs.remoteVideo.classList.remove("remoteVideoInChatting");
      this.$refs.localVideo.classList.remove("localVideoInChatting");

      console.log('Session terminated.');
      stop();
      this.isInitiator = false;
    },
    stop() {
      this.isStarted = false;
      this.pc.close();
      this.pc = null;
    },
    ///////////////////////webRTC////////////////////////////////

    clickStart() {
      this.init()
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
          alert('게임이 종료되었습니다.')
          this.roundFinishFlag = true;
          this.gameStartFlag = false;
          this.round = 0
          this.score = 0

        }
      }
    },
    generateRandomNumber() {
      let tempRandomNumber = Math.floor(Math.random() * 3 + 1) // 숫자 바꾸면 됨
      this.changeCurrentPoseM(tempRandomNumber)
      this.round++


      this.countDown = 5
      this.countFlag = true
      this.countDownTimer()

      // if(this.round==5){
      //   this.roundFinishFlag = true
      //   this.round = 0
      //   this.score=0
      // }
      this.scoreFlag = false
      this.$socket.emit('changepose',
          {tempRandomNumber: tempRandomNumber, round: this.round});

      console.log(tempRandomNumber);
    },
    changeCurrentPoseM: function (x) {
      this.$store.commit("changeCurrentPose", x)
    },
    async init() {
      this.startBtn = false;

      const URL = "https://teachablemachine.withgoogle.com/models/sV2phcmJ-/";
      const modelURL = URL + "model.json";
      const metadataURL = URL + "metadata.json";

      // load the model and metadata
      // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
      // Note: the pose library adds a tmPose object to your window (window.tmPose)
      model = await tmPose.load(modelURL, metadataURL);
      maxPredictions = model.getTotalClasses();

      // Convenience function to setup a webcam
      // const size = 400;
      // const flip = true; // whether to flip the webcam
      // webcam = new tmPose.Webcam(size, size, flip); // width, height, flip
      // await webcam.setup(); // request access to the webcam
      // await webcam.play();
      this.requestId = window.requestAnimationFrame(this.loop);

      // append/get elements to the DOM
      // const canvas = document.getElementById("canvas");
      //
      // canvas.width = size;
      // canvas.height = size;
      // ctx = canvas.getContext("2d");

      labelContainer = document.getElementById("label-container");
      for (let i = 0; i < maxPredictions; i++) {
        // and class labels
        labelContainer.appendChild(document.createElement("div"));
      }
    },
    async loop() {
      //timestamp
      //   webcam.update(); // update the webcam frame
      await this.predict(); //this.predict();
      if (this.requestId) {

        window.requestAnimationFrame(this.loop);
      }
    },
    async predict() {
      // Prediction #1: run input through posenet
      // estimatePose can take in an image, video or canvas html element
      // const { pose, posenetOutput } = await model.estimatePose(webcam.canvas);
      // Prediction 2: run input through teachable machine classification model
      const {posenetOutput} = await model.estimatePose(this.$refs.localVideo);
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
          labelContainer.childNodes[0].innerHTML = " 정확도 : " + prediction[i].probability.toFixed(2);
        }

        if (this.$store.state.currentPose == prediction[i].className && !this.scoreFlag && prediction[i].probability.toFixed(2) >= 0.9) {
          if (this.countDown > 0) {
            this.score++
            this.scoreFlag = true
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
        // this.drawPose(pose);
      }

      // drawPose(pose) {
      // if (webcam.canvas) {
      //   // console.log("drawPose method");
      //   ctx.drawImage(webcam.canvas, 0, 0);
      //   // draw the keypoints and skeleton
      //   if (pose) {
      //     const minPartConfidence = 0.5;
      //     tmPose.drawKeypoints(pose.keypoints, minPartConfidence, ctx);
      //     tmPose.drawSkeleton(pose.keypoints, minPartConfidence, ctx);
      //   }
      // }

    }
  }
}
</script>
