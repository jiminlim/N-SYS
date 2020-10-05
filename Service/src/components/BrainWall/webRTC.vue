<template>
  <div>
    <div>
      <div v-if="gameStartFlag">
        <div>{{ countDown }}</div>
        <div v-if="!roundFinishFlag">
          round - {{ round }}/5
          <div>score - {{ score }}</div>
          <button @click="generateRandomNumber()">포즈 바꾸기 버튼</button>
          <div>현재 포즈 이름 - {{ getCurrentPose }}</div>
          <random-pose></random-pose>
        </div>
        <div v-else-if="roundFinishFlag">
        </div>
      </div>
      <button @click="clickStart()" class="btn2 m-3">START</button>

      <div style="border-style:solid">
        <canvas id="canvas"></canvas>
      </div>

      <div style="border-style:solid" id="label-container">
        <h2>good</h2>
        <h2>bad</h2>
      </div>

      <div class="container">
        <h1>local webRTC </h1>
        <div id='videos'>
          <video id='localVideo' ref="localVideo" autoplay muted></video>
          <video id='remoteVideo' ref="remoteVideo" autoplay></video>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import '@tensorflow/tfjs'
import RandomPose from "@/components/BrainWall/RandomPose";
import * as tmPose from "@teachablemachine/pose"
import {mapGetters} from "vuex";

let model, labelContainer, maxPredictions;
// let model, ctx, labelContainer, maxPredictions;
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
      countDown: 10,

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
    ...mapGetters(['getCurrentPose']),
  }
  ,
  created() {
    let _this = this;
    this.$store.commit("changebar","두뇌의벽");

    if (this.room !== '') {

      console.log('Create or join room', this.room);
      this.$socket.emit('create or join', this.room);
    }
    this.$socket.on('created', function (room) {
      console.log('Created room ' + room);
      this.isInitiator = true;
    }.bind(this));

    this.$socket.on('full', function (room) {
      console.log('Room ' + room + ' is full');
    });

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

    this.$socket.on('changepose',function(tempRandomNumber, round){
      console.log('changepose ',tempRandomNumber,' round :  ',round);

      this.changeCurrentPoseM(tempRandomNumber); // 바꿔줌 .

    })

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
      }
    },
    generateRandomNumber() {
      let tempRandomNumber = Math.floor(Math.random() * 3 + 1) // 숫자 바꾸면 됨
      // this.changeCurrentPoseM(tempRandomNumber)
      this.round++

      this.$socket.emit('changepose', tempRandomNumber, this.round);

      this.countDown = 10
      this.countDownTimer()
      if (this.round == 5) {
        this.roundFinishFlag = true
        this.round = 0
        this.score = 0
      }
      this.scoreFlag = false

      // console.log(tempRandomNumber)
    },
    changeCurrentPoseM: function (x) {
      this.$store.commit("changeCurrentPose", x)
    },
    async init() {
      this.startBtn = false;

      const URL = "https://teachablemachine.withgoogle.com/models/sV2phcmJ-/";
      const modelURL = URL + "model.json";
      const metadataURL = URL + "metadata.json";


      model = await tmPose.load(modelURL, metadataURL);
      maxPredictions = model.getTotalClasses();

      const size = 400;
      this.requestId = window.requestAnimationFrame(this.loop);

      // append/get elements to the DOM
      const canvas = document.getElementById("canvas");

      canvas.width = size;
      canvas.height = size;


      // ctx = canvas.getContext("2d");
      labelContainer = document.getElementById("label-container");
      for (let i = 0; i < maxPredictions; i++) { // and class labels
        labelContainer.appendChild(document.createElement("div"));
      }
    },
    async loop() {
      await this.predict(); //this.predict();
      if (this.requestId) {
        window.requestAnimationFrame(this.loop);
      }

    },
    async predict() {
      // const {pose, posenetOutput} = await model.estimatePose(this.$refs.localVideo);
      const {posenetOutput} = await model.estimatePose(this.$refs.localVideo);
      const prediction = await model.predict(posenetOutput);
      if (prediction[0].probability.toFixed(1) == 1) {
        // console.log(prediction[0].probability.toFixed(1));
      }

      let i = 0;
      for (i = 0; i < maxPredictions; i++) {
        // console.log(this.$store.state.currentPose)
        // console.log(prediction[i].className)
        if (this.$store.state.currentPose == prediction[i].className && !this.scoreFlag && prediction[i].probability.toFixed(2) >= 0.9) {
          if (this.countDown > 0) {
            this.score++
            this.scoreFlag = true
          }

        }
        const classPrediction =
            prediction[i].className + ": " + prediction[i].probability.toFixed(2);
        labelContainer.childNodes[i].innerHTML = classPrediction;
      }
      // this.drawPose(pose);
    },
    // drawPose(pose) {
    //   if (this.$refs.localVideo) {
    //     ctx.drawImage(this.$refs.localVideo, 0, 0);
    //     if (pose) {
    //       const minPartConfidence = 0.5;
    //       tmPose.drawKeypoints(pose.keypoints, minPartConfidence, ctx);
    //       tmPose.drawSkeleton(pose.keypoints, minPartConfidence, ctx);
    //     }
    //   }
    // },

  }
}
</script>