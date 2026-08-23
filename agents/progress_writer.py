from state import Researchstate
from llm import llm
from langchain_core.messages import SystemMessage, HumanMessage

def progressWriterAgent(state: Researchstate):
    print("progress writer agent is running...")
    
    startup_name = state["startup_name"]
    traction_info = state.get("traction_info", "No traction data found.")
    market_info = state.get("market_info", "No market data found.")
    
    system = """You are a Lead Tech Journalist and VC Analyst. Your job is to take raw intelligence about a startup and format it into a professional, highly structured Markdown document.
    
    CRITICAL ANTI-HALLUCINATION RULES:
    1. STRICT ADHERENCE: You must ONLY use the facts, numbers, and competitor names explicitly provided in the Raw Data below. 
    2. ZERO EXTERNAL KNOWLEDGE: Do not inject companies, funding amounts, or product names from your memory. If a competitor or metric is NOT explicitly named in the Raw Data, DO NOT list it.
    3. HANDLING UNKNOWNS: If the Raw Data lacks specific numbers or competitors, use professional VC phrasing like "Competitors remain undisclosed in recent findings" or "Traction metrics are not currently public." DO NOT guess.

    Use these specific headers exactly:
    
    # [Startup Name]: Growth & Market Progress Report
    
    ## Traction & Milestones
    (Synthesize the funding, user growth, and product updates here based ONLY on the provided context)
    
    ## Competitive Landscape & Moat
    (Detail their competitors and how they differentiate themselves based ONLY on the provided context)"""
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