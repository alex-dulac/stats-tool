<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import LoadingCircle from "@components/LoadingCircle.vue";
import SeasonFilter from "@components/filters/SeasonFilter.vue";
import PlayerFilter from "@components/filters/PlayerFilter.vue";
import type { FilterParams } from "@api/apiClient.ts";
import { useFiltersStore } from "@library/store.ts";

export type FilterableChartType =
    'totalPoints' |
    'production' |
    'shootingEfficiency' |
    'perGameConsistency' |
    'headToHead';

const props = defineProps<{
  loading: boolean;
  plot: any;
  showFilters: boolean;
  chartType?: FilterableChartType | undefined;
  onChange?: (props: FilterParams) => void,
  additionalStyle?: Element;
}>();

const filtersStore = useFiltersStore();
const chartContainer = ref();

const handleFiltersChange = (updatedFilters: FilterParams) => {
  props.onChange?.(updatedFilters);
}

watch(() => props.plot, (newPlot) => {
  if (chartContainer.value) {
    chartContainer.value.innerHTML = '';
    if (newPlot) {
      chartContainer.value.appendChild(newPlot);
    }

    if (props.additionalStyle) {
      const existingStyle = chartContainer.value.querySelector('style');
      existingStyle?.remove();
      chartContainer.value.appendChild(props.additionalStyle);
    }
  }
}, { immediate: true });

onMounted(() => {
  if (props.chartType && props.onChange) {
    const storedFilters = filtersStore.getFilters(props.chartType);
    props.onChange(storedFilters);
  }
});
</script>

<template>
  <!-- Layout with filters -->
  <div v-if="showFilters && chartType" class="chart-container-with-filters">
    <div class="chart-area">
      <LoadingCircle v-if="loading" />
      <div ref="chartContainer" class="chart" />
    </div>

    <aside class="filters-sidebar">
      <SeasonFilter
          :onChange="handleFiltersChange"
          :chartType="chartType"
      />
      <PlayerFilter
          :onChange="handleFiltersChange"
          :chartType="chartType"
      />
    </aside>
  </div>

  <!-- Layout without filters (centered) -->
  <div v-else class="chart-container-centered">
    <div class="chart-area-centered">
      <LoadingCircle v-if="loading" />
      <div ref="chartContainer" class="chart" />
    </div>
  </div>
</template>

<style scoped>
.chart-container-with-filters {
  display: flex;
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.chart-area {
  flex: 1;
  min-width: 0;
  position: relative;
  overflow: hidden;
}

.filters-sidebar {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 250px;
  flex-shrink: 0;
}

.chart-container-centered {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.chart-area-centered {
  position: relative;
  overflow: hidden;
}

.chart {
  width: 100%;
  height: 100%;
  overflow: auto;
}
</style>