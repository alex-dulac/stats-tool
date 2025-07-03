import { ref } from "vue";

export interface NavItem {
	displayName: string;
	route: string;
	icon: string;
	description: string;
}

export const totalPoints: NavItem = {
	displayName: 'Total Points',
	route: 'total-points',
	icon: 'mdi-chart-bar',
	description: 'Total points scored by each player in a specific season, broken down by Goals and Assists.'
};

export const scoutingHeatmap: NavItem = {
	displayName: 'Scouting Heatmap',
	route: 'scouting-heatmap',
	icon: 'mdi-fire-circle',
	description: 'Compare scouting grades against average points over time.'
};

export const perGameConsistency: NavItem = {
	displayName: 'Per Game Consistency',
	route: 'per-game-consistency',
	icon: 'mdi-hockey-sticks',
	description: 'Radar chart showing average consistency metrics for each player in a specific season.'
};

export const shootingEfficiency: NavItem = {
	displayName: 'Shooting Efficiency',
	route: 'shooting-efficiency',
	icon: 'mdi-hockey-puck',
	description: 'Compare shooting efficiency against total shots for each player in a specific season.'
};

export const production: NavItem = {
	route: 'production',
	displayName: 'Production',
	icon: 'mdi-account-hard-hat',
	description: 'View Points per game compared to TOI per game for each player in a specific season.'
};

export const dataGrid: NavItem = {
	route: 'data-grid',
	displayName: 'Data Grid',
	icon: 'mdi-table',
	description: 'A grid of raw player statistics.'
};

export const profile: NavItem = {
	route: 'profile',
	displayName: 'Profile',
	icon: 'mdi-cog',
	description: ''
};

export const mainNavItems = ref<NavItem[]>([
	dataGrid,
	totalPoints,
	production,
	shootingEfficiency,
	perGameConsistency,
	scoutingHeatmap,
]);

