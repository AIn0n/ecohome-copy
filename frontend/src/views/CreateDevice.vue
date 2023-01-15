<script setup lang="ts">
import { useRouter, useRoute } from "vue-router";
import { ref, onBeforeMount } from "vue";
// components
import AlertComponent from "@/components/AlertComponent.vue";
import IconAndSpan from "@/components/IconAndSpan.vue";
import api from "@/utilities/axios_config";

const router = useRouter();
const energy_classes = ref({});
const device_types = ref({});
const error = ref("example warning message");
const room: string | string[] = useRoute().params.room;

const en_cls = ref(0);
const dev_type = ref(0);
const name = ref("");
const drain = ref(0);

onBeforeMount(() => {
  api
    .get("/energy-class")
    .then((res) => (energy_classes.value = res.data))
    .catch((e) => (error.value = "cannot get energy classes: " + e.message));
  api
    .get("/device-type")
    .then((res) => (device_types.value = res.data))
    .catch((e) => (error.value = "cannot get device types: " + e.message));
});

function create_device() {
  api
    .post("/" + room + "/device", {
      energy_class: en_cls.value,
      parameter: drain.value,
      name: name.value,
      device_type: dev_type.value,
    })
    .then((res) => (error.value = res.data.message))
    .catch((e) => (error.value = "cannot add new device" + e.message));
}
</script>

<template lang="pug">
div(class="container w-50 text-center")
  h1(class="my-5") Add new device
  AlertComponent(:text="error" @clear="error = ''")
  IconAndSpan(icon="fa-house-laptop" text="Device name")
  input(class="form-control form-control-lg mt-1" type="text" placeholder="new device's name" v-model="name")
  IconAndSpan(icon="fa-lightbulb" text="type")
  select(class="form-select form-select-lg mt-1" v-model="dev_type")
    option(v-for="(value, key) in device_types" :value="value") {{ key }}
  IconAndSpan(icon="fa-plug" text="energy class")
  select(class="form-select form-select-lg" v-model="en_cls")
    option(v-for="(value, key) in energy_classes" :value="value") {{ key }}
  IconAndSpan(icon="fa-bolt" text="energy drain")
  div(class="input-group mt-1")
    input(type="text" class="form-control form-control-lg" placeholder="energy drain in kWh" v-model="drain")
    span(class="input-group-text") kWh
button(@click="router.back()" class="btn btn-outline-secondary position-absolute top-0 end-0 mx-5 my-5 fs-4") back
button(@click="create_device" class="btn btn-primary position-absolute top-0 start-0 mx-5 my-5 fs-4") Create
</template>
