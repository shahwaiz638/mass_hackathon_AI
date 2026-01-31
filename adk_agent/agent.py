import vertexai
from .agent_tools import tools
from google.adk.agents import Agent, BaseAgent
from dotenv import load_dotenv
import os
from adk_agent.coordinator_agent import CoordinatorAgent
from adk_agent.estimated_price_output import EstimatedPriceOutput

load_dotenv()

project=os.getenv("GOOGLE_CLOUD_PROJECT")
location=os.getenv("GOOGLE_CLOUD_LOCATION")
vertexai.init(project=project, location=location)


SYSTEM_PROMPT = r"""
You are an estimation agent that helps recommend prices for the given jobs. Users will require labour work like
plumbing, electrical work, landscaping, cleaning, etc. Your task is to analyze the job details provided by the user
and recommend a competitive price based on market rates and the specifics of the job.

Sample Input:
what is the estimated price for plumbing a kitchen sink?

Sample Thought Process:
Its about $150 to $200 for plumbing a kitchen sink, considering labor and materials in New York, USA.

Sample Output:
{
  "estimated_price": "$150"
}

Sample Input 2:
What would be the estimated cost to landscape a 500 sq ft backyard in Calgary, Canada?

Sample Thought Process 2:
Landscaping a 500 sq ft backyard in Calgary typically costs between $3,000 to $5,000 CAD, depending on the design and materials used.

Sample Output 2:
{
    "estimated_price": "$3000"
}

make sure to use the minimum estimated price in your response. It should be a single value with a dollar sign.

""".strip()


# --- Register it during Agent creation ---
estimator_agent = Agent(
    name="estimation_agent",
    description="An estimation agent that helps recommend prices for various labour jobs based on market rates and job specifics.",
    model="gemini-2.5-pro",
    instruction=SYSTEM_PROMPT,
    tools=tools.tools,  
    output_key="estimated_price",
    output_schema=EstimatedPriceOutput
)

root_agent = CoordinatorAgent(
    estimator_agent=estimator_agent
)

