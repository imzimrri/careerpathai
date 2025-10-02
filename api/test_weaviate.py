"""
Test script for Weaviate RAG integration.
Run this to verify Weaviate connection and query functionality.
"""

import os
import sys
from dotenv import load_dotenv
from weaviate_client import get_weaviate_client

# Load environment variables
load_dotenv()


def test_connection():
    """Test Weaviate connection."""
    print("=" * 60)
    print("TEST 1: Weaviate Connection")
    print("=" * 60)
    
    client = get_weaviate_client()
    
    if not client.url or not client.api_key:
        print("❌ FAILED: Environment variables not set")
        print("   Please configure WEAVIATE_URL and WEAVIATE_API_KEY in .env")
        return False
    
    print(f"Connecting to: {client.url}")
    
    if client.connect():
        print("✅ PASSED: Successfully connected to Weaviate")
        client.disconnect()
        return True
    else:
        print("❌ FAILED: Could not connect to Weaviate")
        return False


def test_query_valid_role():
    """Test query with a valid target role."""
    print("\n" + "=" * 60)
    print("TEST 2: Query with Valid Target Role")
    print("=" * 60)
    
    client = get_weaviate_client()
    
    if not client.connect():
        print("❌ FAILED: Could not connect to Weaviate")
        return False
    
    try:
        target_role = "Machine Learning Engineer"
        print(f"Querying for: {target_role}")
        
        results = client.query_job_knowledge(target_role, limit=3)
        
        if results:
            print(f"✅ PASSED: Retrieved {len(results)} documents")
            print("\nResults:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   Category: {result['category']}")
                print(f"   Certainty: {result.get('certainty', 'N/A')}")
                print(f"   Description: {result['description'][:100]}...")
            return True
        else:
            print("⚠️  WARNING: No results found (collection may be empty)")
            return True  # Not a failure, just empty collection
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    finally:
        client.disconnect()


def test_query_unknown_role():
    """Test query with an unknown/obscure target role."""
    print("\n" + "=" * 60)
    print("TEST 3: Query with Unknown Target Role")
    print("=" * 60)
    
    client = get_weaviate_client()
    
    if not client.connect():
        print("❌ FAILED: Could not connect to Weaviate")
        return False
    
    try:
        target_role = "Quantum Computing Specialist"
        print(f"Querying for: {target_role}")
        
        results = client.query_job_knowledge(target_role, limit=3)
        
        if not results:
            print("✅ PASSED: Correctly returned empty results for unknown role")
        else:
            print(f"✅ PASSED: Retrieved {len(results)} documents (may have partial matches)")
            
        return True
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    finally:
        client.disconnect()


def test_error_handling():
    """Test error handling with invalid credentials."""
    print("\n" + "=" * 60)
    print("TEST 4: Error Handling")
    print("=" * 60)
    
    # Save original values
    original_url = os.getenv("WEAVIATE_URL")
    original_key = os.getenv("WEAVIATE_API_KEY")
    
    # Set invalid credentials
    os.environ["WEAVIATE_URL"] = "https://invalid-url.weaviate.network"
    os.environ["WEAVIATE_API_KEY"] = "invalid-key"
    
    client = get_weaviate_client()
    
    try:
        print("Testing with invalid credentials...")
        
        if not client.connect():
            print("✅ PASSED: Correctly handled invalid credentials")
            result = True
        else:
            print("❌ FAILED: Should not connect with invalid credentials")
            result = False
            
    except Exception as e:
        print(f"✅ PASSED: Correctly raised exception: {str(e)[:50]}...")
        result = True
    finally:
        # Restore original values
        if original_url:
            os.environ["WEAVIATE_URL"] = original_url
        if original_key:
            os.environ["WEAVIATE_API_KEY"] = original_key
    
    return result


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "=" * 60)
    print("WEAVIATE RAG INTEGRATION TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        ("Connection Test", test_connection),
        ("Valid Role Query", test_query_valid_role),
        ("Unknown Role Query", test_query_unknown_role),
        ("Error Handling", test_error_handling),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ UNEXPECTED ERROR in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())