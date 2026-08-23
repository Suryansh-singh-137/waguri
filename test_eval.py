import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval, FaithfulnessMetric

load_dotenv()

# --- 1. Define the Custom Groq LLM Wrapper ---
class GroqEvaluator(DeepEvalBaseLLM):
    def __init__(self, model_name: str = "openai/gpt-oss-120b"):
        self.model_name = model_name
        # Initialize the LangChain Groq client
        self.chat_model = ChatGroq(model_name=self.model_name, temperature=0.0,max_tokens = 8000)

    def load_model(self):
        return self.chat_model

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        return chat_model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        # DeepEval runs asynchronously by default, so it needs this method
        chat_model = self.load_model()
        res = await chat_model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return self.model_name

# --- 2. The Evaluation Test Suite ---
def load_test_case():
    with open("latest_eval_data.json", "r") as f:
        return json.load(f)

def test_correctness():
    data = load_test_case()
    
    # Initialize our custom Groq model
    groq_judge = GroqEvaluator("openai/gpt-oss-120b")
    
    # Pass 'groq_judge' directly to the model parameter instead of 'gpt-4o'
    vc_structure_metric = GEval(
        name="VC Report Structure & Tone",
        criteria="Determine if the report uses professional financial/VC terminology, includes actionable insights, and follows required markdown headers.",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.7,
        model=groq_judge
    )
    
    faithfulness = FaithfulnessMetric(
        threshold=0.7,
        model=groq_judge, 
        include_reason=True
    )
    
    test_case = LLMTestCase(
        input=data["input"],
        actual_output=data["actual_output"],
        retrieval_context=data["retrieval_context"]
    )
    
    assert_test(test_case, [vc_structure_metric, faithfulness])