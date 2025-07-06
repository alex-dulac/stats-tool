<script setup lang="ts">
// https://www.washingtonpost.com/news/fancy-stats/wp/2014/07/21/measuring-shot-efficiency-in-nhl-matters-more-than-shot-volume/
// numberOfGoals / numberOfShots

import { computed, ref, watch } from "vue";
import apiClient, { type FilterParams } from "@api/apiClient.ts";
import * as Plot from "@observablehq/plot";
import { useSettingsStore } from "@library/store.ts";
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
      label: "Total Shots",
      nice: true,
      grid: true
    },
    y: {
      label: "Shooting Efficiency (Goals/Shots)",
      grid: true,
      nice: true,
      percent: true
    },
    color: {
      legend: true,
    },
    marks: [
      Plot.dot(items.value, {
        x: "shots",
        y: "shootingEfficiency",
        fill: "team",
        r: 6,
        opacity: 0.8,
        title: d => `${d.playerName} (${d.team})\nSeason: ${d.season}\nShots: ${d.shots}\nGoals: ${d.goals}\nEfficiency: ${(d.shootingEfficiency * 100).toFixed(1)}%`,
        tip: {
          fill: settingsStore.getChartTipFill,
          textColor: settingsStore.getChartTipTextColor
        }
      }),
      Plot.ruleY([0]),
      Plot.frame()
    ]
  });
};

const fetchData = async (params: FilterParams) => {
  loading.value = true
  const response = await apiClient.getShootingEfficiency(params);
  if (response.data) {
    data.value = response.data;
  }
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

