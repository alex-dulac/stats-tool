<script setup lang="ts">
import { useSettingsStore } from "@library/store.ts";
import { onMounted, ref } from "vue";

const settingsStore = useSettingsStore();

const userName = ref(settingsStore.getName);
const userTheme = ref(settingsStore.getTheme);
const showSuccess = ref(false);

const saveProfile = async () => {
  settingsStore.setSettingsAttributes(userName.value, userTheme.value);
  showSuccess.value = true;
  setTimeout(() => {
    showSuccess.value = false;
  }, 3000);
};

onMounted(() => {
  userName.value = settingsStore.getName;
  userTheme.value = settingsStore.getTheme;
})
</script>

<template>
  <v-container>
    <v-card class="mx-auto pa-4" max-width="600">
      <v-card-title>User Preferences</v-card-title>

      <v-form @submit.prevent="saveProfile">
        <v-text-field
            v-model="userName"
            label="Display Name"
            variant="outlined"
            class="mb-4"
        ></v-text-field>

        <v-select
            v-model="userTheme"
            label="Theme"
            :items="[
            { title: 'Light Theme', value: 'light' },
            { title: 'Dark Theme', value: 'dark' }
          ]"
            item-title="title"
            item-value="value"
            variant="outlined"
            class="mb-4"
        ></v-select>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              color="primary"
              type="submit"
              variant="elevated"
          >
            Save Changes
          </v-btn>
        </v-card-actions>
      </v-form>

      <v-alert
          v-if="showSuccess"
          type="success"
          variant="tonal"
          class="mt-4"
      >
        Profile updated successfully!
      </v-alert>
    </v-card>
  </v-container>
</template>