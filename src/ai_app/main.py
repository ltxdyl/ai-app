import os
import sys
import json
from typing import Annotated, Iterator
from typing_extensions import TypedDict
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, BaseMessage, AIMessageChunk
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

# ========== 配置 MiMo Token Plan ==========
MIMO_BASE_URL = "https://token-plan-cn.xiaomimimo.com/anthropic"
MIMO_API_KEY = os.getenv("MIMO_API_KEY")

# ========== 初始化 MiMo 模型 ==========
llm = ChatAnthropic(
    model="mimo-v2.5-pro",
    base_url=MIMO_BASE_URL,
    api_key=MIMO_API_KEY,
    temperature=0.5,
    max_tokens=4096,
)

# ========== 状态定义 ==========
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# ========== 节点函数 ==========
def chat_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# ========== 构建图 ==========
graph = StateGraph(State)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)
workflow = graph.compile()


def stream_chat(content: str) -> Iterator[str]:
    """流式返回 LLM 回复的文本片段。"""
    for chunk in workflow.stream(
        {"messages": [HumanMessage(content=content)]},
        stream_mode="messages",
    ):
        message, _ = chunk
        if isinstance(message, AIMessageChunk) and message.content:
            if isinstance(message.content, str):
                yield message.content
            elif isinstance(message.content, list):
                for block in message.content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        yield block.get("text", "")


# ========== CLI 入口 ==========
def main():
    sys.stdout.reconfigure(encoding="utf-8")
    content = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "你好，请用一句话介绍你自己"
    for text in stream_chat(content):
        print(text, end="", flush=True)
    print()

# ========== FastAPI ==========
api = FastAPI(title="AI App")


@api.get("/chat")
async def chat(content: str):
    """GET /chat?content=你好 — 流式返回回复（SSE）"""
    async def event_stream():
        for text in stream_chat(content):
            yield f"data: {json.dumps({'text': text}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@api.post("/chat")
async def chat_post(body: dict):
    """POST /chat {"content": "你好"} — 流式返回回复（SSE）"""
    content = body.get("content", "")
    if not content:
        return {"error": "content is required"}

    async def event_stream():
        for text in stream_chat(content):
            yield f"data: {json.dumps({'text': text}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")