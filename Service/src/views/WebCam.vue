<template>
  <div>
    <video ref="localVideo"></video>
<!--    <video ref="remoteVideo"></video>-->
    <button id="start">start</button>
    <button id="call">call</button>
    <button id="hangup">hang up</button>

  </div>
</template>
<script>
export default {
  data (){
    return{
      mediaStream: null,
    }
  },
  mounted() {
    navigator.mediaDevices.getUserMedia({video:true})
        .then(mediaStream=>{
          this.mediaStream = mediaStream;
          // this.$refs.localVideo.srcObject = mediaStream;
          // this.$refs.localVideo.play()
          this.$refs.localVideo.srcObject=mediaStream;
          this.$refs.localVideo.play();
        }).catch(error=>{
        console.log('navigator.getUserMedia error: ', error);
    });

  },
  methods:{
// Handles success by adding the MediaStream to the video element.
//     gotLocalMediaStream (mediaStream) {
//       localStream = mediaStream;
//       localVideo.srcObject = mediaStream;
//     },

// Handles error by logging a message to the console with the error message.
//     handleLocalMediaStreamError(error) {
//       console.log('navigator.getUserMedia error: ', error);
//     }
  }
}

</script>