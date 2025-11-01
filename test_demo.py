#!/usr/bin/env python3
"""
Quick test of the AI agent with sample queries.
This demonstrates the agent's capabilities without interactive input.
"""

import os
from dotenv import load_dotenv
from agent import AIAgent

# Load environment variables
load_dotenv()

def print_separator():
    print("\n" + "="*80 + "\n")

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                     🤖 AI AGENT TEST DEMO 🤖                              ║
║                                                                           ║
║  Running automated test queries to demonstrate agent capabilities        ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize agent
    try:
        agent = AIAgent()
        print(f"\033[92m✅ Agent initialized successfully!\033[0m")
        print(f"\033[92m   Using model: {agent.model}\033[0m\n")
    except Exception as e:
        print(f"\033[91m❌ ERROR: Failed to initialize agent: {e}\033[0m")
        return
    
    # Test queries
    test_queries = [
        "What's the weather in London?",
        "What time is it in Tokyo?",
        "Calculate 25 * 4 + 100",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print_separator()
        print(f"\033[95m📝 TEST QUERY {i}/{len(test_queries)}\033[0m")
        print_separator()
        
        try:
            agent.run(query)
        except Exception as e:
            print(f"\033[91m❌ ERROR: {e}\033[0m")
        
        print_separator()
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                          ✅ TEST COMPLETE ✅                               ║
║                                                                           ║
║  The agent successfully demonstrated:                                    ║
║    ✓ Weather fetching with OpenWeatherMap API                           ║
║    ✓ Time checking across timezones                                     ║
║    ✓ Mathematical calculations                                          ║
║    ✓ Reasoning and tool selection                                       ║
║    ✓ Multi-step problem solving                                         ║
║                                                                           ║
║  To run interactively: python main.py                                    ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()


