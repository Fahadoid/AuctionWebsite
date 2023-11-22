<script lang="ts" setup>
import noImagePath from '@/assets/no-image.png';
import { computed } from '@vue/reactivity';
import { HOST } from '@/lib/api';

const props = defineProps({
  obj: Object,
  attr: String,
  alt: String,
})

const path = computed(() => {
  if (!props.obj || !props.attr) return noImagePath;

  const objPath = props.obj[props.attr];

  if (objPath) {
    if (import.meta.env.DEV) {
      // If in development, append 'http://localhost:8000' before the path
      return `${HOST}${objPath}`;
    } else {
      // Otherwise, return the path as-is
      return objPath;
    }
  } else {
    return noImagePath;
  }
});
</script>

<template>
  <img :src="path" :alt="alt" />
</template>
