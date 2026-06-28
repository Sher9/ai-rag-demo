<template>
  <div class="chat-window">
    <!-- 消息列表 -->
    <div class="message-list" ref="messageListRef">
      <div v-if="messages.length === 0" class="empty-state">
        <el-icon :size="64" color="#c0c4cc"><ChatDotRound /></el-icon>
        <p>上传文档后，开始提问吧</p>
      </div>
      <template v-for="(msg, index) in messages" :key="index">
        <MessageItem
          :role="msg.role"
          :content="msg.content"
          :time="msg.time"
          :is-streaming="msg.isStreaming"
        />
        <!-- 在 AI 消息后展示来源 -->
        <SourceCitation
          v-if="msg.role === 'ai' && msg.sources && msg.sources.length > 0 && !msg.isStreaming"
          :sources="msg.sources"
        />
      </template>
    </div>

    <!-- 输入区域 -->
    <div class="input-area">
      <el-input
        v-model="inputText"
        type="textarea"
        :rows="2"
        placeholder="输入你的问题，按 Enter 发送，Shift+Enter 换行"
        resize="none"
        @keydown.enter.exact.prevent="sendMessage"
        :disabled="isLoading"
      />
      <el-button
        type="primary"
        :icon="Promotion"
        @click="sendMessage"
        :loading="isLoading"
        :disabled="!inputText.trim()"
        class="send-btn"
      >
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'
import MessageItem from './MessageItem.vue'
import SourceCitation from './SourceCitation.vue'
import { chatStream, getSources } from '@/api'
import type { SourceSegment } from '@/api'

interface Message {
  role: 'user' | 'ai'
  content: string
  time: string
  isStreaming?: boolean
  sources?: SourceSegment[]
}

const messages = ref<Message[]>([])
const inputText = ref('')
const isLoading = ref(false)
const messageListRef = ref<HTMLElement>()

// 发送消息
async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || isLoading.value) return

  // 添加用户消息
  const userMsg: Message = {
    role: 'user',
    content: text,
    time: formatTime(new Date())
  }
  messages.value.push(userMsg)
  inputText.value = ''
  await scrollToBottom()

  // 添加 AI 占位消息
  const aiMsg: Message = {
    role: 'ai',
    content: '',
    time: formatTime(new Date()),
    isStreaming: true
  }
  messages.value.push(aiMsg)
  const aiIndex = messages.value.length - 1

  isLoading.value = true

  try {
    // SSE 流式请求
    const response = await chatStream(text)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('无法读取响应流')
    }

    const decoder = new TextDecoder()
    let fullContent = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })
      // SSE 格式: "data:xxx\n\n"
      const lines = chunk.split('\n')
      for (const line of lines) {
        if (line.startsWith('data:')) {
          const data = line.slice(5).trim()
          if (data && data !== '[DONE]') {
            fullContent += data
            messages.value[aiIndex].content = fullContent
            await scrollToBottom()
          }
        } else if (line.trim() && !line.startsWith(':')) {
          // 处理不带 data: 前缀的纯文本流
          fullContent += line
          messages.value[aiIndex].content = fullContent
          await scrollToBottom()
        }
      }
    }

    messages.value[aiIndex].isStreaming = false

    // 流式结束后获取来源片段
    try {
      const sourcesRes = await getSources(text)
      if (sourcesRes.code === 200 && sourcesRes.data) {
        messages.value[aiIndex].sources = sourcesRes.data
      }
    } catch {
      // 来源获取失败不影响主流程
    }
  } catch (e: any) {
    messages.value[aiIndex].content = '抱歉，请求失败: ' + (e?.message || '未知错误')
    messages.value[aiIndex].isStreaming = false
    ElMessage.error('对话失败: ' + (e?.message || '网络错误'))
  } finally {
    isLoading.value = false
  }
}

// 滚动到底部
async function scrollToBottom() {
  await nextTick()
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 清除对话
function clearChat() {
  messages.value = []
}

defineExpose({ clearChat, sendMessage })
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--chat-bg);
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 16px;
  color: var(--text-secondary);
  font-size: 15px;
}

.input-area {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid var(--border-color);
  background: #fff;
  align-items: flex-end;
}

.input-area :deep(.el-textarea__inner) {
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.6;
}

.send-btn {
  flex-shrink: 0;
  height: 40px;
  border-radius: 10px;
}
</style>
