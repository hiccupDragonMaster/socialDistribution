<script setup>
// TODO: Write form data and submission
</script>

<template>
  <div class="signup-prompts">
    <h2>Sign up</h2>
    <form method="post">
<!--      {{ form.as_p }}-->
      <button type="submit">Sign Up</button>
    </form>
    <h4>Already have an account?</h4>
    <a href="{% url 'login' %}">Log In</a>
  </div>
</template>

<style scoped>

</style>