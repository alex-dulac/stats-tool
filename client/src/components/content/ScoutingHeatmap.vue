<script setup lang="ts">
// https://observablehq.com/@observablehq/plot-olympians-hexbin

import { computed, onMounted, ref } from "vue";
import * as Plot from "@observablehq/plot";
import apiClient from "@api/apiClient.ts";
import { useSessionStore } from "@library/store.ts";
import LoadingCircle from "@components/LoadingCircle.vue";
import { seasons } from "@library/utils.ts";

const sessionStore = useSessionStore();
const data = ref();
const chartContainer = ref();
const loading = ref(true);

const items = computed(() => data.value?.data || []);

const fetchDataAndRefreshPlot = async () => {
  loading.value = true
  const response = await apiClient.getScoutingHeatmap();
  data.value = response.data;

  const plot = Plot.plot({
    // There is probably a better way to display this data in a more meaningful way to the user,
    // But this seems like an okay starting point for now
    width: 1000,
    height: 1000,
    margin: 60,
    x: {
      label: "Season",
      tickFormat: "d",
      ticks: seasons,
      grid: true
    },
    y: {
      label: "Scouting Grade",
      domain: [1, 10],
      grid: true
    },
    color: {
      type: "linear",
      scheme: "cividis",
      label: "Average Points",
      legend: true
    },
    marks: [
      Plot.hexagon(items.value, {
        x: "season",
        y: "scoutingGrade",
        fill: "averagePoints",
        r: 8,
        stroke: sessionStore.getTheme === 'dark' ? "#666" : "#ccc",
        strokeWidth: 0.5,
        title: d => `Season: ${d.season}\nScouting Grade: ${d.scoutingGrade}\nAvg Points: ${d.averagePoints}`,
        tip: {
          fill: sessionStore.getTheme === 'dark' ? "#333" : "#fff",
          textColor: sessionStore.getTheme === 'dark' ? "#fff" : "#000"
        }
      }),
      Plot.frame()
    ]
  });

  chartContainer.value.innerHTML = '';
  chartContainer.value.appendChild(plot);
  loading.value = false;
}

onMounted(() => {
  fetchDataAndRefreshPlot();
})
</script>

<template>
  <div class="chart-container">
    <LoadingCircle v-if="loading" />
    <div ref="chartContainer" class="chart" />
  </div>
</template>