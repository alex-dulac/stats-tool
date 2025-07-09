import { defineStore } from "pinia";
import { ref } from "vue";
import apiClient, { type FilterParams } from "@api/apiClient.ts";
import type { FilterableChartType } from "@components/BaseChart.vue";

interface PlayersResponse {
	data: string[];
}

export const initialFilters: FilterParams = {
	season: 2025,
	players: null
}

export const initialSettings = {
	name: '',
	theme: 'light',
};

// in a real prod app with user authentication, we would likely use db for storing user data.
// in this example, we're simply using a store that interacts with local storage.
export const useSettingsStore = defineStore('settings', {
	state: () => {
		const savedSettings = localStorage.getItem('stats-user-settings');
		return savedSettings ? JSON.parse(savedSettings) : initialSettings;
	},

	actions: {
		setSettingsAttributes(name: string, theme: 'light' | 'dark') {
			this.name = name;
			this.theme = theme;

			const storageValue = JSON.stringify({
				name: this.name,
				theme: this.theme,
			});
			localStorage.setItem('stats-user-settings', storageValue);
		}
	},

	getters: {
		getName: (state) => state.name,
		getTheme: (state) => state.theme,
		getChartTipFill: (state) => {
			return state.theme === 'dark' ? "#333" : "#fff";
		},
		getChartTipTextColor: (state) => {
			return state.theme === 'dark' ? "#fff" : "#000";
		}
	}
});

export const usePlayersStore = defineStore('players', () => {
	const players = ref<string[]>([]);
	const isLoaded = ref(false);

	const fetchPlayers = async () => {
		// If already loaded, return cached data
		if (isLoaded.value) {
			return players.value;
		}

		const response = await apiClient.getPlayers();

		if (response.data) {
			const responseData = response.data as PlayersResponse;
			players.value = Array.isArray(responseData.data) ? responseData.data : [];
			isLoaded.value = true;
		}

		return players.value;
	};

	const clearCache = () => {
		players.value = [];
		isLoaded.value = false;
	};

	return {
		players,
		isLoaded,
		fetchPlayers,
		clearCache
	};
});

export const useFiltersStore = defineStore('filters', {
	// Allows the user to navigate to different charts and retain the latest filter settings for each one
	state: () => ({
		filters: {
			totalPoints: initialFilters,
			production: initialFilters,
			shootingEfficiency: initialFilters,
			perGameConsistency: initialFilters
		}
	}),

	actions: {
		// This could be managed in other various ways as well
		setFilters(chart: FilterableChartType, filterParams: FilterParams) {
			this.filters[chart] = filterParams;
		},

		getFilters(chart: FilterableChartType): FilterParams {
			return this.filters[chart] || initialFilters;
		},

		clearFilters() {
			this.filters = {
				totalPoints: initialFilters,
				production: initialFilters,
				shootingEfficiency: initialFilters,
				perGameConsistency: initialFilters
			}
		}
	},

	getters: {
		getTotalPointsFilters: (state) => state.filters.totalPoints || {},
		getProductionFilters: (state) => state.filters.production || {},
		getShootingEfficiencyFilters: (state) => state.filters.shootingEfficiency || {},
		getPerGameConsistencyFilters: (state) => state.filters.perGameConsistency || {}
	}
})

