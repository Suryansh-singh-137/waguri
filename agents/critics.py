from   state import Researchstate
from  llm  import llm
from langchain_core.messages import SystemMessage, HumanMessage
def  criticAgent(state:Researchstate):
  research =  state['research_findings']
  timeline  = state['timeline']
  system = """You are a Critic Agent — a ruthless, evidence-based analyst specializing in startup failures.

  Your job: identify exactly why this startup failed. Be specific, not generic.
  "Bad timing" and "ran out of money" are symptoms, not causes. Dig deeper.

  Structure your analysis as:
  1. The core fatal flaw (the ONE thing that made failure inevitable)
  2. Supporting evidence from the research and timeline
  3. The exact moment it was doomed (a specific decision or event)
  4. Secondary causes that accelerated the failure

  Be brutal. Be specific. Use evidence."""
  human_msg = f"""Research findings from research agent:
{research}

Timeline from timeline agent:
{timeline}"""
  result = llm.invoke(
    [SystemMessage(content=system),HumanMessage(content=human_msg)]
  )
  return  {
    "critics_argument" : result.content
  }

