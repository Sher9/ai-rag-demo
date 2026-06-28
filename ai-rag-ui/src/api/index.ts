import axios from 'axios'
import type { AxiosResponse } from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000, // SSE 流式需要更长超时
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse) => response.data,
  (error: Error) => {
    console.error('API 请求失败:', error)
    return Promise.reject(error)
  }
)

/** 统一响应结构 */
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

/** 文档信息 */
export interface DocumentVO {
  id: string
  fileName: string
  fileType: string
  fileSize: number
  chunkCount: number
  uploadTime: string
}

/** 来源片段 */
export interface SourceSegment {
  documentName: string
  content: string
  similarity: number
}

/** 对话请求 */
export interface ChatRequest {
  question: string
  conversationId?: string
}

/**
 * 上传文档
 */
export function uploadDocument(file: File): Promise<ApiResponse<DocumentVO>> {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

/**
 * SSE 流式问答 - 返回 fetch Response 用于读取流
 */
export function chatStream(question: string): Promise<Response> {
  return fetch('/api/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  })
}

/**
 * 获取来源片段
 */
export function getSources(question: string): Promise<ApiResponse<SourceSegment[]>> {
  return api.post('/chat/sources', { question })
}
