<script lang="ts" setup>
import { onMounted, ref, Ref } from 'vue';
import * as Api from '@/lib/api';
import { useRouter } from 'vue-router';

const router = useRouter();

const email: Ref<string> = ref('');
const password: Ref<string> = ref('');
const dob: Ref<string> = ref('');
const avatar: Ref<File | null> = ref(null);

onMounted(async () => {
  const user = await Api.getCurrentUser();
  email.value = user.email;
  dob.value = user.dob;
});

async function update() {
  // Don't proceed unless email, password, dob are all present
  if (!(email.value && password.value && dob.value)) {
    return;
  }

  if (avatar.value !== null) {
    await Api.updateCurrentUser({
      email: email.value,
      password: password.value,
      dob: dob.value,
      avatar: avatar.value,
    });
  } else {
    await Api.updateCurrentUser({
      email: email.value,
      password: password.value,
      dob: dob.value,
    });
  }

  router.push(`/profile`);
}

function onAvatarChange(e: Event) {
  if (e.target === null) return;

  const target = e.target as HTMLInputElement;
  const files = target.files;
  if (files === null) return;

  if (files.length === 0) {
    avatar.value = null;
  } else {
    avatar.value = files[0];
  }
}
</script>

<template>
  <form>
    <h3>Change Your profile</h3>
    <label>New email:</label><br>
    <input type="text" v-model="email" required><br>
    <label>New password:</label><br>
    <input type="text" v-model="password" required><br>
    <label>New date of birth</label><br>
    <input type="date" v-model="dob" required><br>
    <label>New image</label><br>
    <input type="file" @change="onAvatarChange" accept="image/*"><br>
    <button type="submit" @click="update">submit</button>
  </form>
</template>
