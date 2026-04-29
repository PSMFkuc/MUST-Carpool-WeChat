# -*- coding: utf-8 -*-
"""
agent.py — LangChain + DeepSeek 智能对话
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prediction import RULE_TEXT  # type: ignore[import]

_prompt = ChatPromptTemplate.from_messages([
    ("system", RULE_TEXT),
    ("human", "{question}"),
])

_chain = None  # 懒加载，首次调用时初始化


def _get_chain():
    global _chain
    if _chain is None:
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        llm = ChatOpenAI(
            model="deepseek-chat",
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
            temperature=0.3,
        )
        _chain = _prompt | llm | StrOutputParser()
    return _chain


def chat(question: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        return "错误：未配置 DEEPSEEK_API_KEY，请在 .env 文件中填入您的 API Key。"
    try:
        return _get_chain().invoke({"question": question})
    except Exception as e:
        err = str(e)
        if "402" in err or "balance" in err.lower() or "insufficient" in err.lower():
            return "错误：DeepSeek 账户余额不足，请前往 https://platform.deepseek.com 充值。"
        if "401" in err or "authentication" in err.lower():
            return "错误：API Key 无效，请检查 .env 文件中的 DEEPSEEK_API_KEY。"
        return f"错误：{err}"
