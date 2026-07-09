# LangGraph Search Agent

A simple agentic workflow built with **LangGraph** that plans a search query, runs it through **Tavily Search**, and generates a final answer using an LLM (Google Gemini).

## 🧠 How it works

The agent is structured as a 3-node graph:

```
Planner → Search → Responder
```

1. **Planner** — Takes the user's question and asks the LLM to generate a focused search query.
2. **Search** — Runs the generated query through the Tavily Search API and collects the raw results.
3. **Responder** — Feeds the original question + search results back to the LLM to produce a final, grounded answer.

## 🛠️ Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) — for orchestrating the multi-step agent graph
- [LangChain](https://github.com/langchain-ai/langchain) — message types and tool wrappers
- [Tavily Search API](https://tavily.com/) — real-time web search
- [Google Gemini](https://ai.google.dev/) — LLM for planning and response generation
- Python + `python-dotenv` for environment/config management

## 📂 Project Structure

```
langgraph-search-agent/
├── agent.py          # Main script: graph definition + run logic
├── requirements.txt   # Python dependencies
├── .env.example       # Sample environment file (copy to .env and fill in your keys)
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Simhadrisravya/LangGraph-search-agent-.git
cd LangGraph-search-agent-
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root with:

```
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Run the agent

```bash
python agent.py
```

## 📌 Example

**Input:**
```
Who is the current Deputy Chief Minister of AP?
```

**Flow:**
- Planner generates a search query based on the question
- Search node queries Tavily and retrieves top web results
- Responder synthesizes those results into a final answer

## 🔮 Possible Improvements

- Add conditional routing so the agent skips search when it's not needed
- Improve query generation to more reliably extract the right search intent
- Swap deprecated `TavilySearchResults` for the newer `langchain-tavily` package
- Add streaming output and better error handling for API failures

## 📄 License

This project is open source and available for personal and educational use.
