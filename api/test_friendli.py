"""
Test script for FriendliAI integration.
Validates connection, authentication, and skill gap analysis functionality.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import clients
from friendli_client import get_friendli_client
from weaviate_client import get_weaviate_client


def test_friendli_connection():
    """Test FriendliAI connection and authentication."""
    print("\n" + "="*60)
    print("TEST 1: FriendliAI Connection & Authentication")
    print("="*60)
    
    client = get_friendli_client()
    
    if not client.api_key:
        print("❌ FAILED: FRIENDLI_TOKEN not found in environment")
        return False
    
    print(f"✓ Token configured: {client.api_key[:10]}...")
    print(f"✓ Model configured: {client.model}")
    
    print("\nValidating connection...")
    if client.validate_connection():
        print("✅ PASSED: Successfully connected to FriendliAI API")
        return True
    else:
        print("❌ FAILED: Could not validate FriendliAI connection")
        return False


def test_skill_gap_analysis_with_mock_data():
    """Test skill gap analysis with mock data."""
    print("\n" + "="*60)
    print("TEST 2: Skill Gap Analysis (Mock Data)")
    print("="*60)
    
    client = get_friendli_client()
    
    # Mock knowledge documents
    mock_docs = [
        {
            "title": "Machine Learning Engineer",
            "description": "Requires strong Python programming skills, deep understanding of machine learning algorithms, experience with frameworks like TensorFlow and PyTorch, and knowledge of data preprocessing and model deployment.",
            "category": "Technical Skills"
        },
        {
            "title": "Data Science Fundamentals",
            "description": "Statistical analysis, data visualization with tools like Matplotlib and Seaborn, predictive modeling, and experience with pandas and NumPy are essential.",
            "category": "Core Competencies"
        },
        {
            "title": "Deep Learning Specialization",
            "description": "Understanding of neural networks, CNNs, RNNs, transformers, and experience with GPU computing and model optimization techniques.",
            "category": "Advanced Skills"
        }
    ]
    
    current_role = "Frontend Developer"
    target_role = "Machine Learning Engineer"
    
    print(f"\nCurrent Role: {current_role}")
    print(f"Target Role: {target_role}")
    print(f"Knowledge Documents: {len(mock_docs)}")
    
    try:
        print("\nAnalyzing skill gap...")
        skills = client.analyze_skill_gap(
            current_role=current_role,
            target_role=target_role,
            knowledge_docs=mock_docs
        )
        
        print(f"\n✅ PASSED: Successfully identified {len(skills)} skills")
        print("\nTop 3 Skills to Learn:")
        for i, skill in enumerate(skills, 1):
            print(f"  {i}. {skill}")
        
        # Validate response
        if len(skills) != 3:
            print(f"\n⚠️  WARNING: Expected 3 skills, got {len(skills)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {str(e)}")
        return False


def test_skill_gap_analysis_with_weaviate():
    """Test skill gap analysis with real Weaviate data."""
    print("\n" + "="*60)
    print("TEST 3: Skill Gap Analysis (Weaviate Integration)")
    print("="*60)
    
    # Initialize clients
    weaviate_client = get_weaviate_client()
    friendli_client = get_friendli_client()
    
    current_role = "Backend Developer"
    target_role = "DevOps Engineer"
    
    print(f"\nCurrent Role: {current_role}")
    print(f"Target Role: {target_role}")
    
    try:
        # Connect to Weaviate
        print("\nConnecting to Weaviate...")
        if not weaviate_client.connect():
            print("❌ FAILED: Could not connect to Weaviate")
            return False
        
        print("✓ Connected to Weaviate")
        
        # Query job knowledge
        print(f"\nQuerying knowledge for: {target_role}")
        job_knowledge = weaviate_client.query_job_knowledge(
            target_role=target_role,
            limit=5,
            certainty=0.7
        )
        
        print(f"✓ Retrieved {len(job_knowledge)} documents")
        
        if job_knowledge:
            print("\nSample documents:")
            for i, doc in enumerate(job_knowledge[:2], 1):
                print(f"  {i}. {doc['title']} ({doc['category']})")
        
        # Analyze skill gap
        print("\nAnalyzing skill gap with FriendliAI...")
        skills = friendli_client.analyze_skill_gap(
            current_role=current_role,
            target_role=target_role,
            knowledge_docs=job_knowledge
        )
        
        print(f"\n✅ PASSED: Successfully identified {len(skills)} skills")
        print("\nTop 3 Skills to Learn:")
        for i, skill in enumerate(skills, 1):
            print(f"  {i}. {skill}")
        
        weaviate_client.disconnect()
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {str(e)}")
        if weaviate_client:
            weaviate_client.disconnect()
        return False


def test_error_handling():
    """Test error handling scenarios."""
    print("\n" + "="*60)
    print("TEST 4: Error Handling")
    print("="*60)
    
    client = get_friendli_client()
    
    # Test with empty knowledge docs
    print("\nTest 4a: Empty knowledge documents")
    try:
        skills = client.analyze_skill_gap(
            current_role="Developer",
            target_role="Engineer",
            knowledge_docs=[]
        )
        print(f"✓ Handled empty docs: {len(skills)} skills returned")
    except Exception as e:
        print(f"✓ Properly raised exception: {str(e)[:50]}...")
    
    # Test with same roles
    print("\nTest 4b: Same current and target role")
    try:
        skills = client.analyze_skill_gap(
            current_role="Software Engineer",
            target_role="Software Engineer",
            knowledge_docs=[{"title": "Test", "description": "Test", "category": "Test"}]
        )
        print(f"✓ Handled same roles: {len(skills)} skills returned")
    except Exception as e:
        print(f"✓ Properly raised exception: {str(e)[:50]}...")
    
    print("\n✅ PASSED: Error handling tests completed")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("FRIENDLIAI INTEGRATION TEST SUITE")
    print("="*60)
    
    # Check environment variables
    if not os.getenv("FRIENDLI_TOKEN"):
        print("\n❌ ERROR: FRIENDLI_TOKEN not found in environment")
        print("Please add your FriendliAI token to the .env file")
        sys.exit(1)
    
    results = []
    
    # Run tests
    results.append(("Connection Test", test_friendli_connection()))
    results.append(("Mock Data Test", test_skill_gap_analysis_with_mock_data()))
    results.append(("Weaviate Integration Test", test_skill_gap_analysis_with_weaviate()))
    results.append(("Error Handling Test", test_error_handling()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()