<script setup>
import { useRouter } from "vue-router";
//components
import AlertComponent from "@/components/AlertComponent.vue";
import BorderList from "@/components/BorderList.vue";
import IconAndSpan from "@/components/IconAndSpan.vue";
import { onBeforeMount, onMounted, ref } from "vue";
import api from "../utilities/axios_config";
import Plotly from "plotly.js-dist";

const router = useRouter();
const error = ref("");
const rooms = ref([]);
const price_before_limit = ref(0);
const price_after_limit = ref(0);
const new_before = ref(0);
const new_after = ref(0);
const new_room_name = ref("");
const chart = ref(null);
const all_devices = ref([]);
const highest_consumption_devices = ref([]);
const hours = Array(25)
  .fill()
  .map((_, i) => i);

function refresh_highest_cons() {
  highest_consumption_devices.value = all_devices.value
    .filter((x) => x.device_type == 0)
    .sort((a, b) => {
      a.parameter - b.parameter;
    })
    .slice(0, 3);
}

function refresh_payments() {
  api
    .get("/payments")
    .then((res) => {
      price_before_limit.value = res.data.before_limit;
      price_after_limit.value = res.data.after_limit;
    })
    .catch(() => (error.value = "cannot gather costs"));
  refresh_chart();
}

async function get_rooms() {
  await api
    .get("/room/")
    .then((res) => {
      rooms.value = res.data.map((x) => x.name);
    })
    .catch((e) => {
      error.value = e.message + " (probably backend is not working)";
    });
}

function update_payments() {
  api
    .post("/payments", {
      before_limit: new_before.value,
      after_limit: new_after.value,
    })
    .then((res) => {
      error.value = "successfully updated costs";
      refresh_payments();
    })
    .catch(() => (error.value = "cannot update costs"));
}

async function refresh_chart() {
  await get_rooms();
  let tmp = [];
  for (const room of rooms.value) {
    await api.get(`/${room}/device`).then((res) => {
      tmp.push(res.data);
    });
  }
  all_devices.value = [].concat(...tmp);
  Plotly.newPlot(chart.value, prep_solar_eff(all_devices.value), {
    title: "costs in zlotych",
  });
}

onMounted(async () => {
  refresh_payments();
  await refresh_chart();
  refresh_highest_cons();
});

const days = [
  "monday",
  "tuesday",
  "wendesday",
  "thursday",
  "friday",
  "saturday",
  "sunday",
];

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

function x_data() {
  return [].concat(
    ...days.map((day) => [...hours].map((hour) => `${hour}:00 - ${day}`))
  );
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
  let to_pay_acc = [];
  for (const day of days) {
    let usage = sum_devices_for_day(defs, day);
    let payment = [...usage];
    for (const solar of solars) {
      for (const timestamp of solar.timestamps) {
        if (timestamp.weekdays[day] == true) {
          for (let i = timestamp.start; i < timestamp.end; ++i) {
            payment[i] += solar.parameter;
          }
        }
      }
    }
    to_pay_acc.push(payment);
  }
  const over = []
    .concat(...to_pay_acc)
    .map((e) => -e)
    .map((e) => (e > 0 ? e : 0));

  let result = over.map(() => 0);
  for (let i = 1; i < result.length; ++i) {
    for (let j = 0; j < i; ++j) {
      result[i] += over[j];
    }
  }
  console.log(to_pay_acc);
  const x = x_data();
  return [
    {
      x: x,
      y: result.map((e) =>
        e > 2000 ? e * price_after_limit.value : e * price_before_limit.value
      ),
      type: "scatter",
      mode: "lines",
    },
  ];
}

function delete_room(room) {
  api
    .delete(`/room/${room}`)
    .then((res) => {
      error.value = "successfully removed room";
      get_rooms();
    })
    .catch((e) => (error.value = e.message));
}

function add_room() {
  api
    .post("/room/", { name: new_room_name.value })
    .then((res) => {
      error.value = res.data.message;
      get_rooms();
    })
    .catch((e) => (error.value = e.message));
}
</script>

<template lang="pug">
div(class="row container")
  BorderList(title="Rooms")
    li(class="list-group-item list-group-item-action d-flex justify-content-between" v-for="room in rooms")
      span(class="fs-5" @click="router.push('/room/' + room)") {{ room }}
      button(type="button" class="btn-close" aria-label="Close" @click="delete_room(room)")
    li(class="list-group-item list-group-item-action")
      div(class="input-group")
        input(type="text" class="form-control fs-5" placeholder="new room name" v-model="new_room_name")
        button(class="btn btn-outline-primary" @click="add_room") Add
  div(class="col text-center")
    h1(class="my-5") Eco Home
    AlertComponent(:text="error" @clear="error = ''")
    div(ref="chart")
    div(class="list-group col ms-5 mt-3")
      div(class="list-group-item list-group-item-warning d-flex justify-content-between fs-5")
        p price before limit 
        p {{ price_before_limit }} PLN
      div(class="list-group-item list-group-item-warning d-flex justify-content-between fs-5")
        p price after limit
        p {{ price_after_limit }} PLN
    div(class="row my-5")
      div(class="col mx-3")
        IconAndSpan(icon="fa-wallet" text="price before limit")
        input(class="form-control form-control-sm" type="number" v-model="new_before")
      div(class="col mx-3")
        IconAndSpan(icon="fa-wallet" text="price after limit")
        input(class="form-control form-control-sm" type="number" v-model="new_after")
      button(class="btn btn-primary col fs-5 mx-2" @click="update_payments") refresh price
    IconAndSpan(icon="fa-chart-line" text="highest consumption devices")
    div(class="row my-5")
      div(class="card border-warning col mx-3" v-for="device in highest_consumption_devices")
        div(class="card-body")
          h5(class="card-title") {{device.name}}
        ul(class="list-group list-group-flush")
          li(class="list-group-item d-flex justify-content-between fs-5") 
            p energy drain 
            p {{ device.parameter }} kWh 
          li(class="list-group-item d-flex justify-content-between fs-5")
            p energy class 
            p {{ device.energy_class }}
</template>
