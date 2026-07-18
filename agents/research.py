from dotenv import load_dotenv
load_dotenv()
import os 
from langchain_tavily import TavilySearch
from   state import Researchstate
from  llm  import llm
from langchain_core.messages import SystemMessage, HumanMessage 
tavily  =os.environ.get("TAVILY_API_KEY")
def researchAgent(state:Researchstate):
  tool   =TavilySearch(
    max_results=5,
    topic="general",
  )
 


