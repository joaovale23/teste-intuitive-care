import { createRouter, createWebHistory } from 'vue-router';
import OperadorasList from './views/OperadorasList.vue';
import OperadoraDetail from './views/OperadoraDetail.vue';

const routes = [
  {
    path: '/',
    name: 'OperadorasList',
    component: OperadorasList,
  },
  {
    path: '/operadora/:cnpj',
    name: 'OperadoraDetail',
    component: OperadoraDetail,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { left: 0, top: 0 };
  },
});

export default router;
