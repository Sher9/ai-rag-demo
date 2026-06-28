/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module 'marked' {
  export function marked(src: string, options?: any): string
}

declare module 'highlight.js' {
  const hljs: any
  export default hljs
}
