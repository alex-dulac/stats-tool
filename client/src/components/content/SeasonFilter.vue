<script setup lang="ts">
import { seasons } from "@library/utils.js";
import { onMounted, ref } from "vue";

const props = defineProps<{
  onChange: (season: number) => void
}>();

const selectedSeason = ref(2025);

const handleSeasonChange = (season: number) => {
  selectedSeason.value = season;
  props.onChange(season);
}

onMounted(() => {
  const initialSeason = 2025;
  selectedSeason.value = initialSeason;
  props.onChange(initialSeason);
})
</script>

<template>
  <v-chip-group class="season-filter" filter>
    <v-chip
        v-for="season in seasons"
        :key="season"
        class="season-chip"
        :class="{ active: selectedSeason === season }"
        @click="handleSeasonChange(season)"
    >
      {{ season }}
    </v-chip>
  </v-chip-group>
</template>

<style scoped>
.season-filter {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.season-chip {
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  font-weight: 500;
}
</style>