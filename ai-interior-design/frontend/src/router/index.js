import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/text-to-image',
    name: 'TextToImage',
    component: () => import('@/views/TextToImage.vue')
  },
  {
    path: '/image-to-image',
    name: 'ImageToImage',
    component: () => import('@/views/ImageToImage.vue')
  },
  {
    path: '/gallery',
    name: 'Gallery',
    component: () => import('@/views/Gallery.vue')
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('@/views/Knowledge.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
