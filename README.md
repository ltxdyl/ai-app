# ai-app

基于 LangGraph 的 AI 应用，使用 MiMo Token Plan 提供模型服务。

## 快速开始

### 环境要求

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) 包管理器

### 安装

```bash
# 克隆项目
git clone https://github.com/ltxdyl/ai-app.git
cd ai-app

# 安装依赖
uv sync
```

### 配置

设置环境变量：

```bash
# Windows PowerShell
$env:MIMO_API_KEY="your-api-key"

# Linux/macOS
export MIMO_API_KEY="your-api-key"
```

### 运行

```bash
uv run ai-app
```

## 项目结构

```
ai-app/
├── src/
│   └── ai_app/
│       ├── __init__.py    # 包入口
│       └── main.py        # 主程序逻辑
├── pyproject.toml         # 项目配置
├── uv.lock               # 依赖锁定文件
└── README.md
```

## 技术栈

- **LangGraph** - AI 工作流框架
- **LangChain Anthropic** - Anthropic 模型接口
- **uv** - Python 包管理器