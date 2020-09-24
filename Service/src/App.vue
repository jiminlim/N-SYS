<template>
  <v-app id="inspire">
<!--    <v-navigation-drawer-->
<!--        v-model="drawer"-->
<!--        app-->
<!--        clipped >-->
<!--      <v-list dense>-->
<!--        <v-list-item router :to="{name: 'users'}">-->
<!--          <v-list-item-action>-->
<!--            <v-icon>mdi-view-dashboard</v-icon>-->
<!--          </v-list-item-action>-->
<!--          <v-list-item-content>-->
<!--            <v-list-item-title>User</v-list-item-title>-->
<!--          </v-list-item-content>-->
<!--        </v-list-item>-->
<!--      </v-list>-->
<!--    </v-navigation-drawer>-->

    <v-app-bar app  clipped-left  >
<!--      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>-->
      <v-menu
          bottom
          right
          offset-y
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
              dark
              icon
              v-bind="attrs"
              v-on="on"
          >
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <mypageCard></mypageCard>
      </v-menu>
      <v-toolbar-title @click="$router.push('/')">Application</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>

    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import mypageCard from '@/components/Users/mypage'
export default {
  props: {
    source: String,
  },
  components:{
    mypageCard
  },
  data: () => ({
    drawer: null,
  }),
  created () {
    this.$vuetify.theme.dark = true
  },
  methods:{
  }
}
</script>