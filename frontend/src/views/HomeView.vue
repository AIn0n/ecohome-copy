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
const error = ref("example of warning message");
const rooms = ref([]);
const price_before_limit = 0.5;
const price_after_limit = 0.7;
const new_room_name = ref("");
const chart = ref(null);
const hours = Array(25)
  .fill()
  .map((_, i) => i);

function get_rooms() {
  api
    .get("/room/")
    .then((res) => {
      rooms.value = res.data.map((x) => x.name);
    })
    .catch((e) => {
      error.value = e.message + " (probably backend is not working)";
    });
}

onMounted(() => {
  api
    .get("/room/")
    .then(async (res) => {
      rooms.value = res.data.map((x) => x.name);
      let all_devices = [];
      for (const room of rooms.value) {
        await api.get(`/${room}/device`).then((res) => {
          all_devices.push(res.data);
        });
      }
      Plotly.newPlot(chart.value, prep_solar_eff([].concat(...all_devices)), {
        title: "costs in zlotych",
      });
    })
    .catch((e) => {
      error.value = e.message + " (probably backend is not working)";
    });
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
        e > 2000 ? e * price_after_limit : e * price_before_limit
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

const highest_consumption_devices = [
  {
    name: "TV",
    energy_class: "C",
    energy_drain: 300,
    room: "kitchen",
  },
  {
    name: "Vacuum cleaner",
    energy_class: "D--",
    energy_drain: 250,
    room: "bedroom",
  },
  {
    name: "Blender",
    energy_class: "E",
    energy_drain: 250,
    room: "kitchen",
  },
];
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
    h1(class="my-5") hello User!
    AlertComponent(:text="error" @clear="error = ''")
    div(ref="chart")
    div(class="list-group col ms-5 mt-3")
      div(class="list-group-item list-group-item-warning d-flex justify-content-between fs-4")
        p energy cost
        p 40 zl
      div(class="list-group-item list-group-item-warning d-flex justify-content-between fs-4")
        p estimated month bill
        p 30 zl 
    div(class="row my-5")
      div(class="col mx-3")
        IconAndSpan(icon="fa-wallet" text="price before limit")
        input(class="form-control form-control-sm" type="number")
      div(class="col mx-3")
        IconAndSpan(icon="fa-wallet" text="price after limit")
        input(class="form-control form-control-sm" type="number")
      button(class="btn btn-primary col fs-5 mx-2") refresh price
    IconAndSpan(icon="fa-chart-line" text="highest consumption devices")
    div(class="row mt-5")
      div(class="card border-warning col mx-3" v-for="device in highest_consumption_devices")
        div(class="card-body")
          h5(class="card-title") {{device.name}}
          h6(class="card-subtitle mb-2 text-muted") {{  device.room }}
        ul(class="list-group list-group-flush")
          li(class="list-group-item d-flex justify-content-between fs-5") 
            p energy drain 
            p {{ device.energy_drain }} kWh 
          li(class="list-group-item d-flex justify-content-between fs-5")
            p energy class 
            p {{ device.energy_class }}
</template>
