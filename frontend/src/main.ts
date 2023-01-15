import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
import FontAwesomeIcon from "./utilities/fontawesome-icons";

createApp(App).component("fa-icon", FontAwesomeIcon).use(router).mount("#app");
