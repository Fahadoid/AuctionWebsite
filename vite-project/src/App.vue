<script lang="ts" setup>
import * as Api from '@/lib/api';
import { onMounted } from 'vue';

const LOGIN_PATH = '/login';
const LOGOUT_PATH = '/logout';

onMounted(async () => {
  const user = await Api.getCurrentUser();
  const isLoggedIn = user !== null;
  if (!isLoggedIn) {
    window.location.replace(`${Api.HOST}${LOGIN_PATH}`);
  }
});
</script>

<template>
  <header id="nav">
    <div class="nav-link-container">
      <router-link to="/" class="logo">
        fBay
      </router-link>
      <router-link class="nav-link" to="/">List</router-link>
      <router-link class="nav-link" to="/items/new">Create</router-link>
    </div>
    <div class="nav-link-container">
      <router-link class="nav-link" to="/profile">Profile</router-link>
      <a class="nav-link" :href="`${Api.HOST}${LOGOUT_PATH}`">Log out</a>
    </div>
  </header>
  <main>
    <router-view />
  </main>
</template>

<style scoped>
#nav {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1rem;
}

.logo {
  font-weight: bold;
  color: black;
  font-size: 2rem;
  margin-right: 0.5rem;
}

.nav-link-container {
  display: flex;
  align-items: baseline;
  gap: 1rem;
}

.nav-link {
  color: #222;
  font-weight: bold;
}

.nav-link:hover {
  color: #666;
  text-decoration: underline;
}
</style>
