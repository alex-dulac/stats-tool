import axios, { type AxiosResponse } from "axios";
import { mapKeysToCamelCase } from "@library/utils.ts";

export interface FilterParams {
	season: number | null;
	players: string | null;
}

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

function getRequestConfig(params: any) {
	return Object.keys(params).length > 0 ? { params } : undefined;
}

export default {
	getStats: async () => {
		return handleApiResponse(apiClient.get('/stats'));
	},
	getPlayers: async () => {
		return handleApiResponse(apiClient.get('/players'));
	},
	getStatsByPlayerName: async (playerName: string) => {
		return handleApiResponse(apiClient.get(`/stats/${playerName}`));
	},
	getTotalPoints: async (params: FilterParams) => {
		return handleApiResponse(apiClient.get('/charts/total-points', getRequestConfig(params)));
	},
	getProduction: async (params: FilterParams) => {
		return handleApiResponse(apiClient.get('/charts/production', getRequestConfig(params)));
	},
	getShootingEfficiency: async (params: FilterParams) => {
		return handleApiResponse(apiClient.get('/charts/shooting-efficiency', getRequestConfig(params)));
	},
	getPerGameConsistency: async (params: FilterParams) => {
		return handleApiResponse(apiClient.get('/charts/per-game-consistency', getRequestConfig(params)));
	},
	getScoutingHeatmap: async () => {
		return handleApiResponse(apiClient.get('/charts/scouting-heatmap'));
	},
	getHeadToHead: async (params: FilterParams) => {
		return handleApiResponse(apiClient.get('/charts/head-to-head', getRequestConfig(params)));
	},
};
