from state import ResearchState
from llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def research_agent(state: ResearchState):
    startup_name = state["startup_name"]
    
    # multiple targeted searches
    queries = [
        f"{startup_name} startup failure reasons",
        f"{startup_name} company history funding",
        f"{startup_name} shutdown what went wrong",
        f"{startup_name} founder interview postmortem",
        f"site:reddit.com {startup_name} startup failed"
    ]
    
    all_findings = ""
    for query in queries:
        results = tavily.search(query=query, max_results=3)
        for r in results["results"]:
            all_findings += f"\nSource: {r['url']}\n{r['content']}\n"
    
      
    system = """You are a Research Agent. You have gathered raw search results 
  about a failed startup. Synthesize these into a clean, structured research note.

  Include: founding story, key people, business model, funding history, 
  what they built, what went wrong, public perception, and shutdown details.
  Be factual. Cite sources where possible."""

    result = llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=f"Startup: {startup_name}\n\nRaw research:\n{all_findings}")
    ])
    
    return {"research_findings": result.content}