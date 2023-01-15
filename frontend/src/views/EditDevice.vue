<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { ref } from "vue";
import AlertComponent from "@/components/AlertComponent.vue";

const error_text = ref("example of warning");
const route = useRoute();
const router = useRouter();
const device = route.params.device;
const days = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];
const timestamps = [
  {
    weekdays: ["Monday", "Saturday"],
    start_hour: 12,
    start_minute: 30,
    end_hour: 13,
    end_minute: 0,
  },
  {
    weekdays: ["Sunday"],
    start_hour: 12,
    start_minute: 30,
    end_hour: 13,
    end_minute: 0,
  },
  {
    weekdays: ["Monday", "Tuesday"],
    start_hour: 13,
    start_minute: 45,
    end_hour: 20,
    end_minute: 30,
  },
];
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
          span(class="input-group-text") H
          input(type="number" class="form-control" placeholder="minutes")
          span(class="input-group-text") M
        div(class="input-group input-group-sm w-50 mx-3 my-3")
          span(class="input-group-text") end
          input(type="number" class="form-control" placeholder="hours")
          span(class="input-group-text") H
          input(type="number" class="form-control" placeholder="minutes")
          span(class="input-group-text") M
      div(class="list-group-item")
        div(class="form-check form-check-inline mx-4" v-for="day in days")
          input(class="form-check-input" type="checkbox")
          label(class="form-check-label") {{ day }}
  div(class="d-flex align-items-center" v-for="timestamp in timestamps")
    div(class="card text-bg-primary me-5 my-3")
      div(class="list-group list-group-flush")
        div(class="list-group-item d-flex justify-content-between")
          div(class="input-group input-group-sm w-50 mx-3 my-3")
            span(class="input-group-text") start
            input(type="number" class="form-control" v-model="timestamp.start_hour")
            span(class="input-group-text") H
            input(type="number" class="form-control" v-model="timestamp.start_minute")
            span(class="input-group-text") M
          div(class="input-group input-group-sm w-50 mx-3 my-3")
            span(class="input-group-text") end
            input(type="number" class="form-control" v-model="timestamp.end_hour")
            span(class="input-group-text") H
            input(type="number" class="form-control" v-model="timestamp.end_minute")
            span(class="input-group-text") M
        div(class="list-group-item")
          div(class="form-check form-check-inline mx-4" v-for="day in days")
            input(class="form-check-input" type="checkbox")
            label(class="form-check-label") {{ day }}
    div
      button(type="button" class="btn-close" aria-label="Close")
button(@click="router.back()" class="btn btn-outline-secondary position-absolute top-0 end-0 mx-5 my-5 fs-4") back
button(class="btn btn-primary position-absolute top-0 start-0 mx-5 my-5 fs-4") update
</template>
