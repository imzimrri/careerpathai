"""
Daytona client module for secure code validation.
Implements sandbox execution of generated code snippets using Daytona SDK.
"""

import os
import time
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Daytona SDK
try:
    from daytona import Daytona, DaytonaConfig
    DAYTONA_SDK_AVAILABLE = True
except ImportError:
    logger.warning("Daytona SDK not installed. Install with: pip install daytona-sdk")
    DAYTONA_SDK_AVAILABLE = False

# Configuration - will be loaded after dotenv in __init__
DAYTONA_API_KEY = None
EXECUTION_TIMEOUT = 30

# Fallback validation result
def get_fallback_validation(skill: str, reason: str = "Validation unavailable") -> Dict[str, Any]:
    """
    Generate a fallback validation result when Daytona is unavailable.
    
    Args:
        skill: The skill being validated
        reason: Reason for fallback
    
    Returns:
        Dictionary with fallback validation result
    """
    return {
        "skill": skill,
        "status": "Failure",
        "output": "",
        "error": None,
        "execution_time": 0.0,
        "details": f"Code validation unavailable - {reason}"
    }


class DaytonaClient:
    """
    Client for interacting with Daytona SDK for secure code execution.
    Handles sandbox creation, code execution, and cleanup.
    """
    
    def __init__(self):
        """Initialize Daytona client with environment configuration."""
        # Load API key from environment at runtime, not at module import time
        self.api_key = os.getenv("DAYTONA_API_KEY")
        self.timeout = int(os.getenv("DAYTONA_TIMEOUT", "30"))
        self.daytona = None
        
        if not self.api_key:
            logger.warning("Daytona API key not found in environment variables")
        elif not DAYTONA_SDK_AVAILABLE:
            logger.warning("Daytona SDK not available")
        else:
            try:
                # Initialize Daytona SDK
                config = DaytonaConfig(api_key=self.api_key)
                self.daytona = Daytona(config)
                logger.info("Daytona SDK initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Daytona SDK: {str(e)}")
                self.daytona = None
    
    def validate_code_with_daytona(
        self,
        code: str,
        language: str,
        skill: str
    ) -> Dict[str, Any]:
        """
        Validate code snippet using Daytona sandbox.
        
        This method creates a sandbox, executes the code, captures results,
        and cleans up resources. It implements comprehensive error handling
        and fallback mechanisms.
        
        Args:
            code: The code snippet to validate
            language: Programming language (python, javascript, etc.)
            skill: The skill being demonstrated
        
        Returns:
            Dictionary with validation results:
                - skill: str - The skill being validated
                - status: str - "Success" or "Failure"
                - output: str - stdout from execution
                - error: Optional[str] - stderr if any
                - execution_time: float - Time in seconds
                - details: str - Human-readable summary
        """
        if not self.api_key:
            logger.warning("Daytona API key not configured, using fallback")
            return get_fallback_validation(skill, "API key not configured")
        
        if not DAYTONA_SDK_AVAILABLE:
            logger.warning("Daytona SDK not available, using fallback")
            return get_fallback_validation(skill, "SDK not installed")
        
        if not self.daytona:
            logger.warning("Daytona client not initialized, using fallback")
            return get_fallback_validation(skill, "Client initialization failed")
        
        sandbox = None
        start_time = time.time()
        
        try:
            # Step 1: Create sandbox
            logger.info(f"Creating Daytona sandbox for {language} code")
            sandbox = self.daytona.create()
            logger.info(f"Sandbox created successfully")
            
            # Step 2: Execute code
            logger.info(f"Executing code in sandbox")
            response = sandbox.process.code_run(code)
            
            # Step 3: Calculate execution time
            execution_time = time.time() - start_time
            
            # Step 4: Parse and format results
            if response.exit_code == 0:
                logger.info(f"Code executed successfully")
                return {
                    "skill": skill,
                    "status": "Success",
                    "output": response.result or "",
                    "error": None,
                    "execution_time": round(execution_time, 3),
                    "details": f"Code executed successfully in {execution_time:.2f} seconds"
                }
            else:
                logger.warning(f"Code execution failed with exit code: {response.exit_code}")
                return {
                    "skill": skill,
                    "status": "Failure",
                    "output": response.result or "",
                    "error": f"Exit code: {response.exit_code}",
                    "execution_time": round(execution_time, 3),
                    "details": f"Code execution failed with exit code {response.exit_code}"
                }
        
        except TimeoutError:
            logger.error("Code execution timed out")
            return {
                "skill": skill,
                "status": "Failure",
                "output": "",
                "error": "Execution timeout",
                "execution_time": self.timeout,
                "details": f"Code execution exceeded {self.timeout} second timeout"
            }
        
        except Exception as e:
            logger.error(f"Error validating code with Daytona: {str(e)}")
            execution_time = time.time() - start_time
            return {
                "skill": skill,
                "status": "Failure",
                "output": "",
                "error": str(e),
                "execution_time": round(execution_time, 3),
                "details": f"Validation error: {str(e)}"
            }
        
        finally:
            # Always cleanup sandbox
            if sandbox:
                try:
                    # Use stop() method to cleanup sandbox
                    sandbox.stop()
                    logger.info(f"Sandbox cleaned up successfully")
                except Exception as e:
                    logger.error(f"Failed to cleanup sandbox: {str(e)}")


def get_daytona_client() -> DaytonaClient:
    """
    Factory function to create and return a Daytona client instance.
    
    Returns:
        DaytonaClient: Configured Daytona client instance
    """
    return DaytonaClient()


# Example usage and testing
if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create client
    client = get_daytona_client()
    
    # Test Python code validation
    python_code = """# Simple Python example
numbers = [1, 2, 3, 4, 5]
squared = [n**2 for n in numbers]
print(f"Squared numbers: {squared}")
"""
    
    print("Testing Python code validation...")
    result = client.validate_code_with_daytona(
        code=python_code,
        language="python",
        skill="Python Programming"
    )
    
    print(f"\nValidation Result:")
    print(f"  Skill: {result['skill']}")
    print(f"  Status: {result['status']}")
    print(f"  Execution Time: {result['execution_time']}s")
    print(f"  Details: {result['details']}")
    if result['output']:
        print(f"  Output: {result['output']}")
    if result['error']:
        print(f"  Error: {result['error']}")