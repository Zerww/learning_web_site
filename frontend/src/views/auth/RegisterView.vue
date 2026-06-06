<template>
  <div class="auth-page">
    <el-card class="auth-card" shadow="always">
      <h2 class="auth-title">注册</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="0" @submit.prevent="handleRegister">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名 (4-20字符)" :prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="form.email" placeholder="邮箱" :prefix-icon="Message" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码 (6-20字符)" :prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item prop="password_confirm">
          <el-input v-model="form.password_confirm" type="password" placeholder="确认密码" :prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" class="auth-btn" :loading="loading" native-type="submit">
            注册
          </el-button>
        </el-form-item>
      </el-form>
      <div class="auth-footer">
        已有账号？<router-link to="/auth/login">立即登录</router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, Message } from '@element-plus/icons-vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { register } from '@/api/auth'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
})

const validatePass = (_rule: any, value: string, callback: any) => {
  if (value !== form.password) callback(new Error('两次密码输入不一致'))
  else callback()
}

const rules: FormRules = {
  username: [{ required: true, min: 4, max: 20, message: '用户名需要 4-20 个字符', trigger: 'blur' }],
  email: [{ required: true, type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }],
  password: [{ required: true, min: 6, max: 20, message: '密码需要 6-20 个字符', trigger: 'blur' }],
  password_confirm: [{ required: true, validator: validatePass, trigger: 'blur' }],
}

async function handleRegister() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    await register(form)
    ElMessage.success('注册成功，请登录')
    router.push('/auth/login')
  } catch {
    // Error handled by interceptor
  }
  loading.value = false
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-color);
}

.auth-card {
  width: 420px;
}

.auth-title {
  text-align: center;
  margin-bottom: 24px;
  font-size: 24px;
}

.auth-btn { width: 100%; }

.auth-footer {
  text-align: center;
  font-size: 14px;
  color: #909399;
  a { color: var(--primary-color); }
}
</style>
