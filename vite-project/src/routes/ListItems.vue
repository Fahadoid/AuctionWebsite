<script lang="ts" setup>
import { Ref, ref, onMounted } from 'vue';
import * as Api from '@/lib/api';
import { Item } from '@/lib/api';
import LoadingScreen from '@/components/LoadingScreen.vue';
import DefaultIcon from '@/components/DefaultIcon.vue';

const items: Ref<Item[]> = ref([]);
const finishedLoading: Ref<boolean> = ref(false);

onMounted(async () => {
  items.value = await Api.getItems();
  finishedLoading.value = true;
});

const onSearchChange = (() => {
  let latestPromise: Promise<Item[]> | null = null;

  return async function (e: Event) {
    if (e.target === null) return;

    const target = e.target as HTMLInputElement;
    const search = target.value;
    console.log(`Start request:  ${search}`);
    const newItemsPromise = Api.getItems(search);
    latestPromise = newItemsPromise;

    // Wait for request to complete
    const newItems = await newItemsPromise;
    console.log(`Finish request: ${search}`);

    // Only proceed if the latest promise is this promise
    if (newItemsPromise === latestPromise) {
      console.log(`Updating with:  ${search}`);
      items.value = newItems;
    }
  };
})();
</script>

<template>
  <div id="search-container">
    <label for="search">Search:</label>
    <input id="search" type="text" @input="onSearchChange">
  </div>
  <ul v-if="finishedLoading">
    <li class="item" :class="i.has_ended ? 'ended' : null" v-for="i in items">
      <router-link :to="`/items/${i.id}`">
        <DefaultIcon class="photo" :obj="i" attr="photo_path" :alt="i.title" />
      </router-link>
      <div class="details">
        <div>
          <span class="price">£{{ i.current_price }}</span>
          <router-link class="title" :to="`/items/${i.id}`">{{ i.title }}</router-link>
        </div>
        <span class="description" :to="`/items/${i.id}`">{{ i.desc }}</span>
        {{ i.has_ended ? 'Ended at: ' : 'Ends at: ' }}
        {{ i.end_date }}
      </div>
    </li>
    <p v-if="items.length === 0" class="no-items-msg">
      No items on auction!
    </p>
  </ul>
  <LoadingScreen v-else />
</template>

<style scoped>
#search-container {
  display: flex;
  flex-direction: row;
  gap: 1rem;
}

#search {
  display: block;
  flex-grow: 1;
}

.item {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  margin-bottom: 1rem;
}

.photo {
  display: block;
  width: 6rem;
  height: 6rem;
  border: black solid 1px;
  object-fit: cover;
}

.details {
  display: flex;
  flex-grow: 1;
  justify-content: center;
  flex-direction: column;
}

.title {
  color: black;
}

.title:hover {
  color: black;
  text-decoration: underline;
}

.ended .title {
  color: #333;
  font-style: italic;
  text-decoration: line-through;
}

.ended .title:hover {
  color: #333;
  text-decoration: line-through underline;
}

.price {
  float: right;
}

.no-items-msg {
  text-align: center;
}
</style>
