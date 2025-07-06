<script setup lang="ts">
import { useRouter } from "vue-router";
import { mainNavItems, profile } from "@library/navItems.ts";
import { initialSettings, useSettingsStore } from "@library/store.ts";

const router = useRouter();
const settingsStore = useSettingsStore();

const handleLogout = () => {
  // simulate a logout by just clearing the session data
  settingsStore.setSettingsAttributes(initialSettings.name, initialSettings.theme);
};

const handleItemClick = (route: string) => {
  router.push(route);
};

</script>

<template>
  <v-navigation-drawer
      expand-on-hover
      rail
  >
    <v-list nav>
      <v-list-item
          v-for="(item, index) in mainNavItems"
          :key="index"
          :title="item.displayName"
          :prepend-icon="item.icon"
          @click="handleItemClick(item.route)"
          link
      ></v-list-item>
    </v-list>

    <template #append>
      <v-divider class="mb-2"></v-divider>
      <v-list-item
          :title=profile.displayName
          @click="handleItemClick(profile.route)"
          :prepend-icon=profile.icon
          link
      ></v-list-item>
      <v-list-item
          title="Logout"
          @click="handleLogout"
          prepend-icon="mdi-logout"
          link
      ></v-list-item>
    </template>
  </v-navigation-drawer>
</template>