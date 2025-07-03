import axios, { type AxiosResponse } from "axios";
import { mapKeysToCamelCase } from "@library/utils.ts";

interface Response<T> {
	data: T | null;
	error: string | null;
	isLoading: boolean;
}

const apiClient = axios.create({
	baseURL: import.meta.env.VITE_API_BACKEND_URL || 'http://localhost:8000',
	headers: {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
});

async function handleApiResponse<T>(apiCall: Promise<AxiosResponse>): Promise<Response<T>> {
	const response: Response<T> = {
		data: null,
		error: null,
		isLoading: true
	};

	try {
		const result = await apiCall;
		response.data = mapKeysToCamelCase(result.data) as T;
		response.isLoading = false;
		return response;
	} catch (error: any) {
		response.isLoading = false;
		response.error = error.response?.data?.message || error.message || 'An error occurred with the API request';
		console.error('API Error:', error.response?.data || error.message);
		return response;
	}
}

export default {
	getStats: async () => {
		return handleApiResponse(apiClient.get('/stats'));
	},
	getStatsByPlayerName: async (playerName: string) => {
		return handleApiResponse(apiClient.get(`/stats/${playerName}`));
	},
	getTotalPoints: async (season: number | null = null) => {
		const config = season ? { params: { season } } : undefined;
		return handleApiResponse(apiClient.get('/charts/total-points', config));
	},
	getProduction: async (season: number | null = null) => {
		const config = season ? { params: { season } } : undefined;
		return handleApiResponse(apiClient.get('/charts/production', config));
	},
	getShootingEfficiency: async (season: number | null = null) => {
		const config = season ? { params: { season } } : undefined;
		return handleApiResponse(apiClient.get('/charts/shooting-efficiency', config));
	},
	getPerGameConsistency: async (season: number | null = null) => {
		const config = season ? { params: { season } } : undefined;
		return handleApiResponse(apiClient.get('/charts/per-game-consistency', config));
	},
	getScoutingHeatmap: async () => {
		return handleApiResponse(apiClient.get('/charts/scouting-heatmap'));
	},
};
