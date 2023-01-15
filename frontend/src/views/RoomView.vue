<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { ref, onBeforeMount } from "vue";

import BorderList from "@/components/BorderList.vue";
import AlertComponent from "@/components/AlertComponent.vue";
import api from "@/utilities/axios_config";

const route = useRoute();
const router = useRouter();
const error = ref("warning");
const { name } = route.params;
const devices = ref([]);

function refresh_devices() {
  api
    .get(`/${name}/device`)
    .then((res) => (devices.value = res.data))
    .catch(router.back);
}

function remove_device(device: string) {
  api
    .delete(`/${name}/device/${device}`)
    .then(() => {
      error.value = "device removed";
      refresh_devices();
    })
    .catch((e) => (error.value = e.message));
}

onBeforeMount(refresh_devices);
</script>

<template lang="pug">
div(class="row container")
  BorderList(title="Devices")
    li(class="list-group-item list-group-item-action d-flex justify-content-between" v-for="device in devices")
      span(class="fs-5" @click="router.push('/edit-device/' + device.name)") {{ device.name }}
      button(type="button" class="btn-close" aria-label="Close" @click="remove_device(device.name)")
    li(@click="router.push('/' + name + '/add-device')" class="list-group-item list-group-item-action list-group-item-primary fs-5") Add new device
  div(class="col text-center")
    h1(class="my-5") {{ name }}
    AlertComponent(:text="error" @clear="error = ''")
    div(class="alert alert-primary") placeholder for chart
    button(@click="router.push('/')" class="btn btn-outline-secondary position-absolute top-0 end-0 mx-5 my-5 fs-4") back
</template>
