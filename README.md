# SQL Support Bot

Customer support chatbot built with DeepAgents that interacts with a SQL database (Chinook music store) to answer questions about music and customer accounts.

## What This Bot Does

This bot can help customers:
1. **Find music** - search for songs, albums, and artists in the catalog
2. **Access account info** - look up customer account details

The bot uses DeepAgents to autonomously decide which tools to use based on the customer's query.

## Setup

Install dependencies:
```bash
uv sync
```

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-key-here"
```

## Usage

### Python Script
```bash
uv run python agent.py
```

Type your questions and the agent will respond. Type `quit` to exit.

### Jupyter Notebook
```bash
uv run jupyter notebook
```

Then open `agent.ipynb` and run cells sequentially to interact with the agent.

## Example Queries

- "Can you help me find songs by The Beatles?"
- "What albums does Pink Floyd have?"
- "What's the email for customer ID 5?"

## How It Works

- **Database**: Uses the Chinook database (downloads automatically on first run)
- **Tools**: Agent has access to 4 tools for searching music and looking up customer info
- **Routing**: DeepAgents automatically decides which tool(s) to use based on the query

## Writing Evals

The most valuable evals go beyond "did it return the right answer" — they test whether the agent behaves well under pressure, handles ambiguity gracefully, and fails safely. A few directions worth exploring:

**Robustness to ambiguous input** — What happens when a customer asks something that could mean two different things? For example, "find me something by Elvis" could mean Elvis Presley or Elvis Costello. Does the agent pick one silently, ask for clarification, or surface both? An eval here checks not just the final answer but *whether the agent handles the ambiguity in a reasonable way*.

**Tool use correctness under multi-step reasoning** — Some queries require chaining tools in the right order. For example: "Who else has bought albums from the same artist as customer 12?" requires looking up customer 12's purchases, identifying the artist, then finding other customers. An eval here checks that the agent calls the right tools in the right sequence and doesn't hallucinate intermediate results it never actually retrieved.
