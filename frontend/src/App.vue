<script setup>
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import Taskbar from '@/components/TaskBar.vue'


const authStore = useAuthStore();
</script>

<template>
  <div class="app-container">
    <header class="main-header">
      <h1 class="socdis">SocialDistribution</h1>
    </header>
    <taskbar v-if="authStore.authenticated"/>
    <div class="container pt-4 pb-4">
      <RouterView />
    </div>
  </div>
</template>

<style>
.main-header {
  margin: 1em;
}

.socdis {
  text-align: center;
}
</style>