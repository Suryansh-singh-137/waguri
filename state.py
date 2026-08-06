from typing  import TypedDict
from pydantic import BaseModel, Field
from typing import Literal 
class Researchstate(TypedDict):
  startup_name  : str  
  research_findings:str 
  timeline :str 
  devil_argument :str 
  critics_argument :str 
  final_report:str  
  research_quality:str 
  research_attempts:int
  startup_status:str
  status_reasoning:str
  confidence_score:float
  core_concept:str
  market_competitors:str
  risk_simulation:str
# for classsifying agent
class StartupClassification(BaseModel):
    status: Literal["dead", "alive", "pre_launch"] = Field(description="The operational status of the startup")
    reasoning: str = Field(description="One sentence explaining the evidence used for classification")
    confidence_score: float = Field(description="Score from 0.0 to 1.0")
class IdeaValidationOutput(BaseModel):
    core_concept: str = Field(description="A clear, factual explanation of what the startup is building, their value proposition, and target audience.")
    market_competitors: str = Field(description="A summary of the market they are entering and specific named competitors.")   