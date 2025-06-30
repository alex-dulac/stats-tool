import { defineStore } from "pinia";

export const initialSession = {
	name: '',
    theme: 'light',
};

// in a real prod app with user authentication, we would likely use db for storing user data.
// in this example, we're simply using a store that interacts with local storage.
export const useSessionStore = defineStore('session', {
	state: () => {
		const savedState = localStorage.getItem('stats-user-session');
		return savedState ? JSON.parse(savedState) : initialSession;
	},

	actions: {
		setSessionAttributes(name: string, theme: 'light' | 'dark') {
			this.name = name;
			this.theme = theme;

			const storageValue = JSON.stringify({
				name: this.name,
				theme: this.theme,
			});
			localStorage.setItem('stats-user-session', storageValue);
		}
	},

	getters: {
		getName: (state) => state.name,
		getTheme: (state) => state.theme
	}
});

