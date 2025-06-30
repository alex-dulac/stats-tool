<script setup lang="ts">
// https://observablehq.com/@observablehq/plot-radar-chart
// Radar chart to highlight all-around vs. specialized players.
// Axes: goals_per_game, assists_per_game, shots_per_game, toi_per_game
import {computed, ref} from "vue";
import apiClient from "@api/apiClient.ts";

const data = ref();
const loading = ref(true);

const fetchDataAndRefreshChart = async (season: number | null) => {
  loading.value = true
  const response = await apiClient.getTotalPoints(season);
  data.value = response.data;
}
</script>

<template>
  <h2>Per Game Consistency</h2>
  <p>Radar chart to highlight all-around vs. specialized players. Coming soon!</p>
</template>