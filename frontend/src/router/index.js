import { createRouter, createWebHistory } from 'vue-router';

import { useAuthStore } from '@/stores/auth.store'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import UserSearch from '@/views/UserSearch.vue'
import ProfileView from '@/views/ProfileView.vue'
import PostCreateView from '@/views/PostCreateView.vue'

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: 'active',
  routes: [
    { path: '/', component: HomeView, name: "home" },
    { path: '/login', component: LoginView, name: "login" },
    { path: '/search', component: UserSearch, name: "search" },
    { path: '/profile', component: ProfileView, name: "profile" },
    { path: '/create-post', component: PostCreateView, name: "create-post" },
    { path: '/settings', component: HomeView, name: "settings" },
  ]
});

router.beforeEach(async (to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const auth = useAuthStore(  );

  // if (authRequired && !auth.authenticated) {
  //   auth.returnUrl = to.fullPath;
  //   next('/login');
  // } else {
  //   next();
  // }

  next();
});

export default router
