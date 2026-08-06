from   state import Researchstate
from  llm  import llm
from langchain_core.messages import SystemMessage, HumanMessage
def  preMortemWriterAgent(state:Researchstate):
  print("writer agent  running  ....")
  startup_name = state['startup_name']
  core_concept = state['core_concept']
  market_competitors = state['market_competitors']
  risk_simulation = state['risk_simulation']
  system="""You are a Lead Startup Analyst. Your job is to take the raw intelligence and format it into a professional, highly structured Markdown document.
  use these specific headers exactly:

  # [Startup Name]: Pre-Mortem Risk Analysis

  ## The Vision (Synthesize the core concept)

  ## Market Landscape (Detail the competitors)

  ## The Pre-Mortem: 3-Year Failure Simulation (Format the risk vectors cleanly)"""
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

