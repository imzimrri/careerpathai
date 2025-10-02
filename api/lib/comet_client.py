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
    from opik import Opik
    from opik.decorator import tracker
    OPIK_SDK_AVAILABLE = True
    logger.info("✓ Opik SDK imported successfully")
except ImportError as e:
    logger.warning(f"Opik SDK not installed or import failed: {str(e)}")
    logger.warning("Install with: pip install opik")
    OPIK_SDK_AVAILABLE = False

class CometClient:
    """
    Client for Comet (Opik) observability.
    Handles tracing and logging of the complete workflow.
    """
    
    def __init__(self):
        """Initialize Comet client with environment configuration."""
        # Read environment variables at initialization time (after load_dotenv())
        comet_api_key = os.getenv("COMET_API_KEY")
        comet_project_name = os.getenv("COMET_PROJECT_NAME", "careerpathai")
        comet_workspace = os.getenv("COMET_WORKSPACE")
        
        # Opik-specific configuration (preferred)
        self.api_key = os.getenv("OPIK_API_KEY", comet_api_key)
        self.project_name = os.getenv("OPIK_PROJECT_NAME", comet_project_name)
        self.workspace = os.getenv("OPIK_WORKSPACE", comet_workspace)
        
        # Debug logging
        logger.info(f"Opik Configuration Check:")
        logger.info(f"  API Key present: {bool(self.api_key)}")
        logger.info(f"  Project Name: {self.project_name}")
        logger.info(f"  Workspace: {self.workspace or 'Not set'}")
        self.client = None
        self.current_trace = None
        
        if not self.api_key:
            logger.warning("Opik API key not found in environment variables")
            logger.warning("Please set OPIK_API_KEY or COMET_API_KEY in your .env file")
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
                
                logger.info(f"Initializing Opik client with project: {self.project_name}")
                self.client = Opik(**config_params)
                logger.info(f"✓ Opik client initialized successfully for project: {self.project_name}")
            except Exception as e:
                logger.error(f"✗ Failed to initialize Opik client: {str(e)}")
                logger.error(f"   Check your API key and project name in .env file")
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
            logger.warning("⚠️  Opik client not available, skipping trace")
            logger.warning(f"   API Key present: {bool(self.api_key)}")
            logger.warning(f"   Project: {self.project_name}")
            yield None
            return
        
        trace = None
        try:
            # Create trace
            logger.info(f"🔵 Creating Opik trace: {name}")
            trace = self.client.trace(
                name=name,
                input=metadata,
                metadata=metadata
            )
            self.current_trace = trace
            logger.info(f"✅ Started trace: {name} (ID: {trace.id if hasattr(trace, 'id') else 'unknown'})")
            
            yield trace
            
        except Exception as e:
            logger.error(f"❌ Error in trace context: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            yield None
        
        finally:
            # Finalize trace
            if trace:
                try:
                    logger.info(f"🔵 Finalizing trace: {name}")
                    trace.end()
                    logger.info(f"✅ Finalized trace: {name}")
                except Exception as e:
                    logger.error(f"❌ Error finalizing trace: {str(e)}")
                    import traceback
                    logger.error(traceback.format_exc())
            
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
            # Log error as a span with error metadata
            error_span = self.current_trace.span(
                name=f"error_{component}",
                input={"component": component, "error_type": error_type},
                output={"error_message": error_message},
                metadata={
                    "error": True,
                    "error_type": error_type,
                    "component": component
                }
            )
            error_span.end()
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