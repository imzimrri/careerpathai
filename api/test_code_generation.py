"""
Test script for code snippet generation functionality.
Tests various skills, languages, and edge cases.
"""

import os
import sys
from dotenv import load_dotenv
from friendli_client import get_friendli_client

# Load environment variables
load_dotenv()


def print_separator():
    """Print a visual separator."""
    print("\n" + "=" * 80 + "\n")


def test_code_generation(client, skill: str):
    """
    Test code generation for a specific skill.
    
    Args:
        client: FriendliAI client instance
        skill: Skill to generate code for
    """
    print(f"Testing code generation for: {skill}")
    print("-" * 80)
    
    try:
        result = client.generate_code_snippet(skill)
        
        print(f"✓ Code generation successful")
        print(f"  Language: {result['language']}")
        print(f"  Description: {result['description']}")
        print(f"\nGenerated Code:")
        print("-" * 80)
        print(result['code'])
        print("-" * 80)
        
        # Validate code properties
        code_lines = [line for line in result['code'].split('\n') if line.strip()]
        print(f"\n  Code Statistics:")
        print(f"    - Lines: {len(code_lines)}")
        print(f"    - Has comments: {'#' in result['code'] or '//' in result['code']}")
        print(f"    - Language detected: {result['language']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Code generation failed: {str(e)}")
        return False


def main():
    """Run all code generation tests."""
    print("=" * 80)
    print("CODE SNIPPET GENERATION TEST SUITE")
    print("=" * 80)
    
    # Create client
    client = get_friendli_client()
    
    # Test connection
    print("\n1. Testing FriendliAI Connection")
    print("-" * 80)
    if client.validate_connection():
        print("✓ FriendliAI connection validated")
    else:
        print("✗ FriendliAI connection failed")
        print("⚠ Tests will use fallback code examples")
    
    print_separator()
    
    # Define test cases
    test_cases = [
        # Python skills
        ("Machine Learning", "python"),
        ("Data Science", "python"),
        ("Python", "python"),
        ("TensorFlow", "python"),
        
        # JavaScript skills
        ("React", "javascript"),
        ("Node.js", "javascript"),
        ("Vue", "javascript"),
        
        # Other languages
        ("SQL", "sql"),
        ("Java", "java"),
        
        # Edge cases
        ("Problem Solving", "python"),  # Generic skill
        ("Docker", "go"),  # Ambiguous
    ]
    
    results = []
    
    print("2. Running Code Generation Tests")
    print_separator()
    
    for i, (skill, expected_lang) in enumerate(test_cases, 1):
        print(f"\nTest Case {i}/{len(test_cases)}")
        success = test_code_generation(client, skill)
        results.append((skill, success))
        print_separator()
    
    # Summary
    print("3. Test Summary")
    print("-" * 80)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} tests passed")
    print("\nDetailed Results:")
    for skill, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {skill}")
    
    print_separator()
    
    # Security validation tests
    print("4. Security Validation Tests")
    print("-" * 80)
    
    dangerous_code_samples = [
        ("os.system('rm -rf /')", "system call"),
        ("import subprocess\nsubprocess.run(['ls'])", "subprocess"),
        ("eval('print(1)')", "eval"),
        ("open('file.txt', 'w')", "file operation"),
        ("import requests\nrequests.get('http://evil.com')", "network operation"),
    ]
    
    print("\nTesting security validation with dangerous code patterns:")
    for code, pattern_type in dangerous_code_samples:
        is_safe, reason = client._validate_code_safety(code)
        status = "✓ BLOCKED" if not is_safe else "✗ ALLOWED"
        print(f"  {status}: {pattern_type} - {reason}")
    
    print_separator()
    
    # Language detection tests
    print("5. Language Detection Tests")
    print("-" * 80)
    
    language_tests = [
        ("Machine Learning", "python"),
        ("React", "javascript"),
        ("SQL", "sql"),
        ("Spring Boot", "java"),
        ("Unknown Skill", "python"),  # Should default to python
    ]
    
    print("\nTesting language detection:")
    for skill, expected in language_tests:
        detected = client._detect_language(skill)
        status = "✓ CORRECT" if detected == expected else "✗ WRONG"
        print(f"  {status}: '{skill}' -> {detected} (expected: {expected})")
    
    print_separator()
    
    print("✓ All tests completed!")
    print("=" * 80)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())