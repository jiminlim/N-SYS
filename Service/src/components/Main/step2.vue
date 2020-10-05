<template>
  <div class="container">
    <div id='videos'>
      <video id='localVideo' ref="localVideo" autoplay muted></video>
      <video id='remoteVideo' ref="remoteVideo" autoplay></video>
      <div>
        <button :disabled="s_disabled" id="startButton" @click="startAction" >Start</button>
        <button :disabled="c_disabled"  id="callButton" @click="callAction">Call</button>
        <button :disabled="h_disabled" id="hangupButton" @click="hangupAction">Hang Up</button>
      </div>
    </div>
  </div>
</template>
<script>
//  import JsSIP from 'jssip'
// import Vue from 'vue';
// import io from 'vue-socket.io';
// const localVideo = document.getElementById('localVideo');
// const remoteVideo = document.getElementById('remoteVideo');
// const startButton = document.getElementById('startButton');
// const callButton = document.getElementById('callButton');
// const hangupButton = document.getElementById('hangupButton');


export default {
  data() {
    return {
      startTime : null,
      localStream: null,
      remoteStream: null,
      localPeerConnection : {type: Object},
      remotePeerConnection :{type: Object},
      mediaStreamConstraints: {
        video: true
      },
      offerOptions :{
        offerToReceiveVideo : 1
      },
      s_disabled:false,
      c_disabled:false,
      h_disabled:false,
    }
  },
  mounted() {
  },
  methods: {
    startAction() {
      this.s_disabled = true;
      navigator.mediaDevices.getUserMedia(this.mediaStreamConstraints)
          .then(this.gotLocalMediaStream).catch(this.handleLocalMediaStreamError);
      this.trace('Requesting local stream.');
    },
    callAction() {
      this.c_disabled = true;
      this.h_disabled = false;

      this.trace('Starting call.');
      this.startTime = window.performance.now();

      // Get local media stream tracks.
      const videoTracks = this.localStream.getVideoTracks();
      // const audioTracks = this.localStream.getAudioTracks();
      if (videoTracks.length > 0) {
        this.trace(`Using video device: ${videoTracks[0].label}.`);
      }
      // if (audioTracks.length > 0) {
      //   this.trace(`Using audio device: ${audioTracks[0].label}.`);
      // }

      const servers = null;  // Allows for RTC server configuration.

      // Create peer connections and add behavior.
      this.localPeerConnection = new RTCPeerConnection(servers);
      this.trace('Created local peer connection object localPeerConnection.');

      this.localPeerConnection.addEventListener('icecandidate', this.handleConnection);
      this.localPeerConnection.addEventListener(
          'iceconnectionstatechange', this.handleConnectionChange);

      this.remotePeerConnection = new RTCPeerConnection(servers);
      this.trace('Created remote peer connection object remotePeerConnection.');

      this.remotePeerConnection.addEventListener('icecandidate', this.handleConnection);
      this.remotePeerConnection.addEventListener(
          'iceconnectionstatechange', this.handleConnectionChange);
      this.remotePeerConnection.addEventListener('addstream', this.gotRemoteMediaStream);

      // Add local stream to connection and create offer to connect.
      this.localPeerConnection.addStream(this.localStream);
      this.trace('Added local stream to localPeerConnection.');

      this.trace('localPeerConnection createOffer start.');
      this.localPeerConnection.createOffer(this.offerOptions)
          .then(this.createdOffer).catch(this.setSessionDescriptionError);
    },

    handleConnection(event) {
      const peerConnection = event.target;
      const iceCandidate = event.candidate;

      function getPeerName(peerConnection) {
          return (peerConnection === this.localPeerConnection) ?
              'localPeerConnection' : 'remotePeerConnection';
      }

      if (iceCandidate) {
        const newIceCandidate = new RTCIceCandidate(iceCandidate);
        const otherPeer = (peerConnection === this.localPeerConnection) ?
            this.remotePeerConnection : this.localPeerConnection;

        otherPeer.addIceCandidate(newIceCandidate)
            .then(() => {
              this.trace(`${getPeerName(peerConnection)} addIceCandidate success.`);
            }).catch((error) => {
               this.trace(`${getPeerName(peerConnection)} failed to add ICE Candidate:\n`+
              `${error.toString()}.`);
        });

        this.trace(`${getPeerName(peerConnection)} ICE candidate:\n` +
            `${event.candidate.candidate}.`);
      }
    },
    handleConnectionChange(event) {
      function getPeerName(peerConnection) {
        return (peerConnection === this.localPeerConnection) ?
            'localPeerConnection' : 'remotePeerConnection';
      }
      const peerConnection = event.target;
      console.log('ICE state change event: ', event);
      this.trace(`${getPeerName(peerConnection)} ICE state: ` +
          `${peerConnection.iceConnectionState}.`);
    },

    createdOffer(description) {
      this.trace(`Offer from localPeerConnection:\n${description.sdp}`);

      this.trace('localPeerConnection setLocalDescription start.');
      this.localPeerConnection.setLocalDescription(description)
          .then(() => {
            this.setLocalDescriptionSuccess(this.localPeerConnection);
          }).catch(this.setSessionDescriptionError);
      this.trace('remotePeerConnection setRemoteDescription start.');
      this.remotePeerConnection.setRemoteDescription(description)
          .then(() => {
            this.setRemoteDescriptionSuccess(this.remotePeerConnection);
          }).catch(this.setSessionDescriptionError);

      this.trace('remotePeerConnection createAnswer start.');
      this.remotePeerConnection.createAnswer()
          .then(this.createdAnswer)
          .catch(this.setSessionDescriptionError);
    },
    setDescriptionSuccess(peerConnection, functionName) {
      function getPeerName(peerConnection) {
        return (peerConnection === this.localPeerConnection) ?
            'localPeerConnection' : 'remotePeerConnection';
      }
      const peerName = getPeerName(peerConnection);
      this.trace(`${peerName} ${functionName} complete.`);
    },
    setLocalDescriptionSuccess(peerConnection) {
      this.setDescriptionSuccess(peerConnection, 'setLocalDescription');
    },
    setRemoteDescriptionSuccess(peerConnection) {
      this.setDescriptionSuccess(peerConnection, 'setRemoteDescription');
    },
    createdAnswer(description) {
      this.trace(`Answer from remotePeerConnection:\n${description.sdp}.`);

      this.trace('remotePeerConnection setLocalDescription start.');
      this.remotePeerConnection.setLocalDescription(description)
          .then(() => {
            this.setLocalDescriptionSuccess(this.remotePeerConnection);
          }).catch(this.setSessionDescriptionError);

      this.trace('localPeerConnection setRemoteDescription start.');
      this.localPeerConnection.setRemoteDescription(description)
          .then(() => {
            this.setRemoteDescriptionSuccess(this.localPeerConnection);
          }).catch(this.setSessionDescriptionError);
    },
    setSessionDescriptionError(error) {
      this.trace(`Failed to create session description: ${error.toString()}.`);
    },

    hangupAction() {
      this.trace('Ending call.');
      this.trace(''+this.localPeerConnection);
      this.trace(''+this.remotePeerConnection);


      this.localPeerConnection.close();
      this.remotePeerConnection.close();
      this.localPeerConnection = null;
      this.remotePeerConnection = null;
      this.h_disabled = true;
      this.c_disabled = false;

      this.trace('Ending call.');

    },
    //getusermedia
    gotLocalMediaStream(mediaStream) {
      // localVideo.srcObject = mediaStream;
      this.$refs.localVideo.srcObject=mediaStream;
      this.localStream = mediaStream;
      this.trace('Received local stream.');
      // callButton.disabled = false;  // Enable call button.
      this.c_disabled = false;
    },
    gotRemoteMediaStream(event) {
      const mediaStream = event.stream;
      // remoteVideo.srcObject = mediaStream;
      this.$refs.remoteVideo.srcObject = mediaStream;
      this.remoteStream = mediaStream;
      this.trace('Remote peer connection received remote stream.');
    },
    handleLocalMediaStreamError(error) {
      this.trace(`navigator.getUserMedia error: ${error.toString()}.`);
    },
    trace(text) {
      text = text.trim();
      const now = (window.performance.now() / 1000).toFixed(3);
      console.log(now, text);
    }
  }
}
</script>