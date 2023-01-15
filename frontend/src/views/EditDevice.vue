<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { ref, onBeforeMount } from "vue";
import AlertComponent from "@/components/AlertComponent.vue";
import api from "@/utilities/axios_config";

const error_text = ref("example of warning");
const router = useRouter();
const { device, room } = useRoute().params;
const timestamps = ref([]);
const days = ref({});

function refresh_timestamps() {
  api
    .get(`/${room}/device/${device}/timestamp`)
    .then((res) => (timestamps.value = res.data))
    .catch(() => (error_text.value = "cannot get timestamps, try later"));
}

onBeforeMount(() => {
  refresh_timestamps();
  api
    .get("/day2number")
    .then((res) => (days.value = res.data))
    .catch(() => (error_text.value = "server error"));
});
</script>

<template lang="pug">
div(class="container text-center w-75")
  h1(class="my-5") Edit {{ device }}
  AlertComponent(:text="error_text" @clear="error_text = ''")
  div(class="card text-bg-primary my-3")
    div(class="card-header") add new timestamp
    div(class="list-group list-group-flush")
      div(class="list-group-item d-flex justify-content-between")
        div(class="input-group input-group-sm w-50 mx-3 my-3")
          span(class="input-group-text") start
          input(type="number" class="form-control" placeholder="hours")
        div(class="input-group input-group-sm w-50 mx-3 my-3")
          span(class="input-group-text") end
          input(type="number" class="form-control" placeholder="hours")
      div(class="list-group-item")
        div(class="form-check form-check-inline mx-4" v-for="(value, key) in days")
          input(class="form-check-input" type="checkbox")
          label(class="form-check-label") {{ key }}
  div(class="d-flex align-items-center" v-for="timestamp in timestamps")
    div(class="card text-bg-primary me-5 my-3")
      div(class="list-group list-group-flush")
        div(class="list-group-item d-flex justify-content-between")
          div(class="input-group input-group-sm w-50 mx-3 my-3")
            span(class="input-group-text") start
            input(type="number" class="form-control" v-model="timestamp.start")
          div(class="input-group input-group-sm w-50 mx-3 my-3")
            span(class="input-group-text") end
            input(type="number" class="form-control" v-model="timestamp.end")
        div(class="list-group-item")
          div(class="form-check form-check-inline mx-4" v-for="(value, key) in days")
            input(class="form-check-input" type="checkbox" v-model="timestamp.weekdays[key]")
            label(class="form-check-label") {{ key }}
    div
      button(type="button" class="btn-close" aria-label="Close")
button(@click="router.back()" class="btn btn-outline-secondary position-absolute top-0 end-0 mx-5 my-5 fs-4") back
button(class="btn btn-primary position-absolute top-0 start-0 mx-5 my-5 fs-4") update
</template>
