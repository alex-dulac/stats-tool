<script setup lang="ts">
import { computed, ref } from "vue";
import apiClient from "@api/apiClient.ts";
import * as Plot from "@observablehq/plot";
import LoadingCircle from "@components/LoadingCircle.vue";
import SeasonFilter from "@components/content/SeasonFilter.vue";
import { useSessionStore } from "@library/store.ts";
import type { Stat } from "@library/models.ts";

const sessionStore = useSessionStore();
const data = ref();
const loading = ref(true);
const chartContainer = ref<HTMLDivElement>();

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
        order: "stack",
        title: d => `${d.playerName}\nTeam: ${d.team}\nGoals: ${d.goals}\nAssists: ${d.assists}`,
        tip: {
          fill: sessionStore.getTheme === 'dark' ? "#333" : "#fff",
          textColor: sessionStore.getTheme === 'dark' ? "#fff" : "#000"
        }
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
    <div ref="chartContainer" class="chart" />
  </div>
</template>
