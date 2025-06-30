import { ref } from "vue";

export interface NavItem {
	displayName: string;
	route: string;
	icon: string;
}

export const totalPoints: NavItem = {
	displayName: 'Total Points',
	route: 'total-points',
	icon: 'mdi-chart-bar'
};

// tbd
export const heatmap: NavItem = {
	displayName: 'Heatmap',
	route: 'heatmap',
	icon: 'mdi-fire-circle'
};

export const perGameConsistency: NavItem = {
	displayName: 'Per Game Consistency',
	route: 'per-game-consistency',
	icon: 'mdi-hockey-sticks'
};

export const shootingEfficiency: NavItem = {
	displayName: 'Shooting Efficiency',
	route: 'shooting-efficiency',
	icon: 'mdi-hockey-puck'
};

export const production: NavItem = {
	route: 'production',
	displayName: 'Production',
	icon: 'mdi-account-hard-hat'
};

export const dataGrid: NavItem = {
	route: 'data-grid',
	displayName: 'Data Grid',
	icon: 'mdi-table'
};

export const profile: NavItem = {
	route: 'profile',
	displayName: 'Profile',
	icon: 'mdi-cog'
};

export const mainNavItems = ref<NavItem[]>([
	dataGrid,
	totalPoints,
	production,
	shootingEfficiency,
	perGameConsistency,
]);

