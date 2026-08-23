from state import Researchstate
from llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

supervisor_llm = ChatGroq(model="openai/gpt-oss-120b") 
def supervisor_agent(state: Researchstate):
    print(" Supervisor evaluating research quality...")
    
    research = state["research_findings"]
    startup_name = state["startup_name"]
    attempts = state.get("research_attempts", 0)
    
    system = """You are a Research Quality Supervisor.
Your job is to evaluate whether research findings about a startup are 
sufficient to produce a meaningful postmortem analysis.

Sufficient research must include:
- Basic founding story and founders
- Business model explanation  
- Funding information
- What went wrong or why it failed
- Approximate timeline of key events

Respond with ONLY one word: "sufficient" or "insufficient" """

    result = supervisor_llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=f"Startup: {startup_name}\n\nResearch:\n{research}")
    ])
    
    quality = result.content.strip().lower()
    
    # force sufficient after 2 attempts to avoid infinite loop
    if attempts >= 2:
        quality = "sufficient"
    
    return {
        "research_quality": quality,
        "research_attempts": attempts + 1
    }