<template>
  <div class="home-layout">
    <!-- 左侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2 class="app-title">
          <el-icon :size="22"><Reading /></el-icon>
          知识库问答
        </h2>
        <p class="app-subtitle">基于 RAG 的智能问答系统</p>
      </div>

      <div class="sidebar-section">
        <h3 class="section-title">模型配置</h3>
        <div class="model-badge">
          <el-tag effect="dark" type="success" size="small">{{ currentModel }}</el-tag>
        </div>
      </div>

      <div class="sidebar-section">
        <h3 class="section-title">知识库管理</h3>
        <el-button type="primary" class="upload-btn" @click="uploadRef?.open()">
          <el-icon><Upload /></el-icon>
          上传文档
        </el-button>
        <div class="doc-stats" v-if="docCount > 0">
          <p>已入库文档: <strong>{{ docCount }}</strong> 份</p>
        </div>
      </div>

      <div class="sidebar-section">
        <h3 class="section-title">操作</h3>
        <el-button text @click="clearChat">
          <el-icon><Delete /></el-icon>
          清空对话
        </el-button>
      </div>

      <div class="sidebar-footer">
        <p class="footer-text">Python3 + Vue3</p>
      </div>
    </aside>

    <!-- 右侧聊天区域 -->
    <main class="main-content">
      <ChatWindow ref="chatRef" />
    </main>

    <!-- 上传对话框 -->
    <DocumentUpload ref="uploadRef" @success="onUploadSuccess" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ChatWindow from '@/components/ChatWindow.vue'
import DocumentUpload from '@/components/DocumentUpload.vue'

const chatRef = ref<InstanceType<typeof ChatWindow>>()
const uploadRef = ref<InstanceType<typeof DocumentUpload>>()

const currentModel = ref('DeepSeek')
const docCount = ref(0)

function clearChat() {
  chatRef.value?.clearChat()
}

function onUploadSuccess() {
  docCount.value++
}
</script>

<style scoped>
.home-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* ── 侧边栏 ── */
.sidebar {
  width: 260px;
  min-width: 260px;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  padding: 0;
}

.sidebar-header {
  padding: 24px 20px 16px;
  border-bottom: 1px solid var(--border-color);
}

.app-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 4px;
}

.app-subtitle {
  font-size: 12px;
  color: var(--text-secondary);
  margin: 0;
}

.sidebar-section {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.section-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 10px;
}

.model-badge {
  display: flex;
  align-items: center;
}

.upload-btn {
  width: 100%;
}

.doc-stats {
  margin-top: 10px;
  font-size: 13px;
  color: var(--text-secondary);
}

.doc-stats strong {
  color: var(--primary-color);
}

.sidebar-footer {
  margin-top: auto;
  padding: 16px 20px;
  border-top: 1px solid var(--border-color);
}

.footer-text {
  font-size: 12px;
  color: var(--text-secondary);
  text-align: center;
  margin: 0;
}

/* ── 主内容区 ── */
.main-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}
</style>
