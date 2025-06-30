<script setup lang="ts">
import { computed, ref } from "vue";
import apiClient from "@api/apiClient.ts";
import * as Plot from "@observablehq/plot";
import LoadingCircle from "@components/LoadingCircle.vue";
import SeasonFilter from "@components/content/SeasonFilter.vue";

const data = ref();
const loading = ref(true);
const chartContainer = ref(null);
const items = computed(() => data.value?.data || [])

const fetchDataAndRefreshPlot = async (season: number) => {
  loading.value = true
  const response = await apiClient.getProduction(season);
  data.value = response.data;

  const plot = Plot.plot({
    width: 1200,
    height: 800,
    margin: 40,
    grid: true,
    x: {
      label: "Time on Ice per Game (seconds)",
      nice: true,
      grid: true
    },
    y: {
      label: "Points per Game",
      grid: true,
      nice: true
    },
    color: {
      legend: true,
      scheme: "tableau10"
    },
    marks: [
      Plot.dot(items.value, {
        x: "toiPerGame",
        y: "pointsPerGame",
        fill: "team",
        r: 6,
        opacity: 0.8,
        title: d => `${d.playerName} (${d.team})\nTOI/Game: ${d.toiPerGame} sec\nPoints/Game: ${d.pointsPerGame}`
      }),
      Plot.frame()
    ]
  });

  chartContainer.value.innerHTML = '';
  chartContainer.value.appendChild(plot);
  loading.value = false;
};
</script>

<template>
  <div class="chart-container">
    <SeasonFilter :onChange="fetchDataAndRefreshPlot" />
    <LoadingCircle v-if="loading" />
    <div ref="chartContainer" class="chart"></div>
  </div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.chart {
  width: 100%;
  min-height: 800px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>