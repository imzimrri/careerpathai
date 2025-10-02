"""
Test script for Comet (Opik) observability integration.
Tests the complete workflow tracing and logging.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comet_client import get_comet_client


def test_trace_creation():
    """Test basic trace creation."""
    print("\n" + "="*60)
    print("TEST 1: Basic Trace Creation")
    print("="*60)
    
    client = get_comet_client()
    
    with client.trace_request("test_career_path", {
        "current_role": "Frontend Developer",
        "target_role": "ML Engineer"
    }) as trace:
        print("✓ Trace created successfully")
        
        # Simulate workflow steps
        client.log_weaviate_query(
            target_role="ML Engineer",
            limit=5,
            certainty=0.7,
            documents=[
                {"title": "ML Engineer Role", "category": "Job Roles"},
                {"title": "Python for ML", "category": "Skills"}
            ],
            latency=0.5
        )
        print("✓ Logged Weaviate query")
        
        client.log_friendli_analysis(
            current_role="Frontend Developer",
            target_role="ML Engineer",
            skills=["Machine Learning", "Python", "TensorFlow"],
            latency=2.3,
            token_usage={"prompt": 450, "completion": 120}
        )
        print("✓ Logged FriendliAI analysis")
        
        client.log_aci_course_search(
            skills=["Machine Learning", "Python", "TensorFlow"],
            courses_by_skill={
                "Machine Learning": [{"title": "ML Course 1"}, {"title": "ML Course 2"}],
                "Python": [{"title": "Python Course 1"}],
                "TensorFlow": [{"title": "TF Course 1"}]
            },
            latency=1.2
        )
        print("✓ Logged aci.dev course search")
        
        client.log_code_generation(
            skill="Machine Learning",
            code="import numpy as np\nprint('Hello ML')",
            language="python",
            description="Simple ML example",
            latency=1.5
        )
        print("✓ Logged code generation")
        
        client.log_daytona_validation(
            code="import numpy as np\nprint('Hello ML')",
            language="python",
            skill="Machine Learning",
            validation_result={
                "status": "Success",
                "output": "Hello ML\n",
                "error": None,
                "execution_time": 0.234,
                "details": "Code executed successfully"
            },
            latency=0.9
        )
        print("✓ Logged Daytona validation")
    
    print("\n✓ Trace finalized successfully")
    return True


def test_error_logging():
    """Test error logging."""
    print("\n" + "="*60)
    print("TEST 2: Error Logging")
    print("="*60)
    
    client = get_comet_client()
    
    with client.trace_request("test_error_handling", {
        "current_role": "Frontend Developer",
        "target_role": "ML Engineer"
    }) as trace:
        print("✓ Trace created")
        
        # Log an error
        client.log_error(
            component="test_component",
            error_message="Test error message",
            error_type="TestError"
        )
        print("✓ Error logged successfully")
    
    print("✓ Error trace finalized")
    return True


def test_fallback_behavior():
    """Test fallback behavior when Opik is not available."""
    print("\n" + "="*60)
    print("TEST 3: Fallback Behavior (No API Key)")
    print("="*60)
    
    # Temporarily remove API key
    original_key = os.environ.get("COMET_API_KEY")
    if original_key:
        del os.environ["COMET_API_KEY"]
    
    client = get_comet_client()
    
    with client.trace_request("test_fallback", {
        "current_role": "Frontend Developer",
        "target_role": "ML Engineer"
    }) as trace:
        print("✓ Trace context works without API key")
        
        client.log_weaviate_query(
            target_role="ML Engineer",
            limit=5,
            certainty=0.7,
            documents=[],
            latency=0.5
        )
        print("✓ Logging skipped gracefully")
    
    # Restore API key
    if original_key:
        os.environ["COMET_API_KEY"] = original_key
    
    print("✓ Fallback behavior working correctly")
    return True


def test_performance_overhead():
    """Test that logging doesn't significantly impact performance."""
    print("\n" + "="*60)
    print("TEST 4: Performance Overhead")
    print("="*60)
    
    import time
    
    client = get_comet_client()
    
    # Measure time with logging
    start = time.time()
    with client.trace_request("test_performance", {
        "current_role": "Frontend Developer",
        "target_role": "ML Engineer"
    }) as trace:
        # Simulate some work
        time.sleep(0.01)
        
        client.log_weaviate_query(
            target_role="ML Engineer",
            limit=5,
            certainty=0.7,
            documents=[{"title": "Test"}],
            latency=0.5
        )
    
    overhead = time.time() - start - 0.01  # Subtract simulated work time
    
    print(f"✓ Logging overhead: {overhead*1000:.2f}ms")
    
    if overhead < 0.1:  # Less than 100ms
        print("✓ Performance overhead is acceptable")
        return True
    else:
        print(f"⚠️  Performance overhead is high: {overhead*1000:.2f}ms")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("COMET OBSERVABILITY TEST SUITE")
    print("="*60)
    
    # Check if API key is configured
    if not os.getenv("COMET_API_KEY"):
        print("\n⚠️  WARNING: COMET_API_KEY not found in environment")
        print("   Tests will use fallback behavior")
        print("   Set COMET_API_KEY in .env file for full testing")
    
    tests = [
        ("Trace Creation", test_trace_creation),
        ("Error Logging", test_error_logging),
        ("Fallback Behavior", test_fallback_behavior),
        ("Performance Overhead", test_performance_overhead),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n✗ Test failed with exception: {str(e)}")
            import traceback
            traceback.print_exc()
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
        print("\nNext steps:")
        print("1. Check Comet dashboard for traces")
        print("2. Verify all spans are logged correctly")
        print("3. Test end-to-end workflow with real API")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())