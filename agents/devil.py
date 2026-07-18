from   state import Researchstate
from  llm  import llm
from langchain_core.messages import SystemMessage, HumanMessage
def  devilAgent(state:Researchstate):
  research =  state['research_finding']
  timeline  = state['timeline']
  system = """You are the Devil's Advocate Agent — an optimistic contrarian who argues that this startup could have survived.

  Your job: make the strongest possible case that failure was NOT inevitable.
  Find the missed opportunities, the alternate paths, the external factors beyond their control.

  Structure your argument as:
  1. The core case for survival (what they actually got right)
  2. The pivots they could have made (specific, realistic alternatives)
  3. External factors that unfairly killed them (market timing, competitors, macro events)
  4. The version of this company that succeeds (what it looks like)

Be genuinely convincing. Steel-man their position."""
  human_msg = f"""research finding  by  research agent {research}and timeline  from timeline agent is {timeline}"""
  result = llm.invoke(
    [SystemMessage(content=system),HumanMessage(content=human_msg)]
  )
  return  {
    "devil_argument" : result.content
  }

