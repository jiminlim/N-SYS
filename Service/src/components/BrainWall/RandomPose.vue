<template>
  <div>
    <div>{{RandomNumber}}</div>

<!--    <v-img src="'@/assets/images/pose/'+{{RandomNumber}}+'.jpg'"  contain-->
<!--    <v-img :src="tempsrc"  contain-->
<!--    <v-img src="@/assets/images/pose/1.jpg"  contain-->
    <v-img :src="require(`@/assets/images/pose/${RandomNumber}.jpg`)"  contain
    height="400px"
    width="400px"></v-img>
  </div>
<!--  <div>-->
<!--    <div>{{RandomNumber}}</div>-->
<!--    <v-img :src="imgpath"  contain-->

<!--           height="400px"-->
<!--           width="400px"></v-img>-->
<!--  </div>-->
</template>

<script>
// import pose from '@/assets/images/pose'

export default {
  name: 'RandomPose',
  props:
    ['RandomNumber']

  ,
  data() {
    return {
    }
  },
  // computed :{
  //   tempsrc: ()=>{
  //     return `@/assets/images/pose/`+this.randnum+`.jpg`
  //   }
  // }
}
</script>