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
# for classsifying agent
class StartupClassification(BaseModel):
    status: Literal["dead", "alive", "pre_launch"] = Field(description="The operational status of the startup")
    reasoning: str = Field(description="One sentence explaining the evidence used for classification")
    confidence_score: float = Field(description="Score from 0.0 to 1.0")