<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import api from "@api/apiClient.ts";
import LoadingCircle from "@components/LoadingCircle.vue";
import { secondsToMinuteSeconds } from "@library/utils.ts";

const data = ref();
const loading = ref(true);

const items = computed(() => {
  if (!data.value) return [];
  const rawItems = data.value?.data || [];

  return rawItems.map(item => ({
    ...item,
    toi: secondsToMinuteSeconds(item.toi),
    toiPerGame: secondsToMinuteSeconds(item.toiPerGame)
  }));
});

const headers = [
  { title: 'Player', key: 'playerName', width: '200px' },
  { title: 'Team', key: 'team', },
  { title: 'Season', key: 'season' },
  { title: 'GP', key: 'gp' },
  { title: 'TOI', key: 'toi' },
  { title: 'TOI/Game', key: 'toiPerGame' },
  { title: 'Goals', key: 'goals' },
  { title: 'G/Game', key: 'goalsPerGame' },
  { title: 'Assists', key: 'assists' },
  { title: 'A/Game', key: 'assistsPerGame' },
  { title: 'Points', key: 'points' },
  { title: 'P/Game', key: 'pointsPerGame' },
  { title: 'Shots', key: 'shots' },
  { title: 'S/Game', key: 'shotsPerGame' },
  { title: 'Scouting Grade', key: 'scoutingGrade' },
];

const fetchStats = async () => {
  loading.value = true;
  const response = await api.getStats();
  if (response.data) {
    data.value = response.data;
  }
  loading.value = false;
}

onMounted(() => {
  fetchStats();
});
</script>

<template>
    <div>
      <LoadingCircle v-if="loading" />

      <v-data-table
          v-else
          :items="items"
          :headers="headers"
          :loading="loading"
          class="elevation-3"
          fixed-header
      />
    </div>
</template>

