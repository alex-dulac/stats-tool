<script setup lang="ts">
// https://observablehq.com/@observablehq/plot-olympians-hexbin

import { computed, onMounted, ref } from "vue";
import * as Plot from "@observablehq/plot";
import apiClient from "@api/apiClient.ts";
import { useSettingsStore } from "@library/store.ts";
import { seasons } from "@library/utils.ts";
import BaseChart from "@components/BaseChart.vue";

const settingsStore = useSettingsStore();
const data = ref();
const loading = ref(true);
const plot = ref();

const items = computed(() => data.value?.data || []);

const createPlot = () => {
  plot.value = Plot.plot({
    // There is probably a better way to display this data in a more meaningful way to the user,
    // But this seems like an okay starting point for now
    width: 900,
    height: 900,
    x: {
      label: "Season",
      tickFormat: "d",
      ticks: seasons,
      grid: true
    },
    y: {
      label: "Scouting Grade",
      tickFormat: "d",
      ticks: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
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
        stroke: settingsStore.getTheme === 'dark' ? "#666" : "#ccc",
        strokeWidth: 0.5,
        title: d => `Season: ${d.season}\nScouting Grade: ${d.scoutingGrade}\nAvg Points: ${d.averagePoints}`,
        tip: {
          fill: settingsStore.getChartTipFill,
          textColor: settingsStore.getChartTipTextColor
        }
      }),
      Plot.frame()
    ]
  });
}

const fetchData = async () => {
  loading.value = true
  const response = await apiClient.getScoutingHeatmap();
  if (response.data) {
    data.value = response.data;
  }
  createPlot();
  loading.value = false;
}

onMounted(() => {
  fetchData();
})
</script>

<template>
  <BaseChart
      :loading="loading"
      :plot="plot"
      :showFilters="false"
  />
</template>