import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import underscore from 'vue-underscore'
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1/'

createApp(App).use(store).use(router, axios).use(VueSweetalert2,underscore).mount('#app')
