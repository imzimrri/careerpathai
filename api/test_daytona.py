"""
Test script for Daytona code validation integration.
Tests the complete workflow of code generation and validation.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from daytona_client import get_daytona_client

def test_python_validation():
    """Test Python code validation."""
    print("\n" + "="*60)
    print("TEST 1: Python Code Validation (Success Case)")
    print("="*60)
    
    client = get_daytona_client()
    
    python_code = """# Simple Python example
numbers = [1, 2, 3, 4, 5]
squared = [n**2 for n in numbers]
print(f"Squared numbers: {squared}")
"""
    
    result = client.validate_code_with_daytona(
        code=python_code,
        language="python",
        skill="Python Programming"
    )
    
    print(f"\n✓ Validation Result:")
    print(f"  Skill: {result['skill']}")
    print(f"  Status: {result['status']}")
    print(f"  Execution Time: {result['execution_time']}s")
    print(f"  Details: {result['details']}")
    if result['output']:
        print(f"  Output:\n{result['output']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    
    return result['status'] == "Success"


def test_javascript_validation():
    """Test JavaScript code validation."""
    print("\n" + "="*60)
    print("TEST 2: JavaScript Code Validation (Success Case)")
    print("="*60)
    
    client = get_daytona_client()
    
    js_code = """// Simple JavaScript example
const numbers = [1, 2, 3, 4, 5];
const squared = numbers.map(n => n ** 2);
console.log('Squared numbers:', squared);
"""
    
    result = client.validate_code_with_daytona(
        code=js_code,
        language="javascript",
        skill="JavaScript Programming"
    )
    
    print(f"\n✓ Validation Result:")
    print(f"  Skill: {result['skill']}")
    print(f"  Status: {result['status']}")
    print(f"  Execution Time: {result['execution_time']}s")
    print(f"  Details: {result['details']}")
    if result['output']:
        print(f"  Output:\n{result['output']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    
    return result['status'] == "Success"


def test_syntax_error():
    """Test code with syntax error."""
    print("\n" + "="*60)
    print("TEST 3: Python Code with Syntax Error (Failure Case)")
    print("="*60)
    
    client = get_daytona_client()
    
    bad_code = """# Python code with syntax error
print("Hello, World!"
"""
    
    result = client.validate_code_with_daytona(
        code=bad_code,
        language="python",
        skill="Python Programming"
    )
    
    print(f"\n✓ Validation Result:")
    print(f"  Skill: {result['skill']}")
    print(f"  Status: {result['status']}")
    print(f"  Execution Time: {result['execution_time']}s")
    print(f"  Details: {result['details']}")
    if result['output']:
        print(f"  Output:\n{result['output']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    
    return result['status'] == "Failure"


def test_runtime_error():
    """Test code with runtime error."""
    print("\n" + "="*60)
    print("TEST 4: Python Code with Runtime Error (Failure Case)")
    print("="*60)
    
    client = get_daytona_client()
    
    error_code = """# Python code with runtime error
x = 1 / 0
print("This won't print")
"""
    
    result = client.validate_code_with_daytona(
        code=error_code,
        language="python",
        skill="Python Programming"
    )
    
    print(f"\n✓ Validation Result:")
    print(f"  Skill: {result['skill']}")
    print(f"  Status: {result['status']}")
    print(f"  Execution Time: {result['execution_time']}s")
    print(f"  Details: {result['details']}")
    if result['output']:
        print(f"  Output:\n{result['output']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    
    return result['status'] == "Failure"


def test_machine_learning_code():
    """Test Machine Learning code example."""
    print("\n" + "="*60)
    print("TEST 5: Machine Learning Code (Real-world Example)")
    print("="*60)
    
    client = get_daytona_client()
    
    ml_code = """# Simple linear regression example
import numpy as np

# Sample data: hours studied vs exam score
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 5])

# Simple linear regression calculation
X_mean = np.mean(X)
y_mean = np.mean(y)
slope = np.sum((X - X_mean) * (y - y_mean)) / np.sum((X - X_mean) ** 2)
intercept = y_mean - slope * X_mean

# Predict for 6 hours
prediction = slope * 6 + intercept
print(f"Predicted score for 6 hours: {prediction:.2f}")
"""
    
    result = client.validate_code_with_daytona(
        code=ml_code,
        language="python",
        skill="Machine Learning"
    )
    
    print(f"\n✓ Validation Result:")
    print(f"  Skill: {result['skill']}")
    print(f"  Status: {result['status']}")
    print(f"  Execution Time: {result['execution_time']}s")
    print(f"  Details: {result['details']}")
    if result['output']:
        print(f"  Output:\n{result['output']}")
    if result['error']:
        print(f"  Error: {result['error']}")
    
    return result['status'] == "Success"


def test_fallback_behavior():
    """Test fallback behavior when API key is missing."""
    print("\n" + "="*60)
    print("TEST 6: Fallback Behavior (No API Key)")
    print("="*60)
    
    # Temporarily remove API key
    original_key = os.environ.get("DAYTONA_API_KEY")
    if original_key:
        del os.environ["DAYTONA_API_KEY"]
    
    client = get_daytona_client()
    
    result = client.validate_code_with_daytona(
        code="print('Hello')",
        language="python",
        skill="Python"
    )
    
    print(f"\n✓ Validation Result:")
    print(f"  Skill: {result['skill']}")
    print(f"  Status: {result['status']}")
    print(f"  Details: {result['details']}")
    
    # Restore API key
    if original_key:
        os.environ["DAYTONA_API_KEY"] = original_key
    
    return result['status'] == "Failure" and "unavailable" in result['details'].lower()


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("DAYTONA CODE VALIDATION TEST SUITE")
    print("="*60)
    
    # Check if API key is configured
    if not os.getenv("DAYTONA_API_KEY"):
        print("\n⚠️  WARNING: DAYTONA_API_KEY not found in environment")
        print("   Tests will use fallback behavior")
        print("   Set DAYTONA_API_KEY in .env file for full testing")
    
    tests = [
        ("Python Validation", test_python_validation),
        ("JavaScript Validation", test_javascript_validation),
        ("Syntax Error Handling", test_syntax_error),
        ("Runtime Error Handling", test_runtime_error),
        ("Machine Learning Code", test_machine_learning_code),
        ("Fallback Behavior", test_fallback_behavior),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n✗ Test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())