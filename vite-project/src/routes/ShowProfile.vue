<script lang="ts" setup>
import { Ref, ref, onMounted } from 'vue';
import { User, } from '@/lib/api';
import * as Api from '@/lib/api';
import LoadingScreen from '@/components/LoadingScreen.vue';
import DefaultIcon from '@/components/DefaultIcon.vue';

const currentUser: Ref<User | null> = ref(null);

onMounted(async () => {
  currentUser.value = await Api.getCurrentUser();
});
</script>

<template>
  <div v-if="currentUser !== null">
    <DefaultIcon class="photo" :obj="currentUser" attr="avatar_path" :alt="currentUser.email" />
    <router-link class="float-button" :to="`/profile/${currentUser.id}`">Edit Profile</router-link>
    <h3>Your Profile</h3>
    <ul>
      <li>Email: {{ currentUser.email }}</li>
      <li>Date of birth: {{ currentUser.dob }}</li>
    </ul>
  </div>
  <LoadingScreen v-else />
</template>

<style scoped>
.photo {
  float: right;
  width: 12rem;
  height: 12rem;
  border: black solid 1px;
  object-fit: cover;
}

.float-button {
  float: right;
  margin-right: 1rem
}
</style>
