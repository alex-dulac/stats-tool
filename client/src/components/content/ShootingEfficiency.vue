<script setup lang="ts">
// https://www.washingtonpost.com/news/fancy-stats/wp/2014/07/21/measuring-shot-efficiency-in-nhl-matters-more-than-shot-volume/
// numberOfGoals / numberOfShots

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
const items = computed<Stat[]>(() => data.value?.data || [])

const fetchDataAndRefreshPlot = async (season: number) => {
  loading.value = true
  const response = await apiClient.getShootingEfficiency(season);
  data.value = response.data;

  const plot = Plot.plot({
    width: 1200,
    height: 800,
    margin: 40,
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
        r: d => Math.sqrt(d.goals) * 3, // Size based on goals scored
        opacity: 0.8,
        title: d => `${d.playerName} (${d.team})\nShots: ${d.shots}\nGoals: ${d.goals}\nEfficiency: ${(d.shootingEfficiency * 100).toFixed(1)}%`,
        tip: {
          fill: sessionStore.getTheme === 'dark' ? "#333" : "#fff",
          textColor: sessionStore.getTheme === 'dark' ? "#fff" : "#000"
        }
      }),
      Plot.ruleY([0]),
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
    <div ref="chartContainer" class="chart" />
  </div>
</template>

