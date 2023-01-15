<script setup lang="ts">
defineProps(["text"]);
defineEmits(["clear"]);
</script>

<template lang="pug">
div(v-if="text.length > 0" class="alert alert-dark d-flex justify-content-between") {{text}}
  button(type="button" class="btn-close" aria-label="Close" @click="$emit('clear')")
</template>
