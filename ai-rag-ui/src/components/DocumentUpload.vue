<template>
  <el-dialog
    v-model="visible"
    title="上传文档"
    width="480px"
    :close-on-click-modal="false"
    destroy-on-close
  >
    <el-upload
      ref="uploadRef"
      class="upload-area"
      drag
      :auto-upload="false"
      :limit="1"
      :on-change="handleFileChange"
      :on-remove="handleRemove"
      accept=".pdf,.txt,.md,.markdown,.doc,.docx"
    >
      <el-icon class="upload-icon"><UploadFilled /></el-icon>
      <div class="upload-text">
        <p>将文件拖到此处，或 <em>点击上传</em></p>
        <p class="upload-hint">支持 PDF、TXT、Markdown、Word 格式</p>
      </div>
    </el-upload>

    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="submitUpload" :loading="uploading">
        {{ uploading ? '处理中...' : '上传并入库' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { UploadFile, UploadInstance } from 'element-plus'
import { uploadDocument } from '@/api'

const emit = defineEmits<{
  success: []
}>()

const visible = ref(false)
const uploading = ref(false)
const uploadRef = ref<UploadInstance>()
const selectedFile = ref<File | null>(null)

function open() {
  visible.value = true
  selectedFile.value = null
  uploadRef.value?.clearFiles()
}

function handleFileChange(file: UploadFile) {
  selectedFile.value = file.raw || null
}

function handleRemove() {
  selectedFile.value = null
}

async function submitUpload() {
  if (!selectedFile.value) {
    ElMessage.warning('请选择文件')
    return
  }

  uploading.value = true
  try {
    const res = await uploadDocument(selectedFile.value)
    if (res.code === 200) {
      ElMessage.success(`文档上传成功，已切分为 ${res.data.chunkCount} 个片段并入库`)
      visible.value = false
      emit('success')
    } else {
      ElMessage.error(res.message || '上传失败')
    }
  } catch (e: any) {
    ElMessage.error('上传失败: ' + (e?.message || '网络错误'))
  } finally {
    uploading.value = false
  }
}

defineExpose({ open })
</script>

<style scoped>
.upload-area {
  width: 100%;
}

.upload-icon {
  font-size: 48px;
  color: var(--primary-color);
}

.upload-text {
  margin-top: 8px;
}

.upload-text p {
  margin: 4px 0;
}

.upload-text em {
  color: var(--primary-color);
  font-style: normal;
}

.upload-hint {
  font-size: 12px;
  color: var(--text-secondary);
}
</style>
