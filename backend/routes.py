"""
routes.py — FastAPI 路由（三个核心接口）
"""
from fastapi import APIRouter
from pydantic import BaseModel
from prediction import predict, get_active_recommendations
from agent import chat

router = APIRouter()


# ── 1. 成功率预测 ─────────────────────────────────────────────────────
class PredictReq(BaseModel):
    start:   str
    end:     str
    hour:    int   # 0-23
    weekday: int   # 0=周一 … 6=周日


@router.post("/api/predict")
def api_predict(req: PredictReq):
    return predict(req.start, req.end, req.hour, req.weekday)


# ── 2. 智能对话（LangChain + DeepSeek）───────────────────────────────
class ChatReq(BaseModel):
    question: str


@router.post("/api/chat")
def api_chat(req: ChatReq):
    try:
        reply = chat(req.question)
    except Exception as e:
        reply = f"调用失败：{e}"
    return {"reply": reply}


# ── 3. 主动推荐（常用路线成功率 > 75% 时返回）────────────────────────
@router.get("/api/recommend")
def api_recommend():
    items = get_active_recommendations(threshold=75)
    return {"count": len(items), "items": items}
