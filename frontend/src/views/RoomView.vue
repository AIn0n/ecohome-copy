<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, onBeforeMount, onMounted } from "vue";
import Plotly from "plotly.js-dist";

import BorderList from "@/components/BorderList.vue";
import AlertComponent from "@/components/AlertComponent.vue";
import api from "@/utilities/axios_config";

const route = useRoute();
const router = useRouter();
const error = ref("warning");
const { name } = route.params;
const devices = ref([]);
const chart = ref(null);
const days = [
  "monday",
  "tuesday",
  "wendesday",
  "thursday",
  "friday",
  "saturday",
  "sunday",
];
const hours = Array(25)
  .fill()
  .map((_, i) => i);

async function refresh_devices() {
  await api
    .get(`/${name}/device`)
    .then((res) => (devices.value = res.data))
    .catch(router.back);
}

function remove_device(device) {
  api
    .delete(`/${name}/device/${device}`)
    .then(() => {
      error.value = "device removed";
      refresh_devices();
    })
    .catch((e) => (error.value = e.message));
}

function prep_data_from_one_device(device, day) {
  let data = Array(25)
    .fill()
    .map(() => 0);
  device.timestamps
    .filter((i) => i.weekdays[day] == true)
    .forEach((n) => {
      for (let i = n.start; i < n.end; ++i) data[i] = device.parameter;
    });
  return data;
}

function prep_data_from_week(device) {
  return [].concat(...days.map((i) => prep_data_from_one_device(device, i)));
}

function x_data() {
  return [].concat(
    ...days.map((day) => [...hours].map((hour) => `${hour}:00 - ${day}`))
  );
}

onMounted(async () => {
  await refresh_devices();
  console.log(prep_data_from_week(devices.value[0]));
  Plotly.newPlot(chart.value, [
    { x: x_data(), y: prep_data_from_week(devices.value[0]), type: "scatter" },
  ]);
});
</script>

<template lang="pug">
div(class="row container")
  BorderList(title="Devices")
    li(class="list-group-item list-group-item-action d-flex justify-content-between" v-for="device in devices")
      span(class="fs-5" @click="router.push(`/${name}/edit-device/${device.name}`)") {{ device.name }}
      button(type="button" class="btn-close" aria-label="Close" @click="remove_device(device.name)")
    li(@click="router.push(`/${name}/add-device`)" class="list-group-item list-group-item-action list-group-item-primary fs-5") Add new device
  div(class="col text-center")
    h1(class="my-5") {{ name }}
    AlertComponent(:text="error" @clear="error = ''")
    div(ref="chart") 
    button(@click="router.push('/')" class="btn btn-outline-secondary position-absolute top-0 end-0 mx-5 my-5 fs-4") back
</template>
