<template>
  <v-card
      class="mx-auto"
      max-width="344"
      outlined
  >
    <v-card-actions>
      <div class="my-2">
        <v-btn color="deep-purple accent-4"
               router :to="{name: 'users'}">Login</v-btn>
      </div>
      <div class="ma-2">
        <v-btn color="deep-purple accent-4"
               router-link to="/webcam" >Webcam</v-btn>
      </div>
    </v-card-actions>
    <v-divider></v-divider>
    <v-list-item three-line>

      <v-list-item-content>
        <div class="overline mb-4">mypage</div>
        <v-list-item-title class="headline mb-1">User@email.com</v-list-item-title>
<!--        <v-list-item-subtitle>Greyhound divisely hello coldly fonwderfully</v-list-item-subtitle>-->
      </v-list-item-content>

<!--      <v-list-item-avatar-->
<!--          tile-->
<!--          size="80"-->
<!--          color="grey"-->
<!--      ></v-list-item-avatar>-->
    </v-list-item>
    <v-list dense>
      <v-list-item router :to="{name: 'users'}">
        <v-list-item-action>
          <v-icon>mdi-view-dashboard</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>전적 1 </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item router :to="{name: 'step5'}">
        <v-list-item-action>
          <v-icon>mdi-view-dashboard</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title >step5</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>