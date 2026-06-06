import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

// Direct imports for critical views (avoids Vite HMR lazy-load issues)
import MainLayout from '@/layouts/MainLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import HomeView from '@/views/home/HomeView.vue'
import ProjectList from '@/views/projects/ProjectList.vue'
import ProjectDetail from '@/views/projects/ProjectDetail.vue'
import ArticleList from '@/views/articles/ArticleList.vue'
import ArticleDetail from '@/views/articles/ArticleDetail.vue'
import NoteList from '@/views/notes/NoteList.vue'
import NoteDetail from '@/views/notes/NoteDetail.vue'
import AboutView from '@/views/about/AboutView.vue'
import SearchView from '@/views/home/SearchView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import NotFoundView from '@/views/home/NotFoundView.vue'
import ProfileView from '@/views/profile/ProfileView.vue'
import AdminDashboard from '@/views/admin/DashboardView.vue'
import AdminProjects from '@/views/admin/ProjectManage.vue'
import AdminArticles from '@/views/admin/ArticleManage.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: HomeView,
        meta: { title: '首页' },
      },
      {
        path: 'projects',
        name: 'Projects',
        component: ProjectList,
        meta: { title: '项目作品' },
      },
      {
        path: 'projects/:id',
        name: 'ProjectDetail',
        component: ProjectDetail,
        meta: { title: '项目详情' },
      },
      {
        path: 'articles',
        name: 'Articles',
        component: ArticleList,
        meta: { title: '技术文章' },
      },
      {
        path: 'articles/:id',
        name: 'ArticleDetail',
        component: ArticleDetail,
        meta: { title: '文章详情' },
      },
      {
        path: 'notes',
        name: 'Notes',
        component: NoteList,
        meta: { title: '学习笔记' },
      },
      {
        path: 'notes/:id',
        name: 'NoteDetail',
        component: NoteDetail,
        meta: { title: '笔记详情' },
      },
      {
        path: 'about',
        name: 'About',
        component: AboutView,
        meta: { title: '关于我' },
      },
      {
        path: 'search',
        name: 'Search',
        component: SearchView,
        meta: { title: '搜索' },
      },
    ],
  },
  {
    path: '/auth/login',
    name: 'Login',
    component: LoginView,
    meta: { title: '登录' },
  },
  {
    path: '/auth/register',
    name: 'Register',
    component: RegisterView,
    meta: { title: '注册' },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { title: '个人信息', requiresAuth: true },
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { title: '管理后台', requiresAuth: true, requiresAdmin: true },
      },
      {
        path: 'projects',
        name: 'AdminProjects',
        component: AdminProjects,
        meta: { title: '项目管理', requiresAuth: true, requiresAdmin: true },
      },
      {
        path: 'articles',
        name: 'AdminArticles',
        component: AdminArticles,
        meta: { title: '文章管理', requiresAuth: true, requiresAdmin: true },
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView,
    meta: { title: '404' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

// Navigation guard - check auth
router.beforeEach((to, _from, next) => {
  document.title = `${to.meta.title || ''} - 学习成果展示`

  const requiresAuth = to.meta.requiresAuth as boolean
  const requiresAdmin = to.meta.requiresAdmin as boolean

  if (requiresAuth || requiresAdmin) {
    const token = localStorage.getItem('access_token')
    if (!token) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }

    if (requiresAdmin) {
      const userInfo = localStorage.getItem('user_info')
      if (userInfo) {
        const user = JSON.parse(userInfo)
        if (user.role !== 1) {
          next({ name: 'Home' })
          return
        }
      }
    }
  }

  next()
})

export default router
