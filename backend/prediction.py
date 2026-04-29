# -*- coding: utf-8 -*-
"""
prediction.py - Rule-based prediction logic
"""
from models import get_conn

PEAK_RULES = [
    {"weekday_min": 0, "weekday_max": 4, "hour_min": 7,  "hour_max": 9,  "bonus": 20, "label": "工作日早高峰"},
    {"weekday_min": 0, "weekday_max": 4, "hour_min": 17, "hour_max": 19, "bonus": 15, "label": "工作日晚高峰"},
    {"weekday_min": 5, "weekday_max": 6, "hour_min": 9,  "hour_max": 17, "bonus": 10, "label": "周末白天"},
]

def _peak_bonus(hour, weekday):
    for rule in PEAK_RULES:
        if rule["weekday_min"] <= weekday <= rule["weekday_max"] and rule["hour_min"] <= hour <= rule["hour_max"]:
            return rule["bonus"], rule["label"]
    return 0, "普通时段"

def predict(start, end, hour, weekday):
    conn = get_conn(); c = conn.cursor()
    rows = c.execute("SELECT success FROM history WHERE start=? AND end=? AND ABS(hour-?)<=1 AND weekday=?", (start, end, hour, weekday)).fetchall()
    if len(rows) >= 5:
        base_rate = sum(r["success"] for r in rows) / len(rows)
    else:
        gr = c.execute("SELECT success FROM history WHERE ABS(hour-?)<=1 AND weekday=?", (hour, weekday)).fetchall()
        base_rate = (sum(r["success"] for r in gr) / len(gr)) if gr else 0.5
    conn.close()
    bonus, peak_label = _peak_bonus(hour, weekday)
    rate = max(5, min(98, int(base_rate * 100) + bonus))
    if rate >= 80:
        rec = f"{peak_label}是出行黄金时段，成功率高，建议立即发布！"
    elif rate >= 60:
        rec = f"{peak_label}成功率适中，可以尝试发布，建议提前30分钟。"
    else:
        rec = f"当前{peak_label}成功率较低，推荐改为工作日 7:00-9:00 或 17:00-19:00 出行。"
    return {"rate": rate, "recommendation": rec}

def get_active_recommendations(threshold=75):
    import datetime
    now = datetime.datetime.now()
    hour, weekday = now.hour, now.weekday()
    conn = get_conn()
    routes = conn.execute("SELECT * FROM routes").fetchall()
    conn.close()
    result = []
    for r in routes:
        p = predict(r["start"], r["end"], hour, weekday)
        if p["rate"] > threshold:
            result.append({"user_id": r["user_id"], "start": r["start"], "end": r["end"], "rate": p["rate"], "recommendation": p["recommendation"]})
    return result

RULE_TEXT = """你是 MUST-GO 拼车助手。以下是拼车成功率的预测规则，请严格依据规则回答用户问题：

【预测规则】
1. 基础成功率 = 同路线±1小时历史成功次数 / 总次数（不足5条时使用全局同时段数据）
2. 高峰奖励：工作日早高峰 7-9点 +20分；晚高峰 17-19点 +15分；周末白天 9-17点 +10分
3. 最终成功率 = clamp(基础率×100 + 奖励分, 5, 98)

【回复规范】
- 成功率≥80：热烈推荐，告知是黄金时段
- 成功率60-79：适中，建议提前发布
- 成功率<60：偏低，推荐改为早晚高峰时段

【常见问题】
- 问"什么时候成功率高"：工作日 7-9点 和 17-19点 成功率最高
- 问"周末能拼车吗"：周末白天9-17点有一定成功率，但低于工作日高峰""".strip()
