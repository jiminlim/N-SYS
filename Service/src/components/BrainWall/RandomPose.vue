<template>
  <div>

    <v-img :src="require(`@/assets/images/pose/${getCurrentPose}.jpg`)"  contain
    height="400px"
    width="400px"></v-img>

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