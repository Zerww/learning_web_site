<template>
  <div class="page-wrap-narrow">
    <div class="back-row fade-up">
      <BackButton to="/" label="首页" />
    </div>

    <div class="glass-card about-card fade-up-1">
      <div class="about-header">
        <div class="about-avatar">
          <span>M</span>
        </div>
        <h1 class="about-name">管理员</h1>
        <p class="about-tagline">热爱编程，专注 Web 全栈开发</p>
        <div class="about-links">
          <a href="#" class="about-link">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            example@email.com
          </a>
          <a href="#" class="about-link">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
            github.com/user
          </a>
        </div>
      </div>

      <div class="about-section">
        <h2 class="about-section-title">技能</h2>
        <div class="skill-grid">
          <div v-for="s in skills" :key="s.name" class="skill-item">
            <div class="skill-header">
              <span class="skill-name">{{ s.name }}</span>
              <span class="skill-pct">{{ s.level }}%</span>
            </div>
            <div class="skill-bar">
              <div class="skill-fill" :style="{ width: s.level + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="about-section">
        <h2 class="about-section-title">教育背景</h2>
        <p class="about-text">计算机科学与技术 · 本科</p>
      </div>

      <div class="about-section">
        <h2 class="about-section-title">工作经历</h2>
        <p class="about-text">全栈开发工程师 · 持续成长中</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import BackButton from '@/components/common/BackButton.vue'

const skills = [
  { name: 'Vue.js', level: 85 },
  { name: 'TypeScript', level: 75 },
  { name: 'Python / Django', level: 80 },
  { name: 'MySQL', level: 70 },
  { name: 'Docker', level: 65 },
]
</script>

<style scoped>
.back-row { margin-bottom: 20px; }
.about-card { padding: 36px; }
.about-header { text-align: center; padding: 20px 0 32px; border-bottom: 1px solid var(--stone-200); }

.about-avatar {
  width: 72px; height: 72px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-dark));
  color: #fff; display: inline-flex; align-items: center; justify-content: center;
  font-size: 28px; font-weight: 700; margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(245,158,11,0.2);
}

.about-name { font-size: 26px; font-weight: 700; margin-bottom: 6px; color: var(--text-primary); letter-spacing: -0.03em; }
.about-tagline { color: var(--text-muted); font-size: 15px; margin-bottom: 16px; }

.about-links { display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; }
.about-link {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px; border-radius: 8px;
  background: var(--bg-warm); color: var(--text-secondary);
  font-size: 14px; text-decoration: none; transition: all 0.2s;
}
.about-link:hover { background: rgba(245,158,11,0.08); color: var(--accent-dark); }

.about-section { padding-top: 28px; }
.about-section-title {
  font-size: 18px; font-weight: 600; margin-bottom: 14px;
  color: var(--text-primary); letter-spacing: -0.02em;
}
.about-text { color: var(--text-secondary); font-size: 15px; line-height: 1.6; }

.skill-grid { display: flex; flex-direction: column; gap: 14px; }
.skill-item { }
.skill-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
.skill-name { font-size: 14px; font-weight: 500; color: var(--text-primary); }
.skill-pct { font-size: 13px; color: var(--accent-dark); font-weight: 600; }
.skill-bar { height: 6px; background: var(--stone-200); border-radius: 3px; overflow: hidden; }
.skill-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent-dark)); border-radius: 3px; transition: width 1s ease; }
</style>
