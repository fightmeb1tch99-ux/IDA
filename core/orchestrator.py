"""
IDA OS Orchestrator v3.0
Manages the ReAct cycle, multi-agent communication, and memory integration.
"""
import asyncio
from typing import Dict, Any, List
from logger import log_info, log_error, log_debug
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.browser import BrowserAgent
from brain import Brain
from memory_manager import MemoryManager

class Orchestrator:
    def __init__(self, brain: Brain, memory: MemoryManager):
        self.brain = brain
        self.memory = memory
        self.planner = PlannerAgent(brain)
        self.executor = ExecutorAgent(brain)
        self.browser = BrowserAgent(brain)
        self.agents = {
            "planner": self.planner,
            "executor": self.executor,
            "browser": self.browser
        }

    async def run(self, user_input: str):
        log_info(f"Orchestrator: Processing input: {user_input}")
        
        # 0. Context Retrieval
        context_data = self.memory.get_context(user_input)
        semantic_context = "\n".join(context_data.get("semantic_context", []))
        
        # 1. Thought phase
        thought = self.brain.generate_thought(f"Context: {semantic_context}\nUser: {user_input}")
        log_info(f"Orchestrator Thought: {thought}")
        
        # 2. Planning phase
        plan_result = await self.planner.run(user_input, context=thought)
        plan = plan_result.get("plan", [])
        log_info(f"Orchestrator Plan: {plan}")
        
        # 3. Execution phase (ReAct Loop)
        results = []
        for step in plan:
            log_info(f"Orchestrator: Executing step: {step}")
            
            # Determine which agent should handle the step
            # More aggressive browser detection
            browser_keywords = ["поиск", "найти", "сайт", "браузер", "гугл", "search", "browse", "url", "интернет", "internet", "новости", "news"]
            if any(kw in step.lower() for kw in browser_keywords):
                step_result = await self.browser.run(step, context=thought)
            else:
                step_result = await self.executor.run(step, context=thought)
                
            results.append(step_result)
            
        # 4. Synthesis
        final_response = self.brain.generate_response(
            user_input, 
            tool_result=str(results), 
            thought=thought
        )
        
        # 5. Memory update
        self.memory.save_interaction(
            user_input=user_input, 
            response=final_response, 
            thought=thought,
            metadata={"plan": plan, "execution_results": results}
        )
        
        return final_response

    def _detect_plugin(self, step: str) -> str:
        # Simple plugin detection logic
        for name in self.plugins.plugins.keys():
            if name in step.lower():
                return name
        return None
