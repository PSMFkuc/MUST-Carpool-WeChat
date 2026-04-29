// utils/request.js — 统一请求封装
const BASE_URL = 'http://192.168.31.201:5000'//测试用的局域网私有ip(即本机ip），后续考虑部署云服务器或采用内网穿透用于演示

export function request(method, path, data = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + path,
      method,
      data,
      header: { 'Content-Type': 'application/json' },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          reject(new Error(`HTTP ${res.statusCode}`))
        }
      },
      fail: (err) => reject(err)
    })
  })
}

// 语义化方法
export const post = (path, data) => request('POST', path, data)
export const get  = (path)       => request('GET',  path)

/*AI 智能客服模块

新增 backend/ 独立后端服务（FastAPI + DeepSeek LLM）
实现 /api/chat 接口，支持自然语言对话，由 DeepSeek 提供 AI 能力
实现 /api/predict 接口，基于历史数据预测拼车成功率
实现 /api/recommend 接口，主动推荐高成功率路线
新增后端交互测试面板（访问 http://[host]:5000）
前端集成

新增 MUST-GO/utils/request.js，统一封装 uni.request 请求方法
改造 pages/chat/chat.vue，target=kefu 模式下接入 AI 对话，展示加载动画和流式回复
改造 pages/service/service.vue，新增「AI 问答」入口按钮*/