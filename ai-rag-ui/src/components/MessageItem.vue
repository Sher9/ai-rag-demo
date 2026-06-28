<template>
  <div class="message-item" :class="role">
    <div class="message-avatar">
      <el-avatar v-if="role === 'user'" :size="36" icon="UserFilled" />
      <el-avatar v-else :size="36" :src="aiAvatar" />
    </div>
    <div class="message-content">
      <div class="message-header">
        <span class="message-role">{{ role === 'user' ? '我' : 'AI 助手' }}</span>
        <span class="message-time">{{ formattedTime }}</span>
      </div>
      <div v-if="role === 'ai'" class="markdown-body" v-html="renderedContent"></div>
      <div v-else class="message-text">{{ content }}</div>
      <div v-if="isStreaming" class="typing-cursor"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const props = defineProps<{
  role: 'user' | 'ai'
  content: string
  time?: string
  isStreaming?: boolean
}>()

// 配置 marked
marked.setOptions({
  breaks: true,
  gfm: true
})

const aiAvatar = 'data:image/svg+xml,' + encodeURIComponent(
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#409eff"/><text x="20" y="28" text-anchor="middle" fill="white" font-size="22" font-weight="bold">AI</text></svg>'
)

const renderedContent = computed(() => {
  if (!props.content) return ''
  try {
    const html = marked(props.content)
    return html
  } catch {
    return props.content
  }
})

const formattedTime = computed(() => {
  if (!props.time) return ''
  return props.time
})
</script>

<style scoped>
.message-item {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  animation: fadeIn 0.3s ease;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-item.ai {
  background: var(--msg-ai-bg);
}

.message-avatar {
  flex-shrink: 0;
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.message-role {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
}

.message-time {
  font-size: 12px;
  color: var(--text-secondary);
}

.message-text {
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-word;
}

.user .message-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user .message-text {
  background: var(--msg-user-bg);
  padding: 10px 16px;
  border-radius: 12px 4px 12px 12px;
  max-width: 80%;
}

.user .message-header {
  flex-direction: row-reverse;
}

.ai .markdown-body {
  padding-right: 4px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
