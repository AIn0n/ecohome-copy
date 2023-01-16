<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, onBeforeMount } from "vue";
import AlertComponent from "@/components/AlertComponent.vue";
import api from "@/utilities/axios_config";

const error_text = ref("");
const router = useRouter();
const { device, room } = useRoute().params;
const timestamps = ref([]);
const days = ref({});
const add_new = ref(false);
const new_timestamp = ref({
  start: 0,
  end: 0,
  weekdays: {},
});

function refresh_timestamps() {
  api
    .get(`/${room}/device/${device}/timestamp`)
    .then((res) => (timestamps.value = res.data))
    .catch(() => (error_text.value = "cannot get timestamps, try later"));
}

function preprocess_timestamps() {
  if (add_new.value == true) {
    timestamps.value.push(new_timestamp.value);
  }
  timestamps.value.forEach((elem) => {
    let week_as_num = 0;
    Object.entries(elem["weekdays"]).forEach(([key, value]) => {
      if (value == true) week_as_num += days.value[key];
    });
    elem["weekdays"] = week_as_num;
  });
}

function update_timestamps() {
  preprocess_timestamps();
  api
    .post(`/${room}/device/${device}/timestamp-update`, timestamps.value)
    .then((res) => {
      error_text.value = res.data.message;
      refresh_timestamps();
    })
    .catch(() => (error_text.value = "cannot update timestamps, try later"));
}

function remove_timestamp(timestamp) {
  timestamps.value = timestamps.value.filter((n) => n !== timestamp);
}

onBeforeMount(() => {
  refresh_timestamps();
  api
    .get("/day2number")
    .then((res) => {
      days.value = res.data;
      for (const key in res.data) {
        new_timestamp.value.weekdays[key] = false;
      }
    })
    .catch(() => (error_text.value = "server error"));
});
</script>

<template lang="pug">
div(class="container text-center w-75")
  h1(class="my-5") Edit {{ device }}
  AlertComponent(:text="error_text" @clear="error_text = ''")
  div(class="card text-bg-primary my-3")
    div(class="card-header")
      div(class="form-check")
        input(class="form-check-input" type="checkbox" v-model="add_new")
        label(class="form-check-label") add new timestamp
    div(class="list-group list-group-flush")
      div(class="list-group-item d-flex justify-content-between")
        div(class="input-group input-group-sm w-50 mx-3 my-3")
          span(class="input-group-text") start
          input(type="number" class="form-control" placeholder="hours" v-model="new_timestamp.start")
        div(class="input-group input-group-sm w-50 mx-3 my-3")
          span(class="input-group-text") end
          input(type="number" class="form-control" placeholder="hours" v-model="new_timestamp.end")
      div(class="list-group-item")
        div(class="form-check form-check-inline mx-4" v-for="(value, key) in days")
          input(class="form-check-input" type="checkbox" v-model="new_timestamp.weekdays[key]")
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
      button(type="button" class="btn-close" aria-label="Close" @click="remove_timestamp(timestamp)")
button(@click="router.back()" class="btn btn-outline-secondary position-absolute top-0 end-0 mx-5 my-5 fs-4") back
button(@click="update_timestamps" class="btn btn-primary position-absolute top-0 start-0 mx-5 my-5 fs-4") update
</template>
