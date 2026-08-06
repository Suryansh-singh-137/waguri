from state import Researchstate
from llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
def  riskSimulatorAgent(state:Researchstate):
  print("riskSimulatorAgent running.....")
  startup_name = state['startup_name']
  core_concept = state['core_concept']
  market_competitors = state['market_competitors']
  system = """You are a Ruthless Pre-Mortem Strategist. Fast-forward 3 years into the future and assume this startup has completely failed. 
  
  Your job is to reverse-engineer WHY it died based on their core concept and market competitors. 
  
  Generate 3 highly specific, distinct failure vectors (e.g., "Crushed by incumbent distribution," "Burn rate exhausted before product-market fit," "Regulatory block"). For each vector, provide a brief, realistic explanation of how it played out."""
  result = llm.invoke([
    SystemMessage(content=system),
    HumanMessage(content=f"Startup: {startup_name}\n\nWhat they are building: {core_concept}\n\nTheir market/competitors: {market_competitors}")


  ])
  return  {
    "risk_simulation" : result.content
  }
