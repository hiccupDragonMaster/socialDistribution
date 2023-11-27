<script setup>
import { ref } from 'vue'

const foundUsers = ref();
</script>

<template>

  <h1>Search for Users</h1>
  <br>
    <input name = "username" type="text" placeholder = "Type here..." >

  <br>
  <div id = 'display_user_search'>
    <div v-if="foundUsers">
      <h4 id="user_title">Users:</h4>
<!--      {% if userlist %}-->
<!--      {% for user in userlist %}-->
      <ul>
      <li style="list-style-type:none">
<!--        <a href="{% url 'project:profile' user.id %}">{{ user.displayName }}</a>-->
      </li>
      </ul>
<!--      {% endfor %}-->
    </div>
  </div>
<!--    {%else%}-->
    <p> There are no matching users, try again.</p>
<!--    {%endif%}-->
</template>

<style scoped>

</style>