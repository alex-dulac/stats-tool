import axios from "axios";
import {handleApiResponse} from "./apiHandler.ts";

const apiClient = axios.create({
	baseURL: import.meta.env.VITE_API_BACKEND_URL || 'http://localhost:8000',
	headers: {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
})

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
	}
};