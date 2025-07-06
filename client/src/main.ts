import { createApp } from 'vue';
import App from './App.vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import 'vuetify/lib/styles/main.css';
import { createPinia } from "pinia";
import { aliases, mdi } from 'vuetify/iconsets/mdi';
import '@mdi/font/css/materialdesignicons.css'
import { router } from "./library/router.ts";

const vuetify = createVuetify({
	components,
	directives,
	icons: {
		defaultSet: 'mdi',
		aliases,
		sets: {
			mdi,
		},
	},
});

createApp(App)
	.use(router)
	.use(vuetify)
	.use(createPinia())
	.mount('#app');
