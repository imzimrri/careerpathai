"""
Comet (Opik) client module for observability and tracing.
Implements end-to-end logging of the career path generation workflow.
"""

import os
import time
import logging
from typing import Dict, Any, Optional, List
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Opik SDK
try:
    from opik import Opik, opik_context
    from opik.decorator import track
    OPIK_SDK_AVAILABLE = True
except ImportError:
    logger.warning("Opik SDK not installed. Install with: pip install opik")
    OPIK_SDK_AVAILABLE = False

# Configuration
COMET_API_KEY = os.getenv("COMET_API_KEY")
COMET_PROJECT_NAME = os.getenv("COMET_PROJECT_NAME", "careerpathai")
COMET_WORKSPACE = os.getenv("COMET_WORKSPACE")


class CometClient:
    """
    Client for Comet (Opik) observability.
    Handles tracing and logging of the complete workflow.
    """
    
    def __init__(self):
        """Initialize Comet client with environment configuration."""
        self.api_key = COMET_API_KEY
        self.project_name = COMET_PROJECT_NAME
        self.workspace = COMET_WORKSPACE
        self.client = None
        self.current_trace = None
        
        if not self.api_key:
            logger.warning("Comet API key not found in environment variables")
        elif not OPIK_SDK_AVAILABLE:
            logger.warning("Opik SDK not available")
        else:
            try:
                # Initialize Opik client
                config_params = {
                    "api_key": self.api_key,
                    "project_name": self.project_name
                }
                
                if self.workspace:
                    config_params["workspace"] = self.workspace
                
                self.client = Opik(**config_params)
                logger.info(f"Opik client initialized for project: {self.project_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Opik client: {str(e)}")
                self.client = None
    
    @contextmanager
    def trace_request(self, name: str, metadata: Dict[str, Any]):
        """
        Context manager for tracing a complete request.
        
        Args:
            name: Name of the trace (e.g., "career_path_generation")
            metadata: Metadata to attach to the trace
        
        Yields:
            The trace object for adding spans
        """
        if not self.client:
            # If Opik not available, just yield None and continue
            logger.debug("Opik client not available, skipping trace")
            yield None
            return
        
        trace = None
        try:
            # Create trace
            trace = self.client.trace(
                name=name,
                input=metadata,
                metadata=metadata
            )
            self.current_trace = trace
            logger.info(f"Started trace: {name}")
            
            yield trace
            
        except Exception as e:
            logger.warning(f"Error in trace context: {str(e)}")
            yield None
        
        finally:
            # Finalize trace
            if trace:
                try:
                    trace.end()
                    logger.info(f"Finalized trace: {name}")
                except Exception as e:
                    logger.warning(f"Error finalizing trace: {str(e)}")
            
            self.current_trace = None
    
    def log_span(
        self,
        name: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log a span within the current trace.
        
        Args:
            name: Name of the span (e.g., "weaviate_query")
            input_data: Input data for the span
            output_data: Output data from the span
            metadata: Optional metadata (e.g., latency, token count)
        """
        if not self.client or not self.current_trace:
            logger.debug(f"Skipping span log: {name}")
            return
        
        try:
            span = self.current_trace.span(
                name=name,
                input=input_data,
                output=output_data,
                metadata=metadata or {}
            )
            span.end()
            logger.debug(f"Logged span: {name}")
        
        except Exception as e:
            logger.warning(f"Failed to log span '{name}': {str(e)}")
    
    def log_weaviate_query(
        self,
        target_role: str,
        limit: int,
        certainty: float,
        documents: List[Dict[str, str]],
        latency: float
    ):
        """
        Log Weaviate RAG retrieval.
        
        Args:
            target_role: The target role queried
            limit: Number of documents requested
            certainty: Certainty threshold
            documents: Retrieved documents
            latency: Query latency in seconds
        """
        input_data = {
            "target_role": target_role,
            "limit": limit,
            "certainty": certainty
        }
        
        output_data = {
            "document_count": len(documents),
            "titles": [doc.get("title", "Unknown") for doc in documents[:3]],  # First 3 titles
            "categories": list(set(doc.get("category", "General") for doc in documents))
        }
        
        metadata = {
            "latency_seconds": latency,
            "component": "weaviate"
        }
        
        self.log_span("weaviate_query", input_data, output_data, metadata)
    
    def log_friendli_analysis(
        self,
        current_role: str,
        target_role: str,
        skills: List[str],
        latency: float,
        token_usage: Optional[Dict[str, int]] = None
    ):
        """
        Log FriendliAI skill gap analysis.
        
        Args:
            current_role: User's current role
            target_role: User's target role
            skills: Identified skills
            latency: Analysis latency in seconds
            token_usage: Optional token usage stats
        """
        input_data = {
            "current_role": current_role,
            "target_role": target_role
        }
        
        output_data = {
            "skills": skills,
            "skill_count": len(skills)
        }
        
        metadata = {
            "latency_seconds": latency,
            "component": "friendli_ai"
        }
        
        if token_usage:
            metadata["token_usage"] = token_usage
        
        self.log_span("friendli_skill_analysis", input_data, output_data, metadata)
    
    def log_aci_course_search(
        self,
        skills: List[str],
        courses_by_skill: Dict[str, List[Dict[str, str]]],
        latency: float
    ):
        """
        Log aci.dev course search.
        
        Args:
            skills: Skills searched for
            courses_by_skill: Courses found for each skill
            latency: Search latency in seconds
        """
        input_data = {
            "skills": skills,
            "skill_count": len(skills)
        }
        
        total_courses = sum(len(courses) for courses in courses_by_skill.values())
        output_data = {
            "total_courses": total_courses,
            "courses_per_skill": {skill: len(courses) for skill, courses in courses_by_skill.items()}
        }
        
        metadata = {
            "latency_seconds": latency,
            "component": "aci_dev"
        }
        
        self.log_span("aci_course_search", input_data, output_data, metadata)
    
    def log_code_generation(
        self,
        skill: str,
        code: str,
        language: str,
        description: str,
        latency: float
    ):
        """
        Log code snippet generation.
        
        Args:
            skill: Skill for which code was generated
            code: Generated code snippet
            language: Programming language
            description: Code description
            latency: Generation latency in seconds
        """
        input_data = {
            "skill": skill,
            "language": language
        }
        
        output_data = {
            "code_length": len(code),
            "language": language,
            "description": description,
            "code_preview": code[:100] + "..." if len(code) > 100 else code
        }
        
        metadata = {
            "latency_seconds": latency,
            "component": "code_generation"
        }
        
        self.log_span("code_generation", input_data, output_data, metadata)
    
    def log_daytona_validation(
        self,
        code: str,
        language: str,
        skill: str,
        validation_result: Dict[str, Any],
        latency: float
    ):
        """
        Log Daytona code validation.
        
        Args:
            code: Code that was validated
            language: Programming language
            skill: Skill being validated
            validation_result: Validation result from Daytona
            latency: Validation latency in seconds
        """
        input_data = {
            "skill": skill,
            "language": language,
            "code_length": len(code)
        }
        
        output_data = {
            "status": validation_result.get("status"),
            "execution_time": validation_result.get("execution_time"),
            "has_output": bool(validation_result.get("output")),
            "has_error": bool(validation_result.get("error"))
        }
        
        metadata = {
            "latency_seconds": latency,
            "component": "daytona",
            "validation_details": validation_result.get("details")
        }
        
        self.log_span("daytona_validation", input_data, output_data, metadata)
    
    def log_error(
        self,
        component: str,
        error_message: str,
        error_type: str
    ):
        """
        Log an error that occurred during the workflow.
        
        Args:
            component: Component where error occurred
            error_message: Error message
            error_type: Type of error
        """
        if not self.client or not self.current_trace:
            logger.debug(f"Skipping error log for {component}")
            return
        
        try:
            self.current_trace.log_error(
                component=component,
                error_message=error_message,
                error_type=error_type
            )
            logger.debug(f"Logged error for {component}")
        
        except Exception as e:
            logger.warning(f"Failed to log error: {str(e)}")


def get_comet_client() -> CometClient:
    """
    Factory function to create and return a Comet client instance.
    
    Returns:
        CometClient: Configured Comet client instance
    """
    return CometClient()


# Example usage and testing
if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create client
    client = get_comet_client()
    
    # Test trace creation
    print("Testing Comet trace creation...")
    
    with client.trace_request("test_career_path", {
        "current_role": "Frontend Developer",
        "target_role": "ML Engineer"
    }) as trace:
        # Simulate workflow steps
        
        # Step 1: Weaviate query
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
        
        # Step 2: FriendliAI analysis
        client.log_friendli_analysis(
            current_role="Frontend Developer",
            target_role="ML Engineer",
            skills=["Machine Learning", "Python", "TensorFlow"],
            latency=2.3,
            token_usage={"prompt": 450, "completion": 120}
        )
        
        # Step 3: aci.dev course search
        client.log_aci_course_search(
            skills=["Machine Learning", "Python", "TensorFlow"],
            courses_by_skill={
                "Machine Learning": [{"title": "ML Course 1"}, {"title": "ML Course 2"}],
                "Python": [{"title": "Python Course 1"}],
                "TensorFlow": [{"title": "TF Course 1"}]
            },
            latency=1.2
        )
        
        # Step 4: Code generation
        client.log_code_generation(
            skill="Machine Learning",
            code="import numpy as np\nprint('Hello ML')",
            language="python",
            description="Simple ML example",
            latency=1.5
        )
        
        # Step 5: Daytona validation
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
    
    print("✓ Trace creation test completed")
    print("Check Comet dashboard for trace details")