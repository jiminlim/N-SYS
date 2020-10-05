<template>

  <div class="page-container">
    <div>
    <textarea v-model="textarea" placeholder="textarea"></textarea>
    <input v-model="message" placeholder="btn"/>
    <button @click="sendMessage()">Submit</button>
    </div>
  </div>
</template>
<script> export default {
  name: 'Chat',
  created() {

    this.$socket.on('chat', (data) => {
      this.textarea += '[' + data.socketId + ']' + data.message + "\n"
    })
  }, data() {
    return {textarea: "", message: '',  socketId: ''}
  }, methods: {
    sendMessage() {
      this.$socket.emit('chat', {message: this.message, socketId: this.$socket.id});
      this.textarea +=  '[' + this.$socket.id + ']' +this.message + "\n"
      this.message = '';
      this.socketId = this.$socket.id;
    }
  }
} </script>
<style>
.md-app {
  height: 800px;
  border: 1px solid;
}

.md-textarea {
  height: 300px;
} </style>
