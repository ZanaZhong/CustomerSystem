import { createRouter, createWebHistory } from 'vue-router';
import CustomerPage from '@/components/CustomerPage.vue';
import TransactionPage from '@/components/TransactionPage.vue';

const routes = [
  { path: '/', redirect: '/customers' },
  { path: '/customers', component: CustomerPage },
  { path: '/transactions', component: TransactionPage }
];

const router = createRouter({
  history: createWebHistory(), // 使用 history 模式
  routes,
});

export default router;
