<script setup lang="ts">
import { useSessionStore } from "@library/store.ts";
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const session = useSessionStore();

const welcome = computed(() => {
  return session.getName ? `Welcome, ${session.getName}` : "Welcome"
});

const pageTitle = computed(() => {
  const titleMap: Record<string, string> = {
    'table': 'Data Grid',
    'points': 'Total Points',
    'heatmap': 'Heatmap',
    'per-game-consistency': 'Per Game Consistency',
    'shooting-efficiency': 'Shooting Efficiency',
    'production': 'Production',
  };

  return titleMap[route.name as string] || '';
});
</script>

<template>
  <v-app-bar>
    <template #prepend>
      <div class="ml-2">Hockey Stats Tool</div>
    </template>

    <v-row justify="center" align="center" class="flex-grow-0">
      <h4>{{ pageTitle }}</h4>
    </v-row>

    <template #append>
      <v-row class="mr-2 align-center">
        <h4 class="mr-2">{{ welcome }}</h4>
        <v-img
            :src="'/logo.svg'"
            height="40"
            width="40"
            class="mr-2"
        ></v-img>
        <v-img
            :src="'/shield.png'"
            height="40"
            width="40"
            class="mr-2"
        ></v-img>
      </v-row>
    </template>
  </v-app-bar>
</template>
