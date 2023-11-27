<script setup>
import { ref } from 'vue';

const title = ref('');
const description = ref('');
const content = ref('');
const categories = ref('');
const visibility = ref('PUBLIC');
const unlisted = ref(false);

const handleSubmit = () => {
  // Handle form submission logic here
  console.log('Form submitted!', { title, description, content, categories, visibility, unlisted });
};
</script>

<template>
  <form @submit.prevent="handleSubmit" method="POST" enctype="multipart/form-data" class="container mt-5">
    <div class="mb-3">
      <label for="id_title" class="form-label">Title:</label>
      <input v-model="title" type="text" class="form-control" name="title" maxlength="50" required id="id_title">
    </div>

    <div class="mb-3">
      <label for="id_description" class="form-label">Description:</label>
      <input v-model="description" type="text" class="form-control" name="description" maxlength="200" required id="id_description">
    </div>

    <div class="mb-3">
      <label for="id_content" class="form-label">Content:</label>
      <textarea v-model="content" class="form-control" name="content" maxlength="600" required id="id_content"></textarea>
    </div>

    <div class="mb-3">
      <label for="id_categories" class="form-label">Categories:</label>
      <input v-model="categories" type="text" class="form-control" name="categories" maxlength="200" required id="id_categories">
    </div>

    <div class="mb-3">
      <label for="id_visibility" class="form-label">Visibility:</label>
      <select v-model="visibility" class="form-select" name="visibility" id="id_visibility">
        <option value="PUBLIC">PUBLIC</option>
        <option value="PRIVATE">PRIVATE</option>
        <option value="FRIENDS_ONLY">FRIENDS_ONLY</option>
      </select>
    </div>

    <div class="mb-3 form-check">
      <input v-model="unlisted" type="checkbox" class="form-check-input" name="unlisted" id="id_unlisted">
      <label class="form-check-label" for="id_unlisted">Unlisted?</label>
    </div>

    <button type="submit" class="btn btn-primary">Create</button>
  </form>
</template>

<style scoped>

</style>