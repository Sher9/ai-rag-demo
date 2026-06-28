<template>
  <div class="source-citation" v-if="sources.length > 0">
    <div class="source-header" @click="expanded = !expanded">
      <el-icon><Collection /></el-icon>
      <span>参考来源 ({{ sources.length }})</span>
      <el-icon class="expand-icon" :class="{ rotated: expanded }"><ArrowDown /></el-icon>
    </div>
    <div class="source-list" v-show="expanded">
      <div class="source-item" v-for="(source, index) in sources" :key="index">
        <div class="source-item-header">
          <el-tag size="small" type="info">{{ source.documentName }}</el-tag>
          <span class="similarity">相似度: {{ (source.similarity * 100).toFixed(1) }}%</span>
        </div>
        <div class="source-content">{{ source.content }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { SourceSegment } from '@/api'

defineProps<{
  sources: SourceSegment[]
}>()

const expanded = ref(true)
</script>

<style scoped>
.source-citation {
  margin-top: 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: #fff;
  overflow: hidden;
}

.source-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 14px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text-secondary);
  user-select: none;
  transition: background 0.2s;
}

.source-header:hover {
  background: #f5f7fa;
}

.expand-icon {
  margin-left: auto;
  transition: transform 0.2s;
}

.expand-icon.rotated {
  transform: rotate(180deg);
}

.source-list {
  border-top: 1px solid var(--border-color);
}

.source-item {
  padding: 12px 14px;
  border-bottom: 1px solid #f0f0f0;
}

.source-item:last-child {
  border-bottom: none;
}

.source-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.similarity {
  font-size: 12px;
  color: var(--text-secondary);
}

.source-content {
  font-size: 13px;
  line-height: 1.6;
  color: #555;
  background: #fafafa;
  padding: 8px 12px;
  border-radius: 6px;
  max-height: 120px;
  overflow-y: auto;
}
</style>
