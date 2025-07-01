<script setup lang="ts">
// https://observablehq.com/@observablehq/plot-olympians-hexbin

import { computed, onMounted, ref } from "vue";
import apiClient from "@api/apiClient.ts";
import type { Stat } from "@library/models.ts";

const data = ref();
const loading = ref(true);

const items = computed<Stat[]>(() => data.value?.data || []);

const fetchDataAndRefreshChart = async (season: number | null) => {
  loading.value = true
  const response = await apiClient.getTotalPoints(season);
  data.value = response.data;
}

onMounted(() => {
  fetchDataAndRefreshChart(null);
})
</script>

<template>
  <p>{{ items }}</p>
</template>