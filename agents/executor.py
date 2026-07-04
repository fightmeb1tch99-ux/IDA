"""
Executor Agent for IDA OS
Responsible for executing specific tasks using available tools.
"""
from agents.base import BaseAgent
from logger import log_info, log_error
from tools.tools import TOOLS

class ExecutorAgent(BaseAgent):
    def __init__(self, brain):
        super().__init__("Executor", brain)
        self.brain = brain

    async def run(self, task: str, context: str = ""):
        log_info(f"Executor: Executing task: {task}")
        
        # Decide which tool to use
        # For now, we reuse the brain's tool selection logic
        tool_name, arg = self.brain.decide_tool(task)
        
        if tool_name and tool_name in TOOLS:
            try:
                tool_fn = TOOLS[tool_name]
                result = tool_fn(arg) if arg is not None else tool_fn()
                return {"status": "success", "result": result, "tool": tool_name}
            except Exception as e:
                log_error(f"Executor tool failed: {tool_name}", e)
                return {"status": "error", "message": str(e)}
        
        # If no tool, generate a direct response
        response = self.brain.generate_response(task, thought=context)
        return {"status": "success", "result": response, "tool": None}
