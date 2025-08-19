<script setup lang="ts">
import { useSettingsStore } from "@library/store.ts";
import { computed } from "vue";
import { useRoute } from "vue-router";
import { mainNavItems } from "@library/navItems.ts";

const route = useRoute();
const session = useSettingsStore();

const welcome = computed(() => {
  return session.getName ? `Welcome, ${session.getName}` : "Welcome"
});

const pageTitle = computed(() => {
  const currentItem = mainNavItems.value.find(item => item.route === route.name);
  return currentItem?.displayName || '';
});

const chartDescription = computed(() => {
  const currentItem = mainNavItems.value.find(item => item.route === route.name);
  return currentItem?.description || '';
});
</script>

<template>
  <v-app-bar>
    <template #prepend>
      <div class="ml-2">Hockey Stats Tool</div>
    </template>

    <v-row justify="center" align="center" class="flex-grow-0">
      <h4>{{ pageTitle }}</h4>

      <v-tooltip v-if="pageTitle" location="right">
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-icon>
              mdi-information-outline
            </v-icon>
          </v-btn>
        </template>
        <span>{{ chartDescription }}</span>
      </v-tooltip>
    </v-row>

    <template #append>
      <v-row class="mr-2 align-center">
        <h4 class="mr-2">{{ welcome }}</h4>
        <v-img
            :src="'/logo.png'"
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
