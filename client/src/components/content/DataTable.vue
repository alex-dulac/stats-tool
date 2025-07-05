<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import api from "@api/apiClient.ts";
import LoadingCircle from "@components/LoadingCircle.vue";
import { secondsToMinuteSeconds } from "@library/utils.ts";

const data = ref();
const loading = ref(true);
const search = ref('')

const items = computed(() => data.value?.data || []);

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

      <v-text-field
          v-else
          v-model="search"
          label="Search by player or team"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          hide-details
          single-line
      ></v-text-field>

      <v-data-table
          :items="items"
          :headers="headers"
          :loading="loading"
          v-model:search="search"
          :filter-keys="['playerName', 'team']"
          class="elevation-3"
          fixed-header
          multi-sort
      >
        <!--
          Behind the scenes, toi is sorted by seconds,
          but it should display as "MM:SS" in the table.
        -->
        <template v-slot:item.toi="{ item }">
          {{ secondsToMinuteSeconds(item.toi) }}
        </template>
        <template v-slot:item.toiPerGame="{ item }">
          {{ secondsToMinuteSeconds(item.toiPerGame) }}
        </template>
      </v-data-table>
    </div>
</template>

