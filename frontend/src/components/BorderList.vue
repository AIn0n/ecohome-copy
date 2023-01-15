<script setup lang="ts">
defineProps(["title"]);
</script>

<template lang="pug">
div(class="col-3 border-end border-secondary me-5" style="height:100vh")
  h3(class="text-center my-3") {{ title  }}
  ul(class="list-group list-group-flush me-1")
    slot
</template>
