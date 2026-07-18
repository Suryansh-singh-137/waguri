from   state import Researchstate
from  llm  import llm
from langchain_core.messages import SystemMessage, HumanMessage
def  timelineAgent(state:Researchstate):

  system = """You are a Timeline Agent specialized in reconstructing 
  the chronological history of startups. Given research findings, 
  you identify and order key events with dates.

  Format each event as:
  - [YEAR/DATE] → event description

  Focus on: founding, funding rounds, product launches, 
  pivots, controversies, and shutdown."""
  human_prompt  = f"Startup: {state['startup_name']}\n\nResearch:\n{state['research_findings']}" 
  result = llm.invoke([SystemMessage(content=system), HumanMessage(content=human_prompt)])
  return {
    "timeline": result.content 

  }

