<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { useFiltersStore, usePlayersStore } from "@library/store.ts";
import type { FilterableChartType } from "@components/BaseChart.vue";
import type { FilterParams } from "@api/apiClient.ts";

const props = defineProps<{
  onChange: (updatedFilters: FilterParams) => void;
  chartType: FilterableChartType;
}>();

const filtersStore = useFiltersStore();
const playersStore = usePlayersStore();
const selectedPlayers = ref<string[]>([]);
const allPlayers = computed(() => playersStore.players);

const handlePlayerChange = () => {
  const updatedValue = selectedPlayers.value.length > 0 ? selectedPlayers.value.join('|') : null;
  const currentFilters = filtersStore.getFilters(props.chartType);
  const updatedFilters = { ...currentFilters, players: updatedValue };
  filtersStore.setFilters(props.chartType, updatedFilters);
  props.onChange(updatedFilters);
}

const clearAll = () => {
  selectedPlayers.value = [];
  handlePlayerChange();
};

const isPlayerSelected = (player: string) => {
  return selectedPlayers.value.includes(player);
};

const togglePlayerSelection = (player: string) => {
  const index = selectedPlayers.value.indexOf(player);
  if (index === -1) {
    selectedPlayers.value.push(player);
  } else {
    selectedPlayers.value.splice(index, 1);
  }
  handlePlayerChange();
};

onMounted(async () => {
  await playersStore.fetchPlayers();
  const currentSelectedPlayers = filtersStore.getFilters(props.chartType).players;
  if (currentSelectedPlayers) {
    selectedPlayers.value = currentSelectedPlayers.split('|');
  }
});
</script>

<template>
  <v-card class="player-filter" elevation="2">
    <v-card-text>
      <div class="mb-3">
        <v-btn
            size="small"
            variant="outlined"
            @click="clearAll"
        >
          Clear All
        </v-btn>
      </div>

      <div class="player-list">
        <div v-for="player in allPlayers" :key="player" class="player-checkbox">
          <v-checkbox
              :model-value="isPlayerSelected(player)"
              @update:model-value="togglePlayerSelection(player)"
              :label="player"
              density="compact"
              hide-details
          />
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.player-filter {
  width: 100%;
}

.player-list {
  max-height: 350px;
  overflow-y: auto;
  padding-right: 5px;
}

.player-checkbox {
  margin-bottom: 2px;
}
</style>