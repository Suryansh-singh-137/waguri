from state import Researchstate
from llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient
import os



tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tractionAgent(state: Researchstate):
    print("traction agent is running...")
    startup_name = state["startup_name"]
    
    queries = [
        f"{startup_name} startup funding revenue users growth 2025 2026",
        f"{startup_name} startup new feature launch product update"
    ]
    
    all_findings = ""
    for q in queries:
        results = tavily.search(query=q, max_results=3)
        # Using .get("results", []) is a safer Python pattern to prevent crashes if Tavily returns an empty dict
        for r in results.get("results", []): 
            all_findings += f"\nSource: {r['url']}\n{r['content']}\n"
            
    

    
    
    system = """You are a Growth Equity Analyst.Your job is to extract factual traction metrics (funding amounts, user counts, revenue estimates) and recent product milestones.
    
    CRITICAL RULES:
    1. Do not evaluate the company; just extract the hard facts.
 
    2. If information is sparse, state exactly what is known without hallucinating."""
    
    result =llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=f"Startup: {startup_name}\n\nRaw research:\n{all_findings}")
    ])
    
    
    return {
        "traction_info":result.content
    }