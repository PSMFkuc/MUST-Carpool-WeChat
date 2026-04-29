# -*- coding: utf-8 -*-
"""
main.py — FastAPI 主入口
启动命令：uvicorn main:app --reload --port 5000
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from models import init_db  # type: ignore[import]
from routes import router  # type: ignore[import]

app = FastAPI(title="MUST-GO 拼车成功率预测", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "MUST-GO Carpool Predictor v2"}


@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>MUST-GO 拼车预测 · 接口测试</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Segoe UI',sans-serif;background:#f0f4f8;color:#333}
  header{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:24px 32px}
  header h1{font-size:1.6rem}
  header p{opacity:.85;margin-top:4px;font-size:.9rem}
  .container{max-width:860px;margin:32px auto;padding:0 16px;display:flex;flex-direction:column;gap:24px}
  .card{background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.08);overflow:hidden}
  .card-header{padding:16px 20px;border-bottom:1px solid #eee;display:flex;align-items:center;gap:10px}
  .badge{padding:3px 10px;border-radius:20px;font-size:.75rem;font-weight:700;color:#fff}
  .post{background:#f59e0b}.get{background:#10b981}
  .card-header h2{font-size:1rem;font-weight:600}
  .card-header code{font-size:.85rem;color:#6366f1;margin-left:4px}
  .card-body{padding:20px}
  .row{display:flex;gap:12px;margin-bottom:12px;flex-wrap:wrap}
  label{display:block;font-size:.8rem;color:#666;margin-bottom:4px}
  input,textarea{width:100%;border:1px solid #ddd;border-radius:8px;padding:9px 12px;font-size:.9rem;outline:none;transition:border .2s}
  input:focus,textarea:focus{border-color:#667eea}
  textarea{resize:vertical;min-height:60px}
  .row>div{flex:1;min-width:120px}
  button{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;border-radius:8px;padding:10px 24px;font-size:.9rem;cursor:pointer;transition:opacity .2s}
  button:hover{opacity:.88}
  .result{margin-top:14px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:14px;font-size:.85rem;font-family:monospace;white-space:pre-wrap;min-height:48px;color:#1e293b}
  .err{color:#ef4444}
</style>
</head>
<body>
<header>
  <h1>🚗 MUST-GO 拼车预测系统</h1>
  <p>接口测试面板 · http://127.0.0.1:5000</p>
</header>
<div class="container">

  <!-- 1. 成功率预测 -->
  <div class="card">
    <div class="card-header">
      <span class="badge post">POST</span>
      <h2>成功率预测<code>/api/predict</code></h2>
    </div>
    <div class="card-body">
      <div class="row">
        <div><label>出发地</label><input id="p-start" value="科技园南区"></div>
        <div><label>目的地</label><input id="p-end" value="高铁站"></div>
        <div><label>小时 (0-23)</label><input id="p-hour" type="number" min="0" max="23" value="8"></div>
        <div><label>星期 (0=周一)</label><input id="p-weekday" type="number" min="0" max="6" value="0"></div>
      </div>
      <button onclick="predict()">发送请求</button>
      <div class="result" id="res-predict">结果将显示在此处…</div>
    </div>
  </div>

  <!-- 2. 主动推荐 -->
  <div class="card">
    <div class="card-header">
      <span class="badge get">GET</span>
      <h2>主动推荐<code>/api/recommend</code></h2>
    </div>
    <div class="card-body">
      <button onclick="recommend()">获取推荐路线</button>
      <div class="result" id="res-recommend">结果将显示在此处…</div>
    </div>
  </div>

  <!-- 3. AI 对话 -->
  <div class="card">
    <div class="card-header">
      <span class="badge post">POST</span>
      <h2>AI 智能对话<code>/api/chat</code></h2>
    </div>
    <div class="card-body">
      <div style="margin-bottom:12px">
        <label>问题</label>
        <textarea id="c-question">早上8点从科技园去高铁站拼车成功率高吗？</textarea>
      </div>
      <button onclick="chatApi()">发送</button>
      <div class="result" id="res-chat">结果将显示在此处…</div>
    </div>
  </div>

</div>
<script>
const base = 'http://127.0.0.1:5000'
const show = (id, data, err) => {
  const el = document.getElementById(id)
  el.className = 'result' + (err ? ' err' : '')
  el.textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2)
}
async function predict() {
  const body = {
    start: document.getElementById('p-start').value,
    end:   document.getElementById('p-end').value,
    hour:  parseInt(document.getElementById('p-hour').value),
    weekday: parseInt(document.getElementById('p-weekday').value),
  }
  try {
    const r = await fetch(base+'/api/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
    show('res-predict', await r.json(), !r.ok)
  } catch(e){ show('res-predict', e.message, true) }
}
async function recommend() {
  try {
    const r = await fetch(base+'/api/recommend')
    show('res-recommend', await r.json(), !r.ok)
  } catch(e){ show('res-recommend', e.message, true) }
}
async function chatApi() {
  const body = { question: document.getElementById('c-question').value }
  try {
    const r = await fetch(base+'/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
    show('res-chat', await r.json(), !r.ok)
  } catch(e){ show('res-chat', e.message, true) }
}
</script>
</body>
</html>"""
