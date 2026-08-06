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

    hits_A = resultsA.get("results", [])
    hits_B = resultsB.get("results", [])

    # THE SHORT CIRCUIT: If no web presence is found, bypass the LLM entirely.
    if len(hits_A) == 0 and len(hits_B) == 0:
        print("--> [CLASSIFIER] Zero search results found. Short-circuiting to pre_launch.")
        return {
            "startup_status": "pre_launch",
            "status_reasoning": "Absolutely zero web presence found. Automatically classifying as pre-launch/stealth.",
            "confidence_score": 1.0,
        }

    formatted_A = "\n".join([f"- {r['content']}" for r in resultsA.get("results", [])])
    formatted_B = "\n".join([f"- {r['content']}" for r in resultsB.get("results", [])])

    raw_context = f"""=== MORTALITY SEARCH RESULTS ===
{formatted_A}

=== VITALITY SEARCH RESULTS ===
{formatted_B}"""

    # Bind the LLM to the Pydantic schema
    structured_llm = llm.with_structured_output(StartupClassification)

    # Explicit rule-based system prompt
 # ... (keep your Tavily searches and short-circuit logic the same) ...

    # Explicit rule-based system prompt
    system = f"""You are a Startup Classification Agent. Your task is to determine the current operational status of the specific startup named "{startup_name}".

Classification Rules:
1. "dead": The startup has explicitly shut down, ceased operations, or been liquidated.
2. "alive": STRICTLY reserved for MASSIVE, established companies with undeniable proof of late-stage operations (e.g., Stripe, OpenAI, Airbnb).
3. "pre_launch": YOUR DEFAULT CHOICE. If the company is early-stage, Seed-stage, Y Combinator-backed, newly launched, stealth, or if the search results are vague, you MUST choose "pre_launch".

CRITICAL: AI models naturally want to classify active early-stage companies as "alive". DO NOT DO THIS. If they are an early-stage startup, you MUST output "pre_launch"."""

    result = structured_llm.invoke(
        [
            SystemMessage(content=system),
            HumanMessage(
                content=f"Startup: {startup_name}\n\nRaw context:\n{raw_context}"
            ),
        ]
    )

    # --- NEW: AI TELEMETRY (Read the LLM's mind) ---
    print(f"\n--> [DEBUG] LLM chose: {result.status}")
    print(f"--> [DEBUG] Reason: {result.reasoning}")
    print(f"--> [DEBUG] Confidence: {result.confidence_score}\n")
    # -----------------------------------------------

    # Confidence Fallback Logic
    final_status = result.status
    if result.confidence_score < 0.6:
        final_status = "pre_launch"

    return {
        "startup_status": final_status,
        "status_reasoning": result.reasoning,
        "confidence_score": result.confidence_score,
    }