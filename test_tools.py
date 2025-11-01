#!/usr/bin/env python3
"""
Test script to verify all tools are working correctly.
"""

import os
from dotenv import load_dotenv
from tools import get_weather, get_location, get_time, calculate
import json

load_dotenv()

def test_tool(name, func, *args):
    """Test a tool function and print results."""
    print(f"\n{'='*80}")
    print(f"🧪 TESTING: {name}")
    print(f"{'='*80}\n")
    
    try:
        result = func(*args)
        result_dict = json.loads(result)
        
        if "error" in result_dict:
            print(f"❌ FAILED: {result_dict['error']}")
            return False
        else:
            print(f"✅ SUCCESS!")
            print(f"Result:\n{json.dumps(result_dict, indent=2)}")
            return True
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return False

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    🔧 TOOL TESTING SUITE 🔧                              ║
║                                                                           ║
║  Testing all available tools to verify functionality                      ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    results = {}
    
    # Test 1: Get Location (no parameters)
    print("\n📍 TEST 1: get_location()")
    results['location'] = test_tool("get_location", get_location)
    
    # Test 2: Get Time - UTC
    print("\n🕐 TEST 2: get_time('UTC')")
    results['time_utc'] = test_tool("get_time (UTC)", get_time, "UTC")
    
    # Test 3: Get Time - Tokyo
    print("\n🕐 TEST 3: get_time('Asia/Tokyo')")
    results['time_tokyo'] = test_tool("get_time (Tokyo)", get_time, "Asia/Tokyo")
    
    # Test 4: Get Time - New York
    print("\n🕐 TEST 4: get_time('America/New_York')")
    results['time_ny'] = test_tool("get_time (New York)", get_time, "America/New_York")
    
    # Test 5: Calculate - Simple
    print("\n🔢 TEST 5: calculate('25 * 4 + 100')")
    results['calc_simple'] = test_tool("calculate (simple)", calculate, "25 * 4 + 100")
    
    # Test 6: Calculate - Complex
    print("\n🔢 TEST 6: calculate('(100 + 50) * 2')")
    results['calc_complex'] = test_tool("calculate (complex)", calculate, "(100 + 50) * 2")
    
    # Test 7: Get Weather - London
    print("\n🌤️  TEST 7: get_weather('London')")
    results['weather'] = test_tool("get_weather", get_weather, "London")
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    working = [name for name, result in results.items() if result]
    broken = [name for name, result in results.items() if not result]
    
    print(f"\n✅ WORKING TOOLS ({len(working)}):")
    for tool in working:
        print(f"   • {tool}")
    
    print(f"\n❌ BROKEN TOOLS ({len(broken)}):")
    for tool in broken:
        print(f"   • {tool}")
    
    print("\n" + "="*80)
    
    if len(working) >= 3:
        print("\n✅ Good news! At least 3 tools are working!")
    else:
        print("\n⚠️  Warning: Less than 3 tools are working properly.")

if __name__ == "__main__":
    main()

