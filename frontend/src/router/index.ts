import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

//component: () => import("../views/AboutView.vue"),
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/room/:name",
      name: "room",
      component: () => import("../views/RoomView.vue"),
      props: true,
    },
    {
      path: "/:room/add-device",
      name: "add-device",
      component: () => import("../views/CreateDevice.vue"),
      props: true,
    },
    {
      path: "/edit-device/:device",
      name: "edit-device",
      component: () => import("../views/EditDevice.vue"),
      props: true,
    },
  ],
});

export default router;
