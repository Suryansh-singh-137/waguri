from langgraph.graph import StateGraph, START, END
from state import Researchstate
from agents.research import research_agent
from agents.timeline import timelineAgent
from agents.critics import criticAgent
from agents.devil import devilAgent
from agents.writer import writerAgent
from agents.classifier import classifierAgent
from agents.supervisor import supervisor_agent
from agents.idea_validator import ideaValidatorAgent
from agents.risk_simulator import riskSimulatorAgent
from agents.pre_mortem_writer import preMortemWriterAgent
from  agents.market import marketAgent
from  agents.traction import tractionAgent
from  agents.progress_writer import progressWriterAgent
from  langgraph.checkpoint.memory import MemorySaver



def route_after_supervisor(state: Researchstate):
    quality = state.get('research_quality')
    if quality == "sufficient":
        return "timeline"
    else:
        return "research"

def route_by_status(state: Researchstate) -> str:
    status = state.get("startup_status", "dead")
    
    if status == "dead":
        return "research" 
    elif status == "alive":
        return ["traction", "market"]
    elif status == "pre_launch":
        return "pre_mortem_flow"
        
    return "research" # Safety fallback

graph = StateGraph(Researchstate)

#  Initialize the checkpointer
memory = MemorySaver()


# Add all nodes
graph.add_node("classifier", classifierAgent)
graph.add_node("research", research_agent)
graph.add_node("timeline", timelineAgent)
graph.add_node("devil", devilAgent)
graph.add_node("critic", criticAgent)
graph.add_node("writer", writerAgent)
graph.add_node("supervisor", supervisor_agent)
graph.add_node("idea_validator", ideaValidatorAgent)
graph.add_node("risk_simulator", riskSimulatorAgent)
graph.add_node("pre_mortem_writer", preMortemWriterAgent)


graph.add_node("traction", tractionAgent)
graph.add_node("market", marketAgent)
graph.add_node("progress_writer", progressWriterAgent)


# Graph Wiring
graph.add_edge(START, "classifier")

graph.add_conditional_edges(
    "classifier", 
    route_by_status,
    {
        "research": "research",             
        "traction": "traction",
        "market": "market",      
        "pre_mortem_flow": "idea_validator" 
    }
)


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

graph.add_edge("traction", "progress_writer")
graph.add_edge("market", "progress_writer")
graph.add_edge("idea_validator", "risk_simulator")
graph.add_edge("risk_simulator", "pre_mortem_writer")
graph.add_edge("pre_mortem_writer", END)
graph.add_edge("progress_writer", END)

app = graph.compile(
    checkpointer=memory,
    interrupt_after=["classifier"] 
)