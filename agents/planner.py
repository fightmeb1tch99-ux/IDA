"""
Planner Agent for IDA OS v3.0
Breaks complex tasks into subtasks and manages the execution strategy.
"""
import json
import re
from typing import List, Dict, Any, Optional
from agents.base import BaseAgent
from brain import Brain
from logger import log_info, log_error

class PlannerAgent(BaseAgent):
    def __init__(self, brain: Brain):
        super().__init__("Planner", brain)
        self.brain = brain

    async def run(self, task: str, context: str = "") -> Dict[str, Any]:
        log_info(f"[Planner - Task Architect] Planning task: {task}")
        
        prompt = f"""
        System: Ты — PlannerAgent в IDA OS. Разбей задачу на список конкретных шагов.
        Context: {context}
        Task: {task}
        
        Ответь ТОЛЬКО в формате JSON списка строк: ["шаг 1", "шаг 2"]
        """
        
        response = self.brain.generate_response(prompt)
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group())
            else:
                plan = json.loads(response)
            
            if not isinstance(plan, list):
                plan = [task]
                
            log_info("[Planner - Task Architect] Plan generated successfully")
            return {"plan": plan}
        except Exception as e:
            log_error(f"[Planner] Failed to parse plan: {response}", e)
            return {"plan": [task]} # Fallback to single step
