<template>
  <div class="not-found-page">
    <div class="glass-card not-found-card fade-up">
      <span class="nf-code">404</span>
      <h2 class="nf-title">页面未找到</h2>
      <p class="nf-desc">你访问的页面不存在或已被移除</p>
      <router-link to="/" class="nf-btn">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        返回首页
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found-page {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.not-found-card {
  text-align: center;
  padding: 48px 40px;
  max-width: 420px;
  width: 100%;
}

.nf-code {
  font-size: 72px;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
  display: block;
  margin-bottom: 8px;
  letter-spacing: -0.05em;
}

.nf-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.nf-desc {
  font-size: 15px;
  color: var(--text-muted);
  margin-bottom: 28px;
}

.nf-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--accent), var(--accent-dark));
  color: #fff;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  font-size: 15px;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.25s ease;
}

.nf-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(245,158,11,0.3);
}
</style>
