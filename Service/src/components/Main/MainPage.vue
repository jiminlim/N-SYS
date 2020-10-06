<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col cols="12">
        <v-container class="fill-height" :class="sheet1" @click="toggleSheet">
          <v-hover v-slot:default="{ hover }">
            <v-card
              :elevation="hover ? 24 : 2"
              class="mx-auto"
              height="400"
              max-width="350"
            >
              <v-img
                src="@/assets/images/insertcoin.png"
                height="400"
                max
                width="350"
              ></v-img>
            </v-card>
          </v-hover>
        </v-container>
        <v-container class="fill-height" :class="sheet2">
          <v-hover v-slot:default="{ hover }">
            <v-card
              :elevation="hover ? 24 : 2"
              class="mx-auto"
              height="400"
              max-width="350"
            >
              <v-img
                src="@/assets/images/block.png"
                height="400"
                max
                width="350"
              >
                <v-container fluid class="pa-10">
                  <v-row>
                    <v-hover v-slot:default="{ hover }">
                      <v-card :elevation="hover ? 24 : 2" class="mb-8">
                        <v-img
                          src="@/assets/images/brainStart.png"
                          @click="$router.push('/users')"
                        />
                      </v-card>
                    </v-hover>
                  </v-row>
                  <v-row>
                    <v-hover v-slot:default="{ hover }">
                      <v-card :elevation="hover ? 24 : 2">
                        <v-img
                          src="@/assets/images/snakeStart.png"
                          @click="$router.push('/games')"
                        />
                      </v-card>
                    </v-hover>
                  </v-row>
                </v-container>
              </v-img>
            </v-card>
          </v-hover>
        </v-container>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
  name: "MainPage",
  data: () => ({
    sheet1: "d-flex",
    sheet2: "d-none",
  }),
  methods: {
    toggleSheet() {
      this.sheet1 = "d-none";
      this.sheet2 = "d-flex";
    },
  },
};
</script>
