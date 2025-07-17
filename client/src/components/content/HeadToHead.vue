<script setup lang="ts">
import { computed, ref, watch } from "vue";
import apiClient, { type FilterParams } from "@api/apiClient.ts";
import * as Plot from "@observablehq/plot";
import { useSettingsStore } from "@library/store.ts";
import BaseChart from "@components/BaseChart.vue";

const settingsStore = useSettingsStore();
const data = ref();
const loading = ref(false);
const error = ref();
const items = computed(() => data.value?.data || []);
const plot = ref();

const createPlot = () => {
  if (!items.value || !items.value.player1 || !items.value.player2) {
    return;
  }

  const { player1, player2 } = items.value;

  const comparisonData = [
    { metric: "Total Points", value: player1.totalPoints, player: player1.name },
    { metric: "Total Points", value: player2.totalPoints, player: player2.name },
    { metric: "Points Per Game", value: player1.pointsPerGame, player: player1.name },
    { metric: "Points Per Game", value: player2.pointsPerGame, player: player2.name },
    { metric: "Total Goals", value: player1.totalGoals, player: player1.name },
    { metric: "Total Goals", value: player2.totalGoals, player: player2.name },
    { metric: "Total Assists", value: player1.totalAssists, player: player1.name },
    { metric: "Total Assists", value: player2.totalAssists, player: player2.name },
    { metric: "Shooting %", value: player1.shootingPercentage, player: player1.name },
    { metric: "Shooting %", value: player2.shootingPercentage, player: player2.name }
  ];

  plot.value = Plot.plot({
    width: 1200,
    height: 800,
    margin: 30,
    grid: true,
    x: {
      label: "Value",
      nice: true,
      grid: true
    },
    y: {
      label: "Metric",
      grid: true
    },
    color: {
      legend: true,
      domain: [player1.name, player2.name],
      range: ["#2196F3", "#FF9800"]
    },
    marks: [
      Plot.barX(comparisonData, {
        x: "value",
        y: "metric",
        fill: "player",
        opacity: 0.8,
        title: d => `${d.player}\n${d.metric}: ${d.value}`,
        tip: {
          fill: settingsStore.getChartTipFill,
          textColor: settingsStore.getChartTipTextColor
        }
      }),
      Plot.ruleX([0]),
      Plot.frame(),
    ]
  });
};

const fetchData = async (params: FilterParams) => {
  const players = params.players?.split("|");
  if (!players || players.length != 2) {
    data.value = null;
    plot.value = null;
    return;
  }

  loading.value = true;
  error.value = null;

  const response = await apiClient.getHeadToHead(params);

  if (response.error) {
    error.value = response.error;
    data.value = null;
    plot.value = null;
  } else {
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
  <v-container v-if="error" class="header">
    <p class="text-h6">
      Data not available for the current selection.
    </p>
  </v-container>

  <v-container v-if="!plot && !error" class="header">
    <p class="text-h6">
      Please select two players to compare.
    </p>
  </v-container>

  <v-container v-if="plot" class="header">
    <p class="text-h6">
      {{ items.player1.name }} vs {{ items.player2.name }}
      <br>
      Winner: {{ items.overallWinner }}
    </p>
  </v-container>

  <BaseChart
      :loading="loading"
      :onChange="fetchData"
      :plot="plot"
      :showFilters="true"
      :chartType="'headToHead'"
  />
</template>

<style scoped>
.header {
  font-weight: bold;
  margin-top: 40px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>