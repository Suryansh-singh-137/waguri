from   state import Researchstate
from  llm  import llm
from langchain_core.messages import SystemMessage, HumanMessage
def  writerAgent(state:Researchstate):
  research =  state['research_finding']
  timeline  = state['timeline']
  critic  = state['critics_argument']
  devil  =  state['devil_argument']
  system = """You are the Writer Agent — a senior technology journalist writing a definitive postmortem.

  You have access to research findings, a timeline, a critic's analysis, and a devil's advocate argument.
  Your job: synthesize everything into a compelling, structured report.

  Write the report in this exact format:

  # [Startup Name] — Postmortem

  ## What They Were
  (2-3 sentences on what the startup did and why it was interesting)

  ## The Timeline
  (key moments, use the timeline provided)

  ## The Debate
  ### The Case Against (Critic)
  (summarize the critic's strongest points)

  ### The Case For (Devil's Advocate)  
  (summarize the devil's most compelling arguments)

  ### The Verdict
  (your own conclusion — was failure inevitable or avoidable?)

  ## Cause of Death
  (ranked list, most to least impactful)

  ## Lessons for Founders
  (3-5 actionable takeaways)

  Write with clarity and conviction. This is journalism, not a bullet point dump."""

  human_msg = f"""research finding  by  research agent {research}and timeline  from timeline agent is {timeline} devil argument from devilAgent {devil} crtic from  crtitc agent {critic}"""
  result = llm.invoke(
    [SystemMessage(content=system),HumanMessage(content=human_msg)]
  )
  return  {
    "final_report" : result.content
  }

