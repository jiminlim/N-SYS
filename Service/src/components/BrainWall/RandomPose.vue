<template>
  <div >

<!--    <v-img :src="require(`@/assets/images/pose/${getCurrentPose}.jpg`)" contain></v-img>-->
    <v-img :src="require(`@/assets/images/pose/img1.png`)" contain></v-img>

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