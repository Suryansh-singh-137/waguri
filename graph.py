from langgraph.graph import StateGraph, START, END
from state import Researchstate
from agents.research import research_agent
from agents.timeline import timelineAgent
from agents.critics import criticAgent
from agents.devil import devilAgent
from agents.writer import writerAgent
from agents.supervisor import supervisor_agent
def  route_after_supervisor(state:Researchstate):
  quality=  state['research_quality']
  if quality=="sufficient":
    return  "timeline"
  else:
    return "research"
graph = StateGraph(Researchstate)

graph.add_node("research", research_agent)
graph.add_node("timeline", timelineAgent)
graph.add_node("devil", devilAgent)
graph.add_node("critic", criticAgent)
graph.add_node("writer", writerAgent)
graph.add_node("supervisor",supervisor_agent)
graph.add_edge(START, "research")
graph.add_edge("research", "supervisor")
graph.add_conditional_edges(
  "supervisor",
  route_after_supervisor
)
graph.add_edge("timeline", "devil")
graph.add_edge("timeline", "critic")
graph.add_edge("devil", "writer")
graph.add_edge("critic", "writer")
graph.add_edge("writer", END)

app = graph.compile()