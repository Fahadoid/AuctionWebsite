<template>
  <form>
    <h3>Change Query</h3>
    <label>Question:</label><br>
    <input type="text" v-model="question" required><br>
    <button type="submit" @click="update">submit</button>
  </form>
</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router';
import { ref } from 'vue';
import * as Api from '@/lib/api';

const route = useRoute();
const itemId = typeof route.params.itemId === 'string' ? parseInt(route.params.itemId) : parseInt(route.params.itemId[0]);
const queryId = typeof route.params.queryId === 'string' ? parseInt(route.params.queryId) : parseInt(route.params.queryId[0]);
const question = ref('')


async function update() {
  return await Api.updateItemQuery(itemId, queryId, {
    question: question.value,
  },);
}
</script>
