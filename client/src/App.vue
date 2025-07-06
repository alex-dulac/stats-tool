<script setup lang="ts">
import AppBar from "./components/AppBar.vue";
import Sidebar from "./components/Sidebar.vue";
import MainContent from "./components/MainContent.vue";
import { useSettingsStore } from "@library/store.ts";
import { useTheme } from "vuetify/framework";
import { onMounted, watch } from "vue";

const session = useSettingsStore();
const theme = useTheme();

onMounted(() => {
  theme.change(session.getTheme);
});

watch(() => session.getTheme, (newTheme: string) => theme.change(newTheme));
</script>

<template>
  <v-app>
    <AppBar />
    <Sidebar />
    <MainContent />
  </v-app>
</template>