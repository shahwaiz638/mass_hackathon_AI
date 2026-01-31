import json
import logging
from google.adk.agents import BaseAgent
from typing import Any, AsyncGenerator
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.genai import types
from pydantic import PrivateAttr

class CoordinatorAgent(BaseAgent):
    """
    Author: Shahwaiz.memon@scalateams.com
    
    Coordinator Agent that orchestrates between intent, search, PIM, and chat agents
    to handle PIM attribute operations for all workflows: Create, Update, Delete, 
    Rollback, and Retrieve.
    """
    _estimator_agent: Any = PrivateAttr()
    
    def __init__(self, estimator_agent):
        sub_agents = [agent for agent in [estimator_agent] if agent is not None]
        super().__init__(
            name="Coordinator_Agent",
            sub_agents=sub_agents
        )
        self._estimator_agent = estimator_agent
        
    # Helper methods have been moved to agent_helpers.py
    
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:

        async for evt in self._estimator_agent.run_async(ctx):
            yield evt

        # Try to parse the LLM output as JSON and wrap result in an Event
        estimated_price = "$0"
        if evt and getattr(evt, 'content', None) and evt.content.parts:
            text = (evt.content.parts[0].text or "").strip()
            try:
                data = json.loads(text)
                if "estimated_price" in data:
                    estimated_price = data["estimated_price"]
            except json.JSONDecodeError:
                pass

        content = types.Content(parts=[types.Part(estimated_price)])
        out_event = Event(author=self.name or "Coordinator_Agent", content=content)
        yield out_event

        
        