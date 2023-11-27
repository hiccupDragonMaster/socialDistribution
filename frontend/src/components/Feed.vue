<script setup>
import Post from '@/components/Post.vue'
import { ref } from 'vue'

const posts = ref([]);
</script>

<template>
  <div class="feed">
    <div v-if="posts">
      <post :post="post" :key="post.id" v-for="post in posts"/>
    </div>
    <div v-else>
      <p>There is no activity in your feed...</p>
    </div>
  </div>
</template>

<style scoped>

</style>