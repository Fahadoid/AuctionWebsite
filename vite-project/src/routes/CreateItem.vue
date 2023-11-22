<script lang ="ts" setup>
import { ref, Ref } from "vue";
import { Router, useRouter } from "vue-router";
import * as API from '@/lib/api';

const title: Ref<string> = ref('');
const description: Ref<string> = ref('');
const photo: Ref<File | null> = ref(null);
const startingPrice: Ref<number> = ref(0);
const endDate: Ref<string> = ref('');
const router: Router = useRouter();

async function createItem(e: Event) {
  e.preventDefault();

  const item = await API.createItem({
    title: title.value,
    desc: description.value,
    starting_price: startingPrice.value,
    end_date: endDate.value,
    ...photo.value && { photo: photo.value },
  });

  router.push(`/items/${item.id}`);
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
  <span>
    <form>
      Enter Item Details:
      <br>
      <input name="Title" type="text" placeholder="Item Name" v-model="title" required>
      <br>
      <input name="Description" type="textarea" placeholder="Item Description" v-model="description" required>
      <br>
      <input type="file" @change="onPhotoChange" accept="image/*" required><br>
      <input name="Starting Price" type="number" min="0.01" step="0.01" placeholder="Starting Price"
        v-model="startingPrice" required>
      <br>
      <input name="End Date" type="date" v-model="endDate" required>
      <br>
      <input type="submit" @click="createItem" value="Create">
    </form>
  </span>

</template>
