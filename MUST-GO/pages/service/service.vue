<template>
  <view class="pc-page pc-box service-page">
    <view class="contact-card modern-card">
      <uni-icons type="headphones" size="50" color="var(--pc-primary)"></uni-icons>
      <view class="contact-info">
        <text class="title text-main font-bold">在线客服</text>
        <text class="desc text-sub">服务时间: 08:00 - 22:00</text>
      </view>
      <view class="btn-group">
        <button class="modern-btn ai-btn" @click="goAIChat">AI 问答</button>
        <button class="modern-btn chat-btn" @click="goOnlineSupport">联系人工</button>
      </view>
    </view>

    <view class="faq-section modern-card">
      <view class="faq-header border-bottom">
        <text class="text-main font-bold">常见问题</text>
      </view>
      <uni-collapse accordion>
        <uni-collapse-item title="如何发布拼车行程？">
          <view class="content text-sub">点击首页右下角的加号按钮，填写您的出发地、目的地、时间和预期价格后即可发布。</view>
        </uni-collapse-item>
        <uni-collapse-item title="车主认证需要多久？">
          <view class="content text-sub">提交真实姓名、车牌号和车辆型号后，系统将在1-3个工作日内完成审核。</view>
        </uni-collapse-item>
        <uni-collapse-item title="如何取消已预订的行程？">
          <view class="content text-sub">请在“我的订单”页面找到对应订单，点击进入详情后选择取消。若距离发车不足1小时，可能会扣除部分信用分。</view>
        </uni-collapse-item>
      </uni-collapse>
    </view>
  </view>
</template>

<script setup>
const goOnlineSupport = () => {
  uni.navigateTo({ url: '/pages/chat/chat?target=kefu' })
}
const goAIChat = () => {
  uni.navigateTo({ url: '/pages/chat/chat?target=kefu' })
}
</script>

<style lang="scss" scoped>
.service-page { padding: 30rpx; }
.contact-card { display: flex; align-items: center; padding: 40rpx; margin-bottom: 40rpx; }
.contact-info { flex: 1; margin-left: 30rpx; display: flex; flex-direction: column; gap: 10rpx; }
.title { font-size: 32rpx; }
.desc { font-size: 24rpx; }
.btn-group { display: flex; gap: 16rpx; }
.ai-btn   { margin: 0; font-size: 26rpx; height: 60rpx; line-height: 60rpx; width: 140rpx; background: #10b981; }
.chat-btn { margin: 0; font-size: 26rpx; height: 60rpx; line-height: 60rpx; width: 140rpx; }

.faq-section { padding: 0; }
.faq-header { padding: 30rpx; }
.border-bottom { border-bottom: 1px solid var(--pc-border); }
.content { padding: 30rpx; font-size: 28rpx; line-height: 1.6; background-color: var(--pc-bg); }
</style>