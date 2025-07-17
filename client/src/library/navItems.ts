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

export const dataTable: NavItem = {
	route: 'data-table',
	displayName: 'Data Table',
	icon: 'mdi-table',
	description: 'A table of player statistics by season.'
};

export const headToHead: NavItem = {
	route: 'head-to-head',
	displayName: 'Head To Head',
	icon: 'mdi-fencing',
	description: 'Analyze two players against each other.'
};

export const profile: NavItem = {
	route: 'profile',
	displayName: 'Profile',
	icon: 'mdi-cog',
	description: ''
};

export const mainNavItems = ref<NavItem[]>([
	dataTable,
	totalPoints,
	production,
	shootingEfficiency,
	perGameConsistency,
	scoutingHeatmap,
	headToHead,
]);

