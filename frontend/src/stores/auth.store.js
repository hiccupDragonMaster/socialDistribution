import { defineStore } from 'pinia';
import { fetchWrapper } from '@/helpers/fetch-wrapper';
import router from '@/router';

const baseUrl = `${import.meta.env.VITE_API_URL}`;

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    credentials: JSON.parse(localStorage.getItem('credentials')),
    returnUrl: null,
    tokenRefreshInterval: null
  }),
  actions: {
    async login(username, password) {
      const credentials = await fetchWrapper.post(`${baseUrl}/api/token/`, { username, password });
      this.credentials = credentials;
      localStorage.setItem('credentials', JSON.stringify(credentials));
      router.push(this.returnUrl || '/');
      this.startTokenRefreshInterval();
    },
    async refreshToken() {
      try {
        const response = await fetchWrapper.post(`${baseUrl}/api/token/refresh/`, {
          refresh: this.credentials.refresh
        });
        this.credentials.access = response.access;
        localStorage.setItem('credentials', JSON.stringify(this.credentials));
      } catch (error) {
        console.error('Error refreshing token:', error);
        this.logout();
      }
    },
    startTokenRefreshInterval() {
      // Clear existing interval if any
      if (this.tokenRefreshInterval) {
        clearInterval(this.tokenRefreshInterval);
      }

      // Set up a new interval
      this.tokenRefreshInterval = setInterval(async () => {
        if (this.isAccessTokenAlmostExpired()) {
          await this.refreshToken();
        }
      }, 60000); // Check every minute
    },
    isAccessTokenAlmostExpired() {
      const accessToken = this.credentials?.access;
      if (!accessToken) return true;

      const payload = JSON.parse(atob(accessToken.split('.')[1]));
      const now = Date.now() / 1000;
      const timeLeft = payload.exp - now;
      return timeLeft < 120; // less than 2 minutes remaining
    },
    logout() {
      this.credentials = null;
      localStorage.removeItem('credentials');
      clearInterval(this.tokenRefreshInterval);
      router.push('/login');
    },
  },
  getters: {
    authenticated(state) {
      return !!state.credentials;
    },
  }
});
