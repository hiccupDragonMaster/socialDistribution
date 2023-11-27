<script setup>

import FriendRequest from '@/components/FriendRequest.vue'
import { ref } from 'vue'

const friend_requests = ref([]);
</script>

<template>
  <h2>Inbox</h2>
  <!-- Friend request processing -->
  <h3>Friend Requests</h3>
  <ul>
    <friend-request :request="fr" :key="fr.id" v-for="fr in friend_requests"/>
  </ul>
</template>

<style scoped>

</style>