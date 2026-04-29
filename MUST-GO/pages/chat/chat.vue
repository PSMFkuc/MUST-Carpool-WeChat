<template>
  <view class="chat-page">
    <!-- AI 客服标题栏（仅 target=kefu 时显示） -->
    <view v-if="isAI" class="ai-bar">
      <uni-icons type="staff" size="18" color="#fff"></uni-icons>
      <text class="ai-bar-text">AI 智能客服</text>
      <text class="ai-bar-sub">由 DeepSeek 提供支持</text>
    </view>

    <scroll-view scroll-y class="msg-list" :scroll-into-view="bottomId">
      <view v-for="msg in msgs" :key="msg.id" :class="['msg-row', msg.isMe ? 'me' : 'other']">
        <view v-if="msg.loading" class="bubble modern-card loading-bubble">
          <text class="dot">···</text>
        </view>
        <view v-else class="bubble modern-card">{{ msg.text }}</view>
      </view>
      <view id="bottom-mark" style="height: 20rpx;"></view>
    </scroll-view>

    <view class="input-bar modern-card">
      <uni-easyinput v-model="inputVal" placeholder="发消息..." :clearable="false" :disabled="sending" />
      <button class="modern-btn send-btn" :disabled="sending" @click="send">发送</button>
    </view>
  </view>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { post } from '@/utils/request.js'

const inputVal = ref('')
const bottomId = ref('')
const sending  = ref(false)
const isAI     = ref(false)

const msgs = ref([
  { id: 1, text: '你好，拼车还在吗？', isMe: true },
  { id: 2, text: '在的，随时可以预订', isMe: false }
])

onLoad((options) => {
  if (options.target === 'kefu') {
    isAI.value = true
    msgs.value = [{ id: Date.now(), text: '你好！我是 MUST-GO AI 智能客服，请问有什么可以帮助你？', isMe: false }]
    uni.setNavigationBarTitle({ title: 'AI 智能客服' })
  }
})

const scrollToBottom = () => {
  nextTick(() => { bottomId.value = 'bottom-mark' })
}

const send = async () => {
  const text = inputVal.value.trim()
  if (!text || sending.value) return

  // 添加用户消息
  msgs.value.push({ id: Date.now(), text, isMe: true })
  inputVal.value = ''
  scrollToBottom()

  // 普通聊天：不调用 AI
  if (!isAI.value) return

  // AI 客服：调用后端
  sending.value = true
  const loadingId = Date.now() + 1
  msgs.value.push({ id: loadingId, text: '', isMe: false, loading: true })
  scrollToBottom()

  try {
    const res = await post('/api/chat', { question: text })
    const idx = msgs.value.findIndex(m => m.id === loadingId)
    if (idx !== -1) msgs.value[idx] = { id: loadingId, text: res.reply, isMe: false }
  } catch (e) {
    const idx = msgs.value.findIndex(m => m.id === loadingId)
    if (idx !== -1) msgs.value[idx] = { id: loadingId, text: '网络异常，请稍后重试', isMe: false }
  } finally {
    sending.value = false
    scrollToBottom()
  }
}
</script>

<style lang="scss" scoped>
.chat-page { height: 100vh; display: flex; flex-direction: column; background: var(--pc-bg); }

.ai-bar {
  display: flex; align-items: center; gap: 12rpx;
  background: var(--pc-primary); padding: 20rpx 30rpx;
  .ai-bar-text { color: #fff; font-size: 28rpx; font-weight: bold; }
  .ai-bar-sub  { color: rgba(255,255,255,.7); font-size: 22rpx; margin-left: auto; }
}

.msg-list { flex: 1; padding: 30rpx; }
.msg-row { display: flex; margin-bottom: 40rpx; }
.msg-row.me { justify-content: flex-end; }
.bubble { padding: 20rpx 30rpx; max-width: 70%; word-break: break-all; }
.msg-row.me .bubble { background: var(--pc-primary); color: #fff; }

.loading-bubble { min-width: 80rpx; display: flex; align-items: center; justify-content: center; }
.dot { font-size: 36rpx; color: var(--pc-sub); letter-spacing: 4rpx; animation: blink 1s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

.input-bar { display: flex; padding: 20rpx 30rpx 60rpx; gap: 20rpx; border-radius: 40rpx 40rpx 0 0; }
.send-btn { width: 140rpx; height: 72rpx; line-height: 72rpx; font-size: 28rpx; margin: 0; }
</style>
