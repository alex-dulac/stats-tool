<script setup lang="ts">
import { ref, watch } from "vue";
import LoadingCircle from "@components/LoadingCircle.vue";
import SeasonFilter from "@components/filters/SeasonFilter.vue";
import PlayerFilter from "@components/filters/PlayerFilter.vue";
import type { FilterParams } from "@api/apiClient.ts";

const props = defineProps<{
  loading: boolean;
  plot: any;
  showFilters: boolean;
  onChange?: (props: FilterParams) => void,
  additionalStyle?: Element;
}>();

const chartContainer = ref();
const params = ref()

const handleSeasonChange = (season: number | null) => {
  if (props.onChange) {
    params.value = {...params.value, season };
    props.onChange(params.value);
  }
}

const handlePlayerChange = (players: string | null) => {
  if (props.onChange) {
    params.value = {...params.value, players };
    props.onChange(params.value);
  }
}

const updateChart = () => {
  if (chartContainer.value && props.plot) {
    chartContainer.value.innerHTML = '';
    chartContainer.value.appendChild(props.plot);

    if (props.additionalStyle) {
      const existingStyle = chartContainer.value.querySelector('style');
      existingStyle?.remove();
      chartContainer.value.appendChild(props.additionalStyle);
    }
  }
};

watch(() => props.plot, (newPlot) => {
  if (newPlot) {
    updateChart();
  }
}, { immediate: true });
</script>

<template>
  <div class="chart-container">
    <div class="content-layout" :class="{ 'no-filters': !showFilters }">
      <div class="chart-area">
        <LoadingCircle v-if="loading" />
        <div ref="chartContainer" class="chart" />
      </div>
      <div v-show="showFilters" class="filters-container">
        <SeasonFilter :onChange="handleSeasonChange" />
        <PlayerFilter :onChange="handlePlayerChange" />
      </div>
    </div>
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

.content-layout {
  display: flex;
  gap: 10px;
  width: 100%;
}

.content-layout.no-filters {
  justify-content: center;
}

.chart-area {
  flex: 1;
  min-width: 0;
  position: relative;
  overflow: hidden;
  max-width: 100%;
  margin-left: 100px;
}

.no-filters .chart-area {
  max-width: 1200px;
}

.filters-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 250px;
  flex-shrink: 0;
  margin-right: 50px;
}

.chart {
  width: 100%;
  height: 100%;
  overflow: auto;
  padding: 0;
  margin: 0;
}
</style>