"""
Unit tests for the multi-agent layer (planner / executor).
"""
import asyncio
from unittest.mock import Mock

import pytest

from agents.base import BaseAgent
from agents.executor import ExecutorAgent
from agents.planner import PlannerAgent


def test_base_agent_is_abstract():
    with pytest.raises(TypeError):
        BaseAgent("x")


class TestPlannerAgent:
    def test_parses_json_list_plan(self):
        brain = Mock()
        brain.generate_response.return_value = '["find news", "write report"]'
        planner = PlannerAgent(brain)
        result = asyncio.run(planner.run("do research"))
        assert result["plan"] == ["find news", "write report"]

    def test_extracts_json_embedded_in_text(self):
        brain = Mock()
        brain.generate_response.return_value = 'Here is the plan: ["step one", "step two"] done'
        planner = PlannerAgent(brain)
        result = asyncio.run(planner.run("task"))
        assert result["plan"] == ["step one", "step two"]

    def test_falls_back_to_single_step_on_invalid_json(self):
        brain = Mock()
        brain.generate_response.return_value = "not json at all"
        planner = PlannerAgent(brain)
        result = asyncio.run(planner.run("my task"))
        assert result["plan"] == ["my task"]


class TestExecutorAgent:
    def test_runs_selected_tool(self):
        brain = Mock()
        brain.decide_tool.return_value = ("time", None)
        executor = ExecutorAgent(brain)
        result = asyncio.run(executor.run("what time is it"))
        assert result["status"] == "success"
        assert result["tool"] == "time"

    def test_falls_back_to_direct_response_without_tool(self):
        brain = Mock()
        brain.decide_tool.return_value = (None, None)
        brain.generate_response.return_value = "a direct answer"
        executor = ExecutorAgent(brain)
        result = asyncio.run(executor.run("tell me a joke"))
        assert result["status"] == "success"
        assert result["tool"] is None
        assert result["result"] == "a direct answer"

    def test_handles_unknown_tool_gracefully(self):
        brain = Mock()
        brain.decide_tool.return_value = ("no_such_tool", "arg")
        brain.generate_response.return_value = "fallback"
        executor = ExecutorAgent(brain)
        result = asyncio.run(executor.run("do something"))
        assert result["status"] == "success"
        assert result["tool"] is None
