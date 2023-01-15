<script setup lang="ts">
import { useRouter } from "vue-router";
//components
import AlertComponent from "@/components/AlertComponent.vue";
import BorderList from "@/components/BorderList.vue";
import IconAndSpan from "@/components/IconAndSpan.vue";
import { onBeforeMount, ref } from "vue";
import api from "../utilities/axios_config";

const router = useRouter();
const error = ref("example of warning message");
const rooms = ref([]);
const new_room_name = ref("");

function get_rooms() {
  api
    .get("/room/")
    .then((res) => {
      rooms.value = res.data.map((x: { name: any }) => x.name);
    })
    .catch((e) => {
      error.value = e.message + " (probably backend is not working)";
    });
}

onBeforeMount(get_rooms);

function delete_room(room: string) {
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
    div(class="row my-5")
      div(class="col-6 alert alert-danger") placeholder for chart
      div(class="list-group col ms-5")
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
