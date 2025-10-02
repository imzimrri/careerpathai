"""
Test script for aci.dev integration and tool calling functionality.
Tests the search_learning_content tool and aci.dev client.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools import search_learning_content, get_tool_definition
from aci_client import get_aci_client


def test_search_learning_content():
    """Test the search_learning_content tool function."""
    print("\n" + "="*70)
    print("TEST 1: search_learning_content Tool Function")
    print("="*70)
    
    test_skills = [
        "Python",
        "Machine Learning",
        "React",
        "Docker",
        "Unknown Skill"
    ]
    
    for skill in test_skills:
        print(f"\n{'─'*70}")
        print(f"Testing skill: {skill}")
        print(f"{'─'*70}")
        
        try:
            courses = search_learning_content(skill)
            print(f"✓ Found {len(courses)} courses")
            
            # Display first 2 courses
            for i, course in enumerate(courses[:2], 1):
                print(f"\n  {i}. {course['title']}")
                print(f"     Platform: {course['platform']}")
                print(f"     Duration: {course['duration']}")
                print(f"     Level: {course['level']}")
                print(f"     URL: {course['url'][:60]}...")
            
            if len(courses) > 2:
                print(f"\n  ... and {len(courses) - 2} more courses")
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    return True


def test_tool_definition():
    """Test the tool definition for function calling."""
    print("\n" + "="*70)
    print("TEST 2: Tool Definition")
    print("="*70)
    
    try:
        tool_def = get_tool_definition()
        print(f"\n✓ Tool definition retrieved successfully")
        print(f"  Type: {tool_def['type']}")
        print(f"  Function Name: {tool_def['function']['name']}")
        print(f"  Description: {tool_def['function']['description'][:80]}...")
        print(f"  Parameters: {list(tool_def['function']['parameters']['properties'].keys())}")
        print(f"  Required: {tool_def['function']['parameters']['required']}")
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_aci_client():
    """Test the aci.dev client."""
    print("\n" + "="*70)
    print("TEST 3: aci.dev Client")
    print("="*70)
    
    try:
        client = get_aci_client()
        print("✓ aci.dev client created")
        
        # Test connection validation
        if client.validate_connection():
            print("✓ Connection validated")
        else:
            print("⚠ Connection validation returned False (expected in mock mode)")
        
        # Test getting available tools
        tools = client.get_available_tools()
        print(f"✓ Available tools: {len(tools)}")
        for tool in tools:
            print(f"  - {tool['function']['name']}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_tool_execution():
    """Test executing a tool through the aci.dev client."""
    print("\n" + "="*70)
    print("TEST 4: Tool Execution")
    print("="*70)
    
    try:
        client = get_aci_client()
        
        # Test single tool execution
        print("\nExecuting tool: search_learning_content")
        result = client.execute_tool(
            "search_learning_content",
            {"skill": "Python"}
        )
        
        if result["success"]:
            print(f"✓ Tool executed successfully")
            courses = result["result"]
            print(f"  Found {len(courses)} courses")
            print(f"  First course: {courses[0]['title']}")
        else:
            print(f"✗ Tool execution failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_multi_skill_search():
    """Test searching courses for multiple skills."""
    print("\n" + "="*70)
    print("TEST 5: Multi-Skill Course Search")
    print("="*70)
    
    try:
        client = get_aci_client()
        
        skills = ["Python", "Machine Learning", "React"]
        print(f"\nSearching courses for {len(skills)} skills...")
        
        courses_by_skill = client.search_courses_for_skills(skills)
        
        print(f"✓ Successfully retrieved courses for {len(courses_by_skill)} skills")
        
        for skill, courses in courses_by_skill.items():
            print(f"\n  {skill}:")
            print(f"    - {len(courses)} courses found")
            print(f"    - Top course: {courses[0]['title']}")
            print(f"    - Platform: {courses[0]['platform']}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_error_handling():
    """Test error handling for invalid inputs."""
    print("\n" + "="*70)
    print("TEST 6: Error Handling")
    print("="*70)
    
    try:
        client = get_aci_client()
        
        # Test with invalid tool name
        print("\nTesting with invalid tool name...")
        try:
            client.execute_tool("invalid_tool", {"skill": "Python"})
            print("✗ Should have raised an error")
            return False
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {str(e)[:60]}...")
        
        # Test with missing arguments
        print("\nTesting with missing arguments...")
        try:
            client.execute_tool("search_learning_content", {})
            print("✗ Should have raised an error")
            return False
        except Exception as e:
            print(f"✓ Correctly raised error: {str(e)[:60]}...")
        
        return True
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*70)
    print("RUNNING ACI.DEV INTEGRATION TESTS")
    print("="*70)
    
    tests = [
        ("Search Learning Content", test_search_learning_content),
        ("Tool Definition", test_tool_definition),
        ("aci.dev Client", test_aci_client),
        ("Tool Execution", test_tool_execution),
        ("Multi-Skill Search", test_multi_skill_search),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)