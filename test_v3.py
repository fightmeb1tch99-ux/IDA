"""
Test script for IDA OS v3.0
Tests Orchestrator, Memory, and Reasoning.
"""
import asyncio
import os
from main import IDAOS

async def test_os():
    print("--- Starting IDA OS v3.0 Test ---")
    os_instance = IDAOS()
    
    # Test 1: Simple reasoning and planning
    print("\nTest 1: Reasoning & Planning")
    response1 = await os_instance.process_input("Привет! Расскажи, какой сегодня план на день, если я хочу выучить Python?")
    print(f"Response: {response1}")
    
    # Test 2: Semantic Memory Search
    print("\nTest 2: Semantic Memory (Searching for Python plan)")
    context = os_instance.memory_manager.get_context("Python")
    print(f"Context Found: {context['semantic_context']}")
    
    # Test 3: Structured SQLite Storage
    print("\nTest 3: SQLite Storage Check")
    history = os_instance.memory_manager.db.get_recent_history(limit=5)
    print(f"Recent History from DB: {len(history)} items")

    # Test 4: Browser Automation
    print("\nTest 4: Browser Automation (Searching for IDA OS news)")
    response4 = await os_instance.process_input("Найди в интернете последние новости про искусственный интеллект за сегодня.")
    print(f"Browser Response: {response4}")

    # Test 5: Plugin System
    print("\nTest 5: Plugin System (Weather Plugin)")
    response5 = await os_instance.process_input("Какая сейчас погода в Москве?")
    print(f"Plugin Response: {response5}")
    
    print("\n--- Test Completed ---")

if __name__ == "__main__":
    asyncio.run(test_os())
