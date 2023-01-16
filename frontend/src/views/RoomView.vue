<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, onBeforeMount, onMounted } from "vue";
import Plotly from "plotly.js-dist";

import BorderList from "@/components/BorderList.vue";
import AlertComponent from "@/components/AlertComponent.vue";
import api from "@/utilities/axios_config";

const route = useRoute();
const router = useRouter();
const error = ref("");
const { name } = route.params;
const devices = ref([]);
const chart = ref(null);
const chart_type = ref("power");
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

function prep_power_usage_traces(devices) {
  const x = x_data();
  return devices
    .filter((dev) => dev.device_type == 0)
    .map((dev) => ({
      x: x,
      y: prep_data_from_week(dev),
      type: "scatter",
      mode: "lines",
      name: dev.name,
    }));
}

function sum_devices_for_day(devices, day) {
  const arrays = devices.map((elem) => prep_data_from_one_device(elem, day));
  let result = hours.map(() => 0);
  for (let j = 0; j < hours.length; ++j) {
    for (let i = 0; i < arrays.length; ++i) {
      result[j] -= arrays[i][j];
    }
  }
  return result;
}

function prep_solar_eff(devices) {
  const defs = devices.filter((dev) => dev.device_type == 0);
  const solars = devices.filter((dev) => dev.device_type == 1);
  const accs = devices.filter((dev) => dev.device_type == 2);
  const limit = accs.reduce((acc, n) => acc + n.parameter, 0);
  let accumulator = [];
  let defs_acc = [];
  let to_pay_acc = [];
  for (const day of days) {
    let usage = sum_devices_for_day(defs, day);
    defs_acc = defs_acc.concat(usage);
    let payment = [...usage];
    for (const solar of solars) {
      for (const timestamp of solar.timestamps) {
        if (timestamp.weekdays[day] == true) {
          for (let i = timestamp.start; i < timestamp.end; ++i) {
            usage[i] += solar.parameter;
            payment[i] += solar.parameter;
            if (usage[i] > limit) usage[i] = limit;
          }
        }
      }
      accumulator.push(usage);
    }
    to_pay_acc.push(payment);
  }
  console.log(to_pay_acc);
  const x = x_data();
  return [
    {
      x: x,
      y: [].concat(...accumulator).map((elem) => (elem < 0 ? 0 : elem)),
      type: "scatter",
      mode: "lines",
      name: "generated power",
    },
    {
      x: x,
      y: defs_acc,
      type: "scatter",
      mode: "lines",
      name: "used power",
    },
    {
      x: x,
      y: defs_acc.map(() => limit),
      type: "scatter",
      mode: "lines",
      name: "capacity",
    },
    {
      x: x,
      y: []
        .concat(...to_pay_acc)
        .map((e) => -e)
        .map((e) => (e > 0 ? e : 0)),
      type: "scatter",
      mode: "lines",
      name: "payment",
    },
  ];
}

function redraw_chart() {
  let traces;
  if (chart_type.value === "usage") {
    traces = prep_solar_eff(devices.value);
  } else {
    traces = prep_power_usage_traces(devices.value);
  }
  Plotly.newPlot(chart.value, traces, {
    title: "power usage over week",
  });
}

onMounted(async () => {
  await refresh_devices();
  const traces = prep_power_usage_traces(devices.value);
  Plotly.newPlot(chart.value, traces, {
    title: "power usage over week",
  });
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
    select(class="form-select" @change="redraw_chart" v-model="chart_type")
      option(selected value="power") power usage 
      option(value="usage") solar panels efficiency
    div(ref="chart") 
    button(@click="router.push('/')" class="btn btn-outline-secondary position-absolute top-0 end-0 mx-5 my-5 fs-4") back
</template>
