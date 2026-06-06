<template>
  <div class="profile-page">
    <!-- Ambient background -->
    <div class="ambient-bg">
      <div class="ambient-shape shape-1"></div>
      <div class="ambient-shape shape-2"></div>
    </div>

    <div class="profile-container">
      <div class="back-row fade-in">
        <BackButton to="/" label="首页" />
      </div>

      <!-- Profile Header -->
      <header class="profile-header fade-in-1">
        <div class="header-avatar-group">
          <div class="avatar-ring">
            <div class="avatar-inner">
              <span class="avatar-letter">{{ profileForm.nickname?.charAt(0) || 'U' }}</span>
            </div>
          </div>
          <div class="header-status-dot"></div>
        </div>
        <div class="header-text">
          <h1 class="header-name">{{ profileForm.nickname || '添个昵称吧' }}</h1>
          <p class="header-bio">{{ profileForm.bio || '写一句简介，让别人了解你' }}</p>
        </div>
      </header>

      <!-- Tab Navigation -->
      <nav class="tab-nav fade-in-2">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="['tab-btn', { active: activeTab === tab.key }]"
          @click="activeTab = tab.key"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          <span>{{ tab.label }}</span>
        </button>
      </nav>

      <!-- Tab Content -->
      <div class="tab-content fade-in-3">
        <!-- Tab: Personal Info -->
        <div v-show="activeTab === 'info'" class="tab-panel">
          <div class="section-card">
            <h3 class="section-card-title">编辑个人信息</h3>
            <p class="section-card-sub">以下信息将展示在个人主页上</p>

            <form class="profile-form" @submit.prevent="handleSave">
              <!-- Nickname -->
              <div class="field-group">
                <label class="field-label">昵称</label>
                <div class="field-input-wrap">
                  <input
                    v-model="profileForm.nickname"
                    type="text"
                    class="field-input"
                    placeholder="你的昵称"
                    maxlength="50"
                    autocomplete="off"
                  />
                  <span class="input-underline"></span>
                </div>
              </div>

              <!-- Bio -->
              <div class="field-group">
                <label class="field-label">个人简介</label>
                <div class="field-input-wrap">
                  <textarea
                    v-model="profileForm.bio"
                    class="field-input field-textarea"
                    placeholder="介绍一下自己..."
                    rows="3"
                    maxlength="500"
                  ></textarea>
                  <span class="input-underline"></span>
                </div>
              </div>

              <!-- GitHub -->
              <div class="field-group">
                <label class="field-label">GitHub</label>
                <div class="field-input-wrap">
                  <span class="input-prefix">github.com/</span>
                  <input
                    v-model="profileForm.github_url"
                    type="text"
                    class="field-input field-input-with-prefix"
                    placeholder="你的GitHub用户名"
                    autocomplete="off"
                  />
                  <span class="input-underline"></span>
                </div>
              </div>

              <!-- Website -->
              <div class="field-group">
                <label class="field-label">个人网站</label>
                <div class="field-input-wrap">
                  <input
                    v-model="profileForm.website_url"
                    type="url"
                    class="field-input"
                    placeholder="https://yoursite.com"
                    autocomplete="off"
                  />
                  <span class="input-underline"></span>
                </div>
              </div>

              <button type="submit" class="save-btn" :class="{ loading: saving }" :disabled="saving">
                <span v-if="!saving">保存修改</span>
                <span v-else>保存中…</span>
              </button>
            </form>
          </div>

          <!-- Password Change -->
          <div class="section-card password-section" style="margin-top: 20px;">
            <h3 class="section-card-title">修改密码</h3>
            <p class="section-card-sub">输入旧密码和新密码</p>

            <form class="profile-form" @submit.prevent="handleChangePassword">
              <div class="field-group">
                <label class="field-label">当前密码</label>
                <div class="field-input-wrap">
                  <input v-model="pwForm.old_password" type="password" class="field-input" placeholder="输入当前密码" />
                  <span class="input-underline"></span>
                </div>
              </div>
              <div class="field-group">
                <label class="field-label">新密码</label>
                <div class="field-input-wrap">
                  <input v-model="pwForm.new_password" type="password" class="field-input" placeholder="6-20 位新密码" />
                  <span class="input-underline"></span>
                </div>
              </div>
              <div class="field-group">
                <label class="field-label">确认新密码</label>
                <div class="field-input-wrap">
                  <input v-model="pwForm.new_password_confirm" type="password" class="field-input" placeholder="再次输入新密码" />
                  <span class="input-underline"></span>
                </div>
              </div>
              <button type="submit" class="save-btn secondary" :class="{ loading: pwSaving }" :disabled="pwSaving">
                <span v-if="!pwSaving">更新密码</span>
                <span v-else>更新中…</span>
              </button>
            </form>
          </div>
        </div>

        <!-- Tab: Likes -->
        <div v-show="activeTab === 'likes'" class="tab-panel">
          <div class="section-card">
            <h3 class="section-card-title">我的点赞</h3>
            <p class="section-card-sub">你点赞过的内容</p>

            <div v-if="likesLoading" class="loading-pulse">
              <div class="pulse-line" v-for="i in 3" :key="i"></div>
            </div>

            <div v-else-if="likesList.length === 0" class="empty-state">
              <span class="empty-icon">♡</span>
              <p>还没有点赞过任何内容</p>
            </div>

            <div v-else class="interact-list">
              <button
                v-for="item in likesList"
                :key="item.id"
                class="interact-item"
                @click="goContent(item.content_type, item.object_id)"
              >
                <span class="interact-title">{{ item.content?.title || '已删除' }}</span>
                <span class="interact-meta">
                  <span class="interact-badge">{{ typeLabel(item.content_type) }}</span>
                  <span class="interact-date">{{ item.created_at?.slice(0, 10) }}</span>
                </span>
              </button>
            </div>
          </div>
        </div>

        <!-- Tab: Favorites -->
        <div v-show="activeTab === 'favorites'" class="tab-panel">
          <div class="section-card">
            <h3 class="section-card-title">我的收藏</h3>
            <p class="section-card-sub">你收藏的内容</p>

            <div v-if="favLoading" class="loading-pulse">
              <div class="pulse-line" v-for="i in 3" :key="i"></div>
            </div>

            <div v-else-if="favList.length === 0" class="empty-state">
              <span class="empty-icon">☆</span>
              <p>还没有收藏过任何内容</p>
            </div>

            <div v-else class="interact-list">
              <button
                v-for="item in favList"
                :key="item.id"
                class="interact-item"
                @click="goContent(item.content_type, item.object_id)"
              >
                <span class="interact-title">{{ item.content?.title || '已删除' }}</span>
                <span class="interact-meta">
                  <span class="interact-badge">{{ typeLabel(item.content_type) }}</span>
                  <span v-if="item.folder_name" class="interact-folder-badge">{{ item.folder_name }}</span>
                  <span class="interact-date">{{ item.created_at?.slice(0, 10) }}</span>
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAppStore } from '@/stores/app'
import { getCurrentUser, updateProfile, changePassword } from '@/api/auth'
import BackButton from '@/components/common/BackButton.vue'
import { getMyLikes, getMyFavorites } from '@/api/interactions'

const router = useRouter()
const store = useAppStore()
const activeTab = ref('info')
const saving = ref(false)

const profileForm = reactive({
  nickname: '',
  bio: '',
  avatar: '',
  github_url: '',
  website_url: '',
})

const pwForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: '',
})
const pwSaving = ref(false)

const likesList = ref<any[]>([])
const likesLoading = ref(false)
const favList = ref<any[]>([])
const favLoading = ref(false)

const tabs = [
  { key: 'info', label: '个人信息', icon: '✦' },
  { key: 'likes', label: '我的点赞', icon: '♡' },
  { key: 'favorites', label: '我的收藏', icon: '☆' },
]

onMounted(async () => {
  if (store.user) {
    profileForm.nickname = store.user.nickname || ''
    profileForm.avatar = store.user.avatar || ''
  }
  try {
    const res = await getCurrentUser()
    if (res.data) {
      profileForm.nickname = res.data.nickname || ''
      profileForm.avatar = res.data.avatar || ''
      profileForm.bio = res.data.bio || ''
      profileForm.github_url = res.data.github_url || ''
      profileForm.website_url = res.data.website_url || ''
      store.setUser({
        id: res.data.id,
        username: res.data.username,
        nickname: res.data.nickname || '',
        avatar: res.data.avatar || '',
        role: res.data.role,
      })
    }
  } catch (e: any) {
    const msg = e?.response?.data?.message || e?.message || '加载个人信息失败'
    ElMessage.warning(msg)
  }
  loadLikes()
  loadFavorites()
})

async function loadLikes() {
  likesLoading.value = true
  try {
    const res = await getMyLikes({ page_size: 50 })
    if (res.data) likesList.value = res.data.list
  } catch { /* ignore */ }
  likesLoading.value = false
}

async function loadFavorites() {
  favLoading.value = true
  try {
    const res = await getMyFavorites({ page_size: 50 })
    if (res.data) favList.value = res.data.list
  } catch { /* ignore */ }
  favLoading.value = false
}

function typeLabel(ct: number): string {
  return { 1: '文章', 2: '项目', 3: '笔记' }[ct] || '未知'
}

function goContent(ct: number, oid: number) {
  const paths: Record<number, string> = { 1: '/articles/', 2: '/projects/', 3: '/notes/' }
  router.push(paths[ct] + oid)
}

async function handleChangePassword() {
  if (!pwForm.old_password || !pwForm.new_password) {
    ElMessage.warning('请填写完整')
    return
  }
  if (pwForm.new_password.length < 6 || pwForm.new_password.length > 20) {
    ElMessage.warning('密码需要 6-20 个字符')
    return
  }
  if (pwForm.new_password !== pwForm.new_password_confirm) {
    ElMessage.warning('两次密码输入不一致')
    return
  }
  pwSaving.value = true
  try {
    await changePassword({
      old_password: pwForm.old_password,
      new_password: pwForm.new_password,
      new_password_confirm: pwForm.new_password_confirm,
    })
    ElMessage.success('密码修改成功')
    pwForm.old_password = ''
    pwForm.new_password = ''
    pwForm.new_password_confirm = ''
  } catch (err: any) {
    const msg = err?.response?.data?.message || '密码修改失败'
    ElMessage.error(msg)
  }
  pwSaving.value = false
}

async function handleSave() {
  saving.value = true
  try {
    const data: any = {}
    if (profileForm.nickname) data.nickname = profileForm.nickname
    if (profileForm.bio) data.bio = profileForm.bio
    if (profileForm.github_url) {
      const gh = profileForm.github_url.trim()
      data.github_url = gh.startsWith('http') ? gh : `https://github.com/${gh}`
    } else {
      data.github_url = ''
    }
    if (profileForm.website_url) data.website_url = profileForm.website_url
    else data.website_url = ''

    await updateProfile(data)
    if (store.user) {
      store.user.nickname = profileForm.nickname
      store.user.avatar = profileForm.avatar
      localStorage.setItem('user_info', JSON.stringify(store.user))
    }
    ElMessage.success('保存成功')
  } catch { ElMessage.error('保存失败') }
  saving.value = false
}
</script>

<style scoped>
/* ============ Google Font Import ============ */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

.profile-page {
  font-family: 'DM Sans', sans-serif;
  min-height: 100vh;
  position: relative;
  padding: 40px 20px;
  background: #FFF8F0;
  overflow: hidden;
}

.back-row { margin-bottom: 20px; }

/* ============ Ambient Background ============ */
.ambient-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.ambient-shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.35;
}

.shape-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, #FDE68A, #F59E0B);
  top: -150px; right: -100px;
  animation: float 12s ease-in-out infinite;
}

.shape-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, #FED7AA, #EA580C);
  bottom: -100px; left: -100px;
  animation: float 15s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(30px, -30px) scale(1.05); }
}

/* ============ Container ============ */
.profile-container {
  position: relative;
  z-index: 1;
  max-width: 640px;
  margin: 0 auto;
}

/* ============ Animations ============ */
.fade-in {
  animation: fadeUp 0.6s ease both;
}
.fade-in-1 {
  animation: fadeUp 0.6s ease 0.15s both;
}
.fade-in-2 {
  animation: fadeUp 0.6s ease 0.3s both;
}
.fade-in-3 {
  animation: fadeUp 0.6s ease 0.45s both;
}


@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============ Profile Header ============ */
.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 32px;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 32px rgba(245,158,11,0.10);
  border: 1px solid rgba(245,158,11,0.12);
  margin-bottom: 24px;
}

.header-avatar-group {
  position: relative;
  flex-shrink: 0;
}

.avatar-ring {
  width: 80px; height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FDE68A, #F59E0B);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(245,158,11,0.25);
}

.avatar-inner {
  width: 72px; height: 72px;
  border-radius: 50%;
  background: #FFF8F0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-letter {
  font-size: 28px;
  font-weight: 700;
  color: #92400E;
}

.header-status-dot {
  position: absolute;
  bottom: 4px; right: 4px;
  width: 14px; height: 14px;
  border-radius: 50%;
  background: #22C55E;
  border: 3px solid #FFF8F0;
}

.header-text {
  flex: 1;
  min-width: 0;
}

.header-name {
  font-size: 24px;
  font-weight: 700;
  color: #1C1917;
  margin: 0 0 4px;
  letter-spacing: -0.02em;
}

.header-bio {
  font-size: 15px;
  color: #A8A29E;
  margin: 0;
  line-height: 1.5;
}

/* ============ Tab Navigation ============ */
.tab-nav {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  background: rgba(255,255,255,0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 6px;
  border-radius: 14px;
  border: 1px solid rgba(245,158,11,0.10);
}

.tab-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  background: transparent;
  color: #A8A29E;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: #78716C;
  background: rgba(245,158,11,0.05);
}

.tab-btn.active {
  color: #92400E;
  background: rgba(245,158,11,0.12);
  box-shadow: 0 1px 3px rgba(245,158,11,0.15);
}

.tab-icon {
  font-size: 16px;
  line-height: 1;
}

/* ============ Tab Content ============ */
.tab-content {
  transition: opacity 0.3s ease;
}

.tab-panel {
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============ Section Card ============ */
.section-card {
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 20px;
  padding: 32px;
  border: 1px solid rgba(245,158,11,0.10);
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 24px rgba(245,158,11,0.06);
}

.section-card-title {
  font-size: 20px;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 4px;
  letter-spacing: -0.01em;
}

.section-card-sub {
  font-size: 14px;
  color: #A8A29E;
  margin: 0 0 28px;
}

/* ============ Form ============ */
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-label {
  font-size: 13px;
  font-weight: 600;
  color: #57534E;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.field-input-wrap {
  position: relative;
}

.input-underline {
  position: absolute;
  bottom: 0; left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #F59E0B, #D97706);
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 1px;
}

.field-input:focus ~ .input-underline {
  width: 100%;
}

.field-input {
  width: 100%;
  padding: 14px 16px;
  background: #FFFCF7;
  border: 2px solid #E7E5E4;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: #1C1917;
  outline: none;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.field-input:hover {
  border-color: #D6D3D1;
}

.field-input:focus {
  border-color: #F59E0B;
  background: #FFFFFF;
  box-shadow: 0 0 0 4px rgba(245,158,11,0.08);
}

.field-input::placeholder {
  color: #D6D3D1;
}

.field-textarea {
  resize: vertical;
  min-height: 80px;
  line-height: 1.6;
}

.field-input-with-prefix {
  padding-left: 108px;
}

.input-prefix {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 14px;
  color: #A8A29E;
  pointer-events: none;
  font-family: 'DM Sans', sans-serif;
  z-index: 1;
}

/* ============ Save Button ============ */
.save-btn {
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #F59E0B, #D97706);
  border: none;
  border-radius: 12px;
  color: #FFFFFF;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.02em;
  margin-top: 8px;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(245,158,11,0.30);
}

.save-btn:active:not(:disabled) {
  transform: translateY(0);
}

.save-btn.loading {
  opacity: 0.8;
  cursor: wait;
}

.save-btn.secondary {
  background: var(--stone-700);
  &:hover:not(:disabled) {
    box-shadow: 0 8px 24px rgba(68,64,60,0.25);
  }
}

.password-section {
  border: 1px solid rgba(245,158,11,0.08);
}

/* ============ Like/Favorite List ============ */
.interact-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.interact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 16px;
  background: #FFFCF7;
  border: 1px solid #E7E5E4;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
  text-align: left;
  font-family: 'DM Sans', sans-serif;
}

.interact-item:hover {
  background: #FFFFFF;
  border-color: #FDE68A;
  transform: translateX(4px);
  box-shadow: 0 2px 12px rgba(245,158,11,0.08);
}

.interact-title {
  flex: 1;
  font-size: 15px;
  font-weight: 500;
  color: #1C1917;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.interact-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.interact-badge {
  font-size: 12px;
  font-weight: 600;
  color: #D97706;
  background: rgba(245,158,11,0.10);
  padding: 3px 10px;
  border-radius: 6px;
}

.interact-folder-badge {
  font-size: 12px;
  font-weight: 500;
  color: #78716C;
  background: #F5F5F4;
  padding: 3px 10px;
  border-radius: 6px;
}

.interact-date {
  font-size: 13px;
  color: #A8A29E;
}

/* ============ Empty State ============ */
.empty-state {
  text-align: center;
  padding: 40px 0;
}

.empty-icon {
  font-size: 40px;
  color: #D6D3D1;
  display: block;
  margin-bottom: 12px;
}

.empty-state p {
  font-size: 15px;
  color: #A8A29E;
  margin: 0;
}

/* ============ Loading Pulse ============ */
.loading-pulse {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 8px 0;
}

.pulse-line {
  height: 48px;
  background: linear-gradient(90deg, #F5F5F4 25%, #EDE9E6 50%, #F5F5F4 75%);
  background-size: 200% 100%;
  border-radius: 12px;
  animation: pulse 1.5s ease infinite;
}

@keyframes pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ============ Responsive ============ */
@media (max-width: 600px) {
  .profile-page { padding: 20px 12px; }
  .profile-header { flex-direction: column; text-align: center; padding: 24px; }
  .header-text { text-align: center; }
  .tab-btn { font-size: 13px; padding: 10px 14px; }
  .section-card { padding: 20px; }
  .field-input-with-prefix { padding-left: 100px; }
}
</style>
