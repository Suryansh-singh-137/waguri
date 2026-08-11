from state import Researchstate
from llm import llm
from langchain_core.messages import SystemMessage, HumanMessage

def progressWriterAgent(state: Researchstate):
    print("progress writer agent is running...")
    
    startup_name = state["startup_name"]
    traction_info = state.get("traction_info", "No traction data found.")
    market_info = state.get("market_info", "No market data found.")
    
    system = """You are a Lead Tech Journalist. Your job is to take raw intelligence about an active startup and format it into a professional, highly structured Markdown document.
    
    Use these specific headers exactly:
    
    # [Startup Name]: Growth & Market Progress Report
    
    ## Traction & Milestones
    (Synthesize the funding, user growth, and product updates here)
    
    ## Competitive Landscape & Moat
    (Detail their competitors and how they differentiate themselves)"""
    
    human_msg = f"""Startup: {startup_name}
    
    Traction Data:
    {traction_info}
    
    Market Data:
    {market_info}"""
    
    result = llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=human_msg)
    ])
    
    return {
        "final_report": result.content
    }