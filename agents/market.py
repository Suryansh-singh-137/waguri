from state import Researchstate
from llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient
import os



tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def marketAgent(state: Researchstate):
    print("market agent is running...")
    startup_name = state["startup_name"]
    
    queries = [
        f"{startup_name} startup competitors alternatives",
        f"{startup_name} market share competitive advantage"
    ]
    
    all_findings = ""
    for q in queries:
        results = tavily.search(query=q, max_results=3)
        # Using .get("results", []) is a safer Python pattern to prevent crashes if Tavily returns an empty dict
        for r in results.get("results", []): 
            all_findings += f"\nSource: {r['url']}\n{r['content']}\n"
            
    

    
    
    system = """You are a Market Research Analyst.Identify the startup's top 3 active competitors and explain how this startup differentiates itself (their "moat")."""
    
    result =llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=f"Startup: {startup_name}\n\nRaw research:\n{all_findings}")
    ])
    
    
    return {
        "market_info":result.content
    }