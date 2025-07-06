import { createRouter, createWebHistory } from 'vue-router';

const routes = [
	{
		path: '/',
		redirect: '/data-table'
	},
	{
		path: '/data-table',
		name: 'data-table',
		component: () => import('@components/content/DataTable.vue'),
		meta: {
			requiresAuth: false, //note: set all routes to true if we had a login system, but we don't!
		},
	},
	{
		path: '/total-points',
		name: 'total-points',
		component: () => import('@components/content/TotalPoints.vue'),
	},
	{
		path: '/per-game-consistency',
		name: 'per-game-consistency',
		component: () => import('@components/content/PerGameConsistency.vue'),
	},
	{
		path: '/shooting-efficiency',
		name: 'shooting-efficiency',
		component: () => import('@components/content/ShootingEfficiency.vue'),
	},
	{
		path: '/production',
		name: 'production',
		component: () => import('@components/content/Production.vue'),
	},
	{
		path: '/scouting-heatmap',
		name: 'scouting-heatmap',
		component: () => import('@components/content/ScoutingHeatmap.vue'),
	},
	{
		path: '/profile',
		name: 'profile',
		component: () => import('@components/content/Profile.vue'),
	},
	{
		// catch-all
		path: '/:pathMatch(.*)*',
		redirect: '/'
	},
];

export const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: routes
});

router.beforeEach(async (to, from, next) => {
	// here we could check if the user is authenticated before allowing navigation
	next();
});
