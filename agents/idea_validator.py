from state import Researchstate,IdeaValidationOutput
from llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient
import os



tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def ideaValidatorAgent(state: Researchstate):
    print("idea validator agent is running...")
    startup_name = state["startup_name"]
    
    queries = [
        f"{startup_name} startup (stealth OR waitlist OR vision OR founder building)",
        f"{startup_name} startup alternatives competitors"
    ]
    
    all_findings = ""
    for q in queries:
        results = tavily.search(query=q, max_results=3)
        # Using .get("results", []) is a safer Python pattern to prevent crashes if Tavily returns an empty dict
        for r in results.get("results", []): 
            all_findings += f"\nSource: {r['url']}\n{r['content']}\n"
            
    
    structured_llm = llm.with_structured_output(IdeaValidationOutput)
    
    
    system = """You are a Seed-Stage VC Analyst. Your only job is to analyze the search results and extract factual information about an early-stage startup. 
    
    CRITICAL RULES:
    1. Do not evaluate if the idea is good, bad, valid, or risky.
    2. Simply explain exactly what product or service they are building.
    3. Identify who they are competing against in the market.
    4. If information is sparse, state exactly what is known without hallucinating."""
    
    result = structured_llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=f"Startup: {startup_name}\n\nRaw research:\n{all_findings}")
    ])
    
    
    return {
        "core_concept": result.core_concept,
        "market_competitors": result.market_competitors
    }