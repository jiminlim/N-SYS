<template>
  <div class="container">
    <h1>local webRTC </h1>
    <div id='videos'>
      <video id='localVideo' ref="localVideo" autoplay muted></video>
      <video id='remoteVideo' ref="remoteVideo" autoplay></video>
    </div>
  </div>
</template>

<script>
const mediaOption = {
  audio: true,
  video: {
    mandatory: {
      maxWidth: 160,
      maxHeight: 120,
      maxFrameRate: 5,
    },
    optional: [
      { googNoiseReduction: true }, // Likely removes the noise in the captured video stream at the expense of computational effort.
      { facingMode: 'user' }, // Select the front/user facing camera or the rear/environment facing camera if available (on Phone)
    ],
  },
};
export default {
  data() {
    return {
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
          'OfferToReceiveAudio': true,
          'OfferToReceiveVideo': true
        }
      },
      constraints: {
        video: true
      }
    }
  },
  created() {
   let _this = this;
    if (this.room !== '') {
      console.log('Create or join room', this.room);
      this.$socket.emit('create or join', this.room);
    }
    this.$socket.on('created', function (room){
      console.log('Created room ' + room);
      this.isInitiator = true;
    }.bind(this));

    this.$socket.on('full', function (room){
      console.log('Room ' + room + ' is full');
    });

    this.$socket.on('join', function (room){
      console.log('Another peer made a request to join room ' + room);
      console.log('This peer is the initiator of room ' + room + '!');
      _this.isChannelReady = true;
      console.log('ischannel - join  체크 '+_this.isChannelReady);

    });

    this.$socket.on('joined', function (room){
      console.log('This peer has joined room ' + room);
      _this.isChannelReady = true;
      console.log('ischannel - joined 체크 '+_this.isChannelReady);
    });

    this.$socket.on('log', function (array){
      console.log.apply(console, array);
    });
    /////////////////////////////////////////////////////////////////

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
    ////////////////////////////////////////////////////////////////////////

    navigator.mediaDevices.getUserMedia(mediaOption)
        .then(this.gotStream)
        .catch(function(e) {
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
      console.log('ddddddd '+this.isChannelReady);
      if (!this.isStarted && this.localStream.active === true
          && this.isChannelReady) {
        console.log('crestepeerconnection')
        this.createPeerConnection();
        this.pc.addStream(this.localStream);
        this.isStarted = true;
        console.log('isInitiator'+ this.isInitiator);
        if (this.isInitiator) {
          this.doCall();
        }
      }
    },
    gotStream(stream) {
      console.log('Adding local stream.');
      this.localStream = stream;
      // this.$refs.localVideo.src = window.URL.createObjectURL(stream);
      this.$refs.localVideo.srcObject=stream;
      this.sendMessage('got user media');
      if (this.isInitiator) {
        this.maybeStart2();
      }
    },
    // handleUserMediaError(error){
    //   console.log('getUserMedia error: ', error);
    // },
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
          candidate: event.candidate.candidate});
      } else {
        console.log('End of candidates.');
      }
    },
    handleCreateOfferError(event){
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
      // this.pc.createAnswer(this.setLocalAndSendMessage,
      //     null,
      //     this.sdpConstraints);
    },
    setLocalAndSendMessage(sessionDescription) {
      // Set Opus as the preferred codec in SDP if Opus is present.
      // sessionDescription.sdp = this.preferOpus(sessionDescription.sdp);
      this.pc.setLocalDescription(sessionDescription);
      console.log('setLocalAndSendMessage sending message' , sessionDescription);
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
        xhr.onreadystatechange = function(){
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
      // this.$refs.remoteVideo.src =
      //     window.URL.createObjectURL(event.stream);
      // this.remoteStream = event.stream;
      // let _this = this;
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
    // preferOpus(sdp) {
    //   // Set Opus as the default audio codec if it's present.
    //   let sdpLines = sdp.split('\r\n');
    //   let mLineIndex;
    //   // Search for m line.
    //   for (let i = 0; i < sdpLines.length; i++) {
    //     if (sdpLines[i].search('m=audio') !== -1) {
    //       mLineIndex = i;
    //       break;
    //     }
    //   }
    //   if (mLineIndex === null) {
    //     return sdp;
    //   }
    //   // If Opus is available, set it as the default in m line.
    //   for (let i = 0; i < sdpLines.length; i++) {
    //     if (sdpLines[i].search('opus/48000') !== -1) {
    //       let opusPayload = this.extractSdp(sdpLines[i], /:(\d+) opus\/48000/i);
    //       if (opusPayload) {
    //         sdpLines[mLineIndex] = this.setDefaultCodec(sdpLines[mLineIndex], opusPayload);
    //       }
    //       break;
    //     }
    //   }
    //   // Remove CN in m line and sdp.
    //   sdpLines = this.removeCN(sdpLines, mLineIndex);
    //   sdp = sdpLines.join('\r\n');
    //   return sdp;
    // },
    // extractSdp(sdpLine, pattern) {
    //   let result = sdpLine.match(pattern);
    //   return result && result.length === 2 ? result[1] : null;
    // },
    // setDefaultCodec(mLine, payload) {
    //   // Set the selected codec to the first in m line.
    //   let elements = mLine.split(' ');
    //   let newLine = [];
    //   let index = 0;
    //   for (let i = 0; i < elements.length; i++) {
    //     if (index === 3) { // Format of media starts from the fourth.
    //       newLine[index++] = payload; // Put target payload to the first.
    //     }
    //     if (elements[i] !== payload) {
    //       newLine[index++] = elements[i];
    //     }
    //   }
    //   return newLine.join(' ');
    // },
    // removeCN(sdpLines, mLineIndex) {
    //   // Strip CN from sdp before CN constraints is ready.
    //   console.log(sdpLines[mLineIndex]);
    //   let mLineElements = sdpLines[mLineIndex].split(' ');
    //   // Scan from end for the convenience of removing an item.
    //   for (let i = sdpLines.length-1; i >= 0; i--) {
    //     let payload = this.extractSdp(sdpLines[i], /a=rtpmap:(\d+) CN\/\d+/i);
    //     if (payload) {
    //       let cnPos = mLineElements.indexOf(payload);
    //       if (cnPos !== -1) {
    //         // Remove CN payload from m line.
    //         mLineElements.splice(cnPos, 1);
    //       }
    //       // Remove CN line in sdp
    //       sdpLines.splice(i, 1);
    //     }
    //   }
    //   sdpLines[mLineIndex] = mLineElements.join(' ');
    //   return sdpLines;
    // }
  }
}
</script>