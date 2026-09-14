import os
import sys
from typing import Annotated
from typing_extensions import TypedDict
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, BaseMessage, AIMessageChunk
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# ========== 配置 MiMo Token Plan ==========
MIMO_BASE_URL = "https://token-plan-cn.xiaomimimo.com/anthropic"  
MIMO_API_KEY = os.getenv("MIMO_API_KEY")  

# ========== 初始化 MiMo 模型 ==========
llm = ChatAnthropic(
    model="mimo-v2.5-pro",          # 按套餐选模型，注意模型名里的点要保留
    base_url=MIMO_BASE_URL,
    api_key=MIMO_API_KEY,
    temperature=0.7,
    # Anthropic API 通常要求指定 max_tokens
    max_tokens=1024,
)

# ========== 状态定义（不变） ==========
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# ========== 节点函数（不变） ==========
def chat_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# ========== 构建图（不变） ==========
graph = StateGraph(State)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)
app = graph.compile()


def main():
    # 设置控制台编码为 UTF-8
    sys.stdout.reconfigure(encoding="utf-8")

    # ========== 流式调用 ==========
    for chunk in app.stream(
        {"messages": [HumanMessage(content="你好，请用一句话介绍你自己")]},
        stream_mode="messages",
    ):
        message, _ = chunk
        if isinstance(message, AIMessageChunk) and message.content:
            # content 可能是字符串或列表（包含 thinking/text 等块）
            if isinstance(message.content, str):
                print(message.content, end="", flush=True)
            elif isinstance(message.content, list):
                for block in message.content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        print(block.get("text", ""), end="", flush=True)
    print()  # 换行