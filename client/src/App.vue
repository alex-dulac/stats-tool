<script setup lang="ts">
import AppBar from "./components/AppBar.vue";
import Sidebar from "./components/Sidebar.vue";
import MainContent from "./components/MainContent.vue";
import {useSessionStore} from "@library/store.ts";
import {useTheme} from "vuetify/framework";
import {onMounted, watch} from "vue";

const session = useSessionStore();
const theme = useTheme();

onMounted(() => {
  theme.global.name.value = session.getTheme;
});

watch(() => session.getTheme, (newTheme: string) => theme.global.name.value = newTheme);
</script>

<template>
  <v-app>
    <AppBar />
    <Sidebar />
    <MainContent />
  </v-app>
</template>