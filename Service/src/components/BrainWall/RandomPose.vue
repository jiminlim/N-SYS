<template>
  <div >
    <v-card >
    <v-img :src="require(`@/assets/images/pose/${getCurrentPose}.png`)" style="height: 300px" contain></v-img>
    </v-card>
  </div>

</template>

<script>

import {mapGetters} from 'vuex'

export default {
  name: 'RandomPose',

  computed:{
    ...mapGetters(['getCurrentPose'])
  },
  methods:{

  },

}
</script>