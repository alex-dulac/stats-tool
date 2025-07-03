export const toCamelCase = (str: string): string => {
	return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
};

export const mapKeysToCamelCase = <T>(obj: T): T => {
	if (Array.isArray(obj)) {
		return obj.map(mapKeysToCamelCase) as T;
	}

	if (obj && typeof obj === 'object') {
		return Object.fromEntries(
			Object.entries(obj).map(([key, value]) => [
				toCamelCase(key),
				mapKeysToCamelCase(value)
			])
		) as T;
	}

	return obj;
};

export const seasons = [2019, 2020, 2021, 2022, 2023, 2024, 2025];

export const secondsToMinuteSeconds = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
	const secondsRemaining = Math.floor(seconds % 60);

    return `${minutes.toString().padStart(2, '0')}:${secondsRemaining.toString().padStart(2, '0')}`;
}