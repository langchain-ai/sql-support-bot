# SQL Support Bot

Customer support chatbot that interacts with a SQL database (Chinook music store) to answer questions about music and customer accounts.

## Implementations

This repository includes **two implementations** of the same bot:

### 1. LangGraph Version (Original)
- **File**: `agent.ipynb`
- **Approach**: Manual routing with conditional edges
- **Pros**: Full control, token-efficient, explicit workflow
- **Cons**: More code, manual state management

### 2. DeepAgents Version (New)
- **Files**: `agent_deepagents.py` and `agent_deepagents.ipynb`
- **Approach**: Autonomous routing and planning
- **Pros**: Less code, built-in planning, faster to build
- **Cons**: ~20x more tokens, less control over workflow

## Setup

Create a virtual environment and install the dependencies:
```bash
uv venv
uv sync
```

Copy `.env.example` to `.env` and add your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### Python Script (DeepAgents)
```bash
python agent_deepagents.py
```

Then choose between:
1. Simple agent (all tools in one agent)
2. Agent with subagents (specialized contexts)

### Jupyter Notebooks
```bash
jupyter notebook
```

Then open either:
- `agent.ipynb` - LangGraph implementation
- `agent_deepagents.ipynb` - DeepAgents implementation

## Key Differences

| Feature | LangGraph | DeepAgents |
|---------|-----------|------------|
| Code complexity | ~150 lines | ~50-80 lines |
| Routing | Manual conditional edges | Autonomous |
| State management | Explicit | Automatic |
| Token usage | Efficient | ~20x overhead |
| Planning | Manual | Built-in |
| Development speed | Slower | Faster |
| Control | Full control | Less control |

## Which to Use?

**Use LangGraph when:**
- You need precise control over workflow execution
- Token efficiency is critical
- You want to optimize every transition

**Use DeepAgents when:**
- You want rapid prototyping
- You need autonomous task handling
- Built-in planning is valuable
- Token cost is acceptable for convenience
