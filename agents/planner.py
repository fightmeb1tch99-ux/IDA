"""
Planner Agent for IDA OS v3.0
Breaks complex tasks into subtasks and manages the execution strategy.
"""
import json
import re
from typing import List, Dict, Any, Optional
from agents.base import BaseAgent
from brain import Brain
from logger import log_info, log_error, log_debug

class PlannerAgent(BaseAgent):
    def __init__(self, brain: Brain):
        super().__init__("Planner", brain)
        self.brain = brain

    async def run(self, task: str, context: str = "") -> Dict[str, Any]:
        log_info(f"[Planner - Task Architect] Planning task: {task}")
        
        prompt = f"Ты — PlannerAgent в IDA OS. Разбей задачу на список конкретных шагов. Ответь ТОЛЬКО в формате JSON списка строк, например: [\"найти новости\", \"составить отчет\"]. Задача: {task}"
        
        response = self.brain.generate_response(prompt)
        try:
            # If response is a fallback text, use the task as a single step
            if "Я выполнил задачу" in response or "Извини" in response:
                return {"plan": [task]}

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
            log_debug(f"[Planner] Using fallback plan due to parse error")
            return {"plan": [task]} # Fallback to single step
