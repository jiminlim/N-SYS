<template>
  <v-card class="mx-auto" max-width="344" outlined>
    <v-card-actions>
      <div class="my-2">
        <v-btn
          color="deep-purple accent-4"
          router
          :to="{ name: 'users' }"
          v-if="!login"
          >Login</v-btn
        >
      </div>

      <div class="ma-2">
        <v-btn color="deep-purple accent-4" @click="log_out" v-if="login"
          >Logout</v-btn
        >
        <v-btn color="deep-purple accent-4" router-link to="/webcam"
          >Webcam</v-btn
        >
      </div>
    </v-card-actions>
    <v-divider></v-divider>
    <v-list-item three-line>
      <v-list-item-content>
        <div class="overline mb-4">
          <v-btn
            color="deep-purple accent-4"
            router
            :to="{ name: 'myprofile' }"
            v-if="login"
            >MyPage</v-btn
          >
        </div>
        <v-list-item-title class="headline mb-1"
          >User@email.com</v-list-item-title
        >
      </v-list-item-content>

    </v-list-item>
    <v-list dense>
      <v-list-item router :to="{ name: 'game1' }">
        <v-list-item-action>
          <v-icon>mdi-view-dashboard</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>두뇌의벽</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item router :to="{ name: 'game2' }">
        <v-list-item-action>
          <v-icon>mdi-view-dashboard</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>뱀게임 </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>
<script>
export default {
  data() {
    return {
      login: localStorage.getItem("IsLogin"),
    };
  },
  methods: {
    log_out() {
      localStorage.clear();
      window.location.href = "/";
    },
  },
};
</script>
