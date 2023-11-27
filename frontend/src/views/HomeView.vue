<script setup>
import Inbox from '@/components/Inbox.vue'
import Feed from '@/components/Feed.vue'
</script>

<template>
  <div>
    <div class="user-profile">
      <img src="" alt="User image">
      <div class="user-details">
        <h2 id="stream-name">sashreek</h2>
        <p>Welcome to SocialDistribution! Make posts, explore other user profiles, and make friends.</p>
        <button>Settings</button>
      </div>
    </div>
    <feed/>
    <inbox/>
  </div>
</template>