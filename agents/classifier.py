from state import Researchstate, StartupClassification
from llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def classifierAgent(state: Researchstate):
    print("classifier agent is running...")
    startup_name = state["startup_name"]
    
    # Dual-query strategy for competing signals
    queryA = f"{startup_name} startup shut down closed postmortem defunct"
    queryB = f"{startup_name} startup funding launch features hiring 2025 2026"
    
    resultsA = tavily.search(query=queryA, max_results=3)
    resultsB = tavily.search(query=queryB, max_results=3)
    
    formatted_A = "\n".join([f"- {r['content']}" for r in resultsA.get("results", [])])
    formatted_B = "\n".join([f"- {r['content']}" for r in resultsB.get("results", [])])

    raw_context = f"""=== MORTALITY SEARCH RESULTS ===
{formatted_A}

=== VITALITY SEARCH RESULTS ===
{formatted_B}"""

    # Bind the LLM to the Pydantic schema
    structured_llm = llm.with_structured_output(StartupClassification)
    
    # Explicit rule-based system prompt
    system = """You are a Startup Classification Agent. Your task is to determine the current operational status of a startup based strictly on the provided search results.

Classification Rules:
1. "dead": The startup has explicitly shut down, ceased operations, been liquidated, or the founders published a postmortem. (Focus on Mortality results).
2. "alive": The startup has recent activity in 2025 or 2026, such as raising funds, launching features, or actively hiring. (Focus on Vitality results).
3. "pre_launch": There is almost no search presence, they are in stealth mode, or only have an early waitlist. 

CRITICAL: Recency trumps all. If they raised money in 2023 but an article from 2025 says they shut down, they are "dead"."""

    result = structured_llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=f"Startup: {startup_name}\n\nRaw context:\n{raw_context}")
    ])
    
    # Confidence Fallback Logic
    final_status = result.status
    if result.confidence_score < 0.6:
        final_status = "pre_launch"
        
    # Return dictionary uses exact string literals to match the state keys
    return {
        "startup_status": final_status,
        "status_reasoning": result.reasoning,
        "confidence_score": result.confidence_score
    }