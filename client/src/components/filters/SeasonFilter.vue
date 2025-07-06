<script setup lang="ts">
import { seasons } from "@library/utils.js";
import { onMounted, ref } from "vue";

const props = defineProps<{
  onChange: (season: number) => void
}>();

const selectedSeason = ref();

const handleSeasonChange = (season: number) => {
  selectedSeason.value = season;
  props.onChange(season);
}

onMounted(() => {
  const initialSeason = 2025;
  selectedSeason.value = initialSeason;
  props.onChange(initialSeason);
});
</script>

<template>
  <v-card class="season-filter-card" elevation="2">
    <v-card-text>
      <div class="season-filter-grid">
        <v-chip
            :color="selectedSeason === null ? 'primary' : undefined"
            class="season-chip"
            @click="handleSeasonChange(null)"
        >
          ALL
        </v-chip>
        <v-chip
            v-for="season in seasons"
            :key="season"
            :value="season"
            :color="selectedSeason === season ? 'primary' : undefined"
            class="season-chip"
            @click="handleSeasonChange(season)"
        >
          {{ season }}
        </v-chip>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.season-filter-card {
  width: 100%;
}

.season-filter-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.season-chip {
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  font-weight: 500;
  width: 100%;
  justify-content: center;
}

</style>