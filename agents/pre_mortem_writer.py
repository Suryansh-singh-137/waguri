from   state import Researchstate
from  llm  import llm
from langchain_core.messages import SystemMessage, HumanMessage
def  preMortemWriterAgent(state:Researchstate):
  print("writer agent  running  ....")
  startup_name = state['startup_name']
  core_concept = state['core_concept']
  market_competitors = state['market_competitors']
  risk_simulation = state['risk_simulation']
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
  human_msg  = f"""Startup: {startup_name}
  Core Concept: {core_concept}
  Market Competitors: {market_competitors}
  Risk Simulation: {risk_simulation}"""

  result = llm.invoke(
    [SystemMessage(content=system),HumanMessage(content=human_msg)]
  )
  return  {
    "final_report" : result.content
  }

