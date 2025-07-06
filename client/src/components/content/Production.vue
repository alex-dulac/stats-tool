<script setup lang="ts">
import { computed, ref, watch } from "vue";
import apiClient, { type FilterParams } from "@api/apiClient.ts";
import * as Plot from "@observablehq/plot";
import { useSettingsStore } from "@library/store.ts";
import { secondsToMinuteSeconds } from "@library/utils.ts";
import BaseChart from "@components/BaseChart.vue";

const settingsStore = useSettingsStore();
const data = ref();
const loading = ref(true);
const items = computed(() => data.value?.data || []);
const plot = ref();

const createPlot = () => {
  plot.value = Plot.plot({
    width: 1200,
    height: 800,
    margin: 30,
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
        title: d => `${d.playerName} (${d.team})\nSeason: ${d.season}\nTOI/Game: ${secondsToMinuteSeconds(d.toiPerGame)}\nPoints/Game: ${d.pointsPerGame}`,
        tip: {
          fill: settingsStore.getChartTipFill,
          textColor: settingsStore.getChartTipTextColor
        }
      }),
      Plot.frame()
    ]
  });
};

const fetchData = async (params: FilterParams) => {
  loading.value = true
  const response = await apiClient.getProduction(params);
  data.value = response.data;
  loading.value = false;
};

watch(items, () => {
  if (items.value) {
    createPlot();
  }
}, { immediate: true });
</script>

<template>
  <BaseChart
      :loading="loading"
      :onChange="fetchData"
      :plot="plot"
      :showFilters="true"
  />
</template>

