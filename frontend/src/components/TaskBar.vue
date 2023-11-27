<script setup>

import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

const authStore = useAuthStore()
</script>

<template>
  <div class="task_bar">
    <div class="center_nav">
        <router-link class="btn btn-info" :to="{ name: 'search' }">Search</router-link>
        <router-link class="btn btn-info" :to="{ name: 'profile' }">Profile</router-link>
        <router-link class="btn btn-info" role="button" :to="{ name: 'create-post' }">Create a post</router-link>
        <router-link class="btn btn-info" :to="{ name: 'home' }">Home</router-link>
    </div>
    <div class="right_nav">
        <router-link class="btn btn-info" :to="{ name: 'settings' }">Settings</router-link>
        <a @click="authStore.logout()" class="btn btn-info">Logout</a>
    </div>
  </div>
</template>

<style scoped>
.task_bar {
  padding: 0 1em;
  justify-content: flex-start;
  position: relative;
}

.center_nav {
  flex: 0 1 auto;
  position: absolute;
  gap: 0.5em;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-self: center;
}

.right_nav {
  flex: 0 1 auto;
  gap: 0.5em;
  display: flex;
  width: 200px;
  margin-left: auto;
}
</style>
