<template>
  <div class="loading-center">
    <v-progress-circular
        size="200"
        indeterminate>
    </v-progress-circular>
  </div>
</template>

<style scoped>
.loading-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
