<template>
  <div>
    <h1>step 4</h1>
  </div>
</template>
<script>
export default {
  data (){
    return {
      isInitiator : false,
      room : ''
    }
  },
  created() {
    this.$socket.on('created', function(room, clientId) {
      this.isInitiator = true;
      console.log('created'+room+' '+clientId);
    });

    this.$socket.on('full', function(room) {
      console.log('Message from client: Room ' + room + ' is full :^(');
    });

    this.$socket.on('ipaddr', function(ipaddr) {
      console.log('Message from client: Server IP address is ' + ipaddr);
    });

    this.$socket.on('joined', function(room, clientId) {
      this.isInitiator = false;
      console.log('joined'+room+' '+clientId);
    });

    this.$socket.on('log', function(array) {
      console.log.apply(console, array);
    });
  },
  mounted() {
    window.room = prompt("Enter room name:");
    this.room = window.room;
    // this.room = 'ddnflkndfklndf';
    console.log('hhhhhh',this.room);


    if (this.room !== "") {
      console.log('Message from client: Asking to join room ' + this.room);
      this.$socket.emit('create or join', this.room);
    }
  }
}
</script>