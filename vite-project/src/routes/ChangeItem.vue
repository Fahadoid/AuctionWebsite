<script lang="ts" setup>
import { useRoute, useRouter } from 'vue-router';
import { onMounted, Ref, ref } from 'vue';
import * as Api from '@/lib/api';

const route = useRoute();
const router = useRouter();
const itemId = typeof route.params.id === 'string' ? parseInt(route.params.id) : parseInt(route.params.id[0]);

const title: Ref<string> = ref('');
const description: Ref<string> = ref('');
const startingPrice: Ref<number> = ref(0);
const photo: Ref<File | null> = ref(null);
const endDate: Ref<string> = ref('');

onMounted(async () => {
  const item = await Api.getItem(itemId);
  title.value = item.title;
  description.value = item.desc;
  startingPrice.value = parseFloat(item.starting_price);
  endDate.value = item.end_date;
});

async function update() {
  await Api.updateItem(itemId, {
    title: title.value,
    desc: description.value,
    starting_price: startingPrice.value,
    end_date: endDate.value,
    ...photo.value && { photo: photo.value },
  });

  router.push(`/items/${itemId}`);
}

function onPhotoChange(e: Event) {
  if (e.target === null) return;

  const target = e.target as HTMLInputElement;
  const files = target.files;
  if (files === null) return;

  if (files.length === 0) {
    photo.value = null;
  } else {
    photo.value = files[0];
  }
}
</script>

<template>
  <form>
    <h3>Change Item</h3>
    <label>Item Name:</label><br>
    <input type="text" v-model="title" required><br>
    <label>Item Description:</label><br>
    <input type="textarea" v-model="description" required><br>
    <label>Picture of item:</label><br>
    <input type="file" @change="onPhotoChange" accept="image/*" required><br>
    <label>Starting Price:</label><br>
    <input type="number" min="0.01" step="0.01" v-model="startingPrice" required><br>
    <label>End Date:</label><br>
    <input type="date" v-model="endDate" required> <br>
    <button type="submit" @click="update">submit</button>
  </form>
</template>
