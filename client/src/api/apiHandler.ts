import { mapKeysToCamelCase } from '@library/utils';
import type { AxiosResponse } from "axios";

interface Response<T> {
	data: T | null;
	error: string | null;
	isLoading: boolean;
}

export async function handleApiResponse<T>(apiCall: Promise<AxiosResponse>): Promise<Response<T>> {
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