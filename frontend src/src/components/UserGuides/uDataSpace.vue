<script setup >
import {defineProps} from "vue";

const props = defineProps({
  isDark: {
    type: Boolean,
    required: true
  },
  windowsHeight: {
    type: Number,
    required: true
  },
  windowsWidth: {
    type: Number,
    required: true
  }
})
</script>

<template>
  <p>下面是数据空间的使用介绍</p>
</template>

<style scoped>

</style>