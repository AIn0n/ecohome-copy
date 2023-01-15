<script setup lang="ts">
defineProps(["icon", "text"]);
</script>

<template lang="pug">
div(class="container mt-3")
  fa-icon(:icon="icon" class="me-3 fa-lg")
  span(class="fs-5") {{text}}
</template>
