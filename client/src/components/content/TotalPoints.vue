<script setup lang="ts">
import {computed, ref} from "vue";
import apiClient from "@api/apiClient.ts";
import * as Plot from "@observablehq/plot";
import LoadingCircle from "@components/LoadingCircle.vue";
import SeasonFilter from "@components/content/SeasonFilter.vue";

const data = ref();
const loading = ref(true);
const chartContainer = ref(null);

const items = computed<[]>(() => {
  return data.value?.data?.flatMap(d => [
    { playerName: d.playerName, season: d.season, stat: "Goals", value: d.goals },
    { playerName: d.playerName, season: d.season, stat: "Assists", value: d.assists }
  ]) || [];
});

const fetchDataAndRefreshPlot = async (season: number) => {
  loading.value = true
  const response = await apiClient.getTotalPoints(season);
  data.value = response.data;

  const plot = Plot.plot({
    width: 1200,
    height: 800,
    margin: 40,
    x: { label: "Player", tickRotate: 30 },
    y: { label: "Total Points", grid: true },
    fx: { label: "Season" },
    color: { legend: true },
    marks: [
      Plot.barY(items.value, {
        x: "playerName",
        y: "value",
        fill: "stat",
        fx: "season",
        order: "stack"
      }),
      Plot.ruleY([0]),
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