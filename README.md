# Waguri — Dead Startup Postmortem Engine

<div align="center">
  <img src="./assets/logo.svg" alt="Waguri Logo" width="200">
  
  **Automated postmortem research for failed startups**
  
  *Type a startup name. Six specialized AI agents research it, debate it, and produce a structured postmortem.*
</div>

Most startup failures get a tweet and a Medium post.

Waguri gives them a trial.

Type a startup name. Six specialized AI agents research it, debate it, and produce a structured postmortem — what they built, when things went wrong, whether failure was inevitable, and what founders can learn from it.

---

## The Problem

Startup postmortems are either too shallow ("they ran out of money") or locked behind paywalls and academic papers. The real lessons — the specific decisions, the exact moment things broke, the alternate paths not taken — rarely get documented properly.

Waguri automates deep postmortem research using a multi-agent system where each agent has a distinct job, a distinct perspective, and a distinct way of attacking the problem.

---

## Architecture

<img width="1927" height="3001" alt="Waguri Multi-Agent Architecture Diagram" src="https://github.com/user-attachments/assets/9edb709f-1553-4701-bd50-8b043dc5d489" />

---

## How It Works

You type a name. The system does the rest.

```
$ python main.py
Enter startup name: Quibi

[1/6] Researching Quibi...
[2/6] Supervisor evaluating research quality...
[3/6] Building timeline...
[4/6] Devil's Advocate building case for survival...
[5/6] Critic identifying cause of death...
[6/6] Writing final report...

Report saved to quibi_postmortem.md
```

---

## The Agent Architecture

Six specialized agents, each with a completely distinct role:

### 🔍 Research Agent

Runs 5 targeted web searches across different angles — founding story, funding history, what went wrong, founder interviews, and public perception. Synthesizes raw search results into a clean structured research note.

### 👁️ Supervisor Agent

Evaluates whether the research is sufficient to produce a meaningful postmortem. If key information is missing — funding details, cause of failure, timeline anchors — it sends the Research Agent back to search again with more targeted queries. Guards against infinite loops with a maximum retry count. This is the orchestration layer that makes the system dynamic rather than a fixed pipeline.

### 📅 Timeline Agent

Takes the research note and reconstructs the chronological history of the company — founding, funding rounds, product launches, pivots, controversies, and shutdown. Outputs a structured timeline that both debate agents use as their source of truth.

### ✅ Devil's Advocate Agent

Makes the strongest possible case that the startup could have survived. Finds what they got right, identifies realistic pivot opportunities, and argues which external factors were genuinely beyond their control. Runs in parallel with the Critic.

### ❌ Critic Agent

Identifies the real cause of death — not the symptom ("ran out of money") but the underlying flaw that made failure likely from early on. Finds the exact moment the company was doomed. Runs in parallel with the Devil's Advocate.

### ✍️ Writer Agent

Reads everything — research, timeline, both sides of the debate — and synthesizes it into a structured markdown report with a verdict, ranked causes of death, and lessons for founders.

---

## Output Format

Every postmortem follows this structure:

```markdown
# [Startup] — Postmortem

## What They Were

## The Timeline

## The Debate

### The Case Against (Critic)

### The Case For (Devil's Advocate)

### The Verdict

## Cause of Death (ranked)

## Lessons for Founders
```

Reports are saved automatically as `[startup]_postmortem.md`.

---

## What Makes This Different From Just Asking ChatGPT

|                     | ChatGPT               | Waguri                                   |
| ------------------- | --------------------- | ---------------------------------------- |
| Research            | Your knowledge cutoff | Live web search                          |
| Perspective         | Single voice          | Critic vs Devil's Advocate debate        |
| Quality control     | None                  | Supervisor evaluates and retries         |
| Parallel processing | Sequential            | Devil + Critic run simultaneously        |
| Output              | Chat response         | Structured markdown report saved to file |
| Depth               | Surface level         | Multi-source synthesis                   |

---

## Tech Stack

| What             | Why                                                             |
| ---------------- | --------------------------------------------------------------- |
| LangGraph        | Multi-agent orchestration, parallel execution, supervisor loops |
| Tavily           | Web search API with deep content extraction                     |
| LangChain + Groq | LLM integration (llama-3.3-70b-versatile)                       |
| Python + uv      | Dependency management                                           |

---

## Project Structure

```
waguri/
│
├── main.py              # Entry point — takes startup name, runs graph, saves report
├── graph.py             # LangGraph orchestration — all nodes, edges, routing logic
├── state.py             # Shared state TypedDict flowing between all agents
├── llm.py               # LLM initialization (shared across all agents)
│
├── agents/
│   ├── research.py      # Web research + synthesis
│   ├── supervisor.py    # Quality evaluation + retry routing
│   ├── timeline.py      # Chronological reconstruction
│   ├── devil.py         # Devil's Advocate — case for survival
│   ├── critic.py        # Critic — cause of death analysis
│   └── writer.py        # Final report synthesis
│
├── assets/
│   ├── logo.svg         # Vector logo (main source of truth)
│   └── logo.png         # Raster fallback
│
├── .env                 # API keys (never commit this)
├── pyproject.toml       # Dependencies
├── .gitignore
└── README.md
```

---

## Getting Started

### 1. Clone and Install

```bash
git clone https://github.com/yourusername/waguri
cd waguri
uv sync
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**Get free API keys:**

- **Groq:** [console.groq.com](https://console.groq.com) — free tier
- **Tavily:** [tavily.com](https://tavily.com) — free tier, 1000 searches/month

### 3. Run

```bash
uv run main.py
```

Enter any startup name. Report saves automatically.

---

## Example Startups to Try

| Startup      | Why It's Interesting                               |
| ------------ | -------------------------------------------------- |
| **Quibi**    | $1.75B raised, failed in 6 months                  |
| **Vine**     | Killed by its own parent company                   |
| **Theranos** | Fraud vs genuine belief — the debate writes itself |
| **Juicero**  | $400 juice press that didn't need to exist         |
| **Fab.com**  | Grew too fast, pivoted too late                    |
| **WeWork**   | IPO collapse, cult of personality                  |

---

## What I Learned Building This

This project taught me multi-agent orchestration in practice — not from tutorials but from real design decisions:

- **Shared state is better than separate agent states** — centralized truth reduces bugs and coordination overhead
- **When to use parallel edges vs the Send API** — Devil's Advocate and Critic can run simultaneously, speeding up debate
- **How supervisor loops turn a pipeline into a true orchestrated system** — not a fixed chain, but dynamic retry logic
- **How specialized system prompts change output quality dramatically** — each agent's personality matters
- **Why smaller models work better for evaluation tasks** — supervisor uses 8B, not 70B, and still catches quality issues

---


