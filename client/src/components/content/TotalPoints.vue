<script setup lang="ts">
import { computed, ref, watch } from "vue";
import apiClient, { type FilterParams } from "@api/apiClient.ts";
import * as Plot from "@observablehq/plot";
import { useSettingsStore } from "@library/store.ts";
import type { Stat } from "@library/models.ts";
import BaseChart from "@components/BaseChart.vue";

const settingsStore = useSettingsStore();
const data = ref();
const loading = ref(true);
const plot = ref();

const items = computed<[]>(() => {
  return data.value?.data?.flatMap((d: Stat) => [
    {
      playerName: d.playerName,
      team: d.team,
      playerTeam: `${d.playerName} (${d.team})`,
      season: d.season,
      stat: "Goals",
      value: d.goals,
      goals: d.goals,
      assists: d.assists
    },
    {
      playerName: d.playerName,
      team: d.team,
      playerTeam: `${d.playerName} (${d.team})`,
      season: d.season,
      stat: "Assists",
      value: d.assists,
      goals: d.goals,
      assists: d.assists
    }
  ]) || [];
});

const createPlot = () => {
  plot.value = Plot.plot({
    width: 1200,
    height: 800,
    margin: 20,
    x: { label: "Player (Season)", tickRotate: 30 },
    y: { label: "Total Points", grid: true },
    color: { legend: true },
    marks: [
      Plot.barY(items.value, {
        x: d => `${d.playerName} (${d.season})`,
        y: "value",
        fill: "stat",
        order: "stack",
        title: d => `${d.playerName}\nSeason: ${d.season}\nTeam: ${d.team}\nGoals: ${d.goals}\nAssists: ${d.assists}`,
        tip: {
          fill: settingsStore.getChartTipFill,
          textColor: settingsStore.getChartTipTextColor
        }
      }),
      Plot.ruleY([0]),
    ]
  });
};

const fetchData = async (params: FilterParams) => {
  loading.value = true;
  const response = await apiClient.getTotalPoints(params);
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