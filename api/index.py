"""
FastAPI backend orchestrator for CareerPath AI.
Main entry point for Vercel serverless function deployment.
"""

import os
import time
import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from api.weaviate_client import get_weaviate_client
from api.friendli_client import get_friendli_client
from api.aci_client import get_aci_client
from api.daytona_client import get_daytona_client
from api.comet_client import get_comet_client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CareerPath AI API",
    version="1.0.0",
    description="API for generating personalized career learning paths"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class UserInput(BaseModel):
    """User input model for career path generation."""
    currentRole: str = Field(..., description="User's current job title")
    targetRole: str = Field(..., description="User's desired job title")


class Course(BaseModel):
    """Course recommendation model."""
    title: str = Field(..., description="Course title")
    url: str = Field(..., description="URL to learning resource")
    platform: str = Field(..., description="Platform name (e.g., YouTube, Udemy)")
    duration: Optional[str] = Field(None, description="Estimated duration")
    level: Optional[str] = Field(None, description="Difficulty level")


class CodeValidationResult(BaseModel):
    """Code validation result from Daytona."""
    skill: str = Field(..., description="Skill being validated")
    status: str = Field(..., description="Success or Failure")
    output: str = Field(..., description="stdout from execution")
    error: Optional[str] = Field(None, description="stderr if any")
    execution_time: float = Field(..., description="Time in seconds")
    details: str = Field(..., description="Human-readable summary")


class CodeSnippet(BaseModel):
    """Code snippet model with metadata."""
    code: str = Field(..., description="The actual code snippet")
    language: str = Field(..., description="Programming language (e.g., python, javascript)")
    description: str = Field(..., description="Brief description of what the code does")
    validation: Optional[CodeValidationResult] = Field(None, description="Validation result from Daytona")


class SkillWithCourses(BaseModel):
    """Skill with associated course recommendations and optional code snippet."""
    skill: str = Field(..., description="Skill name")
    courses: List[Course] = Field(..., description="List of recommended courses")
    code_snippet: Optional[CodeSnippet] = Field(None, description="Code example (only for first skill)")


class CodeValidation(BaseModel):
    """Code validation result model."""
    skill: str = Field(..., description="Skill being validated")
    status: str = Field(..., description="Success or Failure")
    details: str = Field(..., description="Validation details")


class CareerPath(BaseModel):
    """Career path response model."""
    title: str = Field(..., description="Summary title for the career path")
    skillsToLearn: List[str] = Field(..., description="Top 3 recommended skills")
    skillsWithCourses: List[SkillWithCourses] = Field(..., description="Skills with course recommendations")
    codeValidationResult: CodeValidation = Field(..., description="Code validation result")


# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "CareerPath AI API",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check including Weaviate connection."""
    health_status = {
        "api": "healthy",
        "weaviate": "unknown"
    }
    
    try:
        client = get_weaviate_client()
        if client.connect():
            health_status["weaviate"] = "connected"
            client.disconnect()
        else:
            health_status["weaviate"] = "disconnected"
    except Exception as e:
        health_status["weaviate"] = f"error: {str(e)}"
    
    return health_status


@app.post("/api/generate-career-path", response_model=CareerPath)
async def generate_career_path(user_input: UserInput):
    """
    Generate a personalized career learning path.
    
    This endpoint orchestrates the full workflow:
    1. Query Weaviate for relevant job knowledge (COMPLETED - Story 1.2)
    2. Analyze with FriendliAI (COMPLETED - Story 1.3)
    3. Call aci.dev for course recommendations (COMPLETED - Story 1.4)
    4. Generate code snippet for first skill (COMPLETED - Story 1.5)
    5. Validate code with Daytona (COMPLETED - Story 1.6)
    6. Log everything with Comet (THIS STORY - Story 1.7)
    
    Args:
        user_input: User's current and target roles
    
    Returns:
        CareerPath: Complete career learning path with recommendations
    
    Raises:
        HTTPException: If any step in the workflow fails
    """
    logger.info(f"Generating career path: {user_input.currentRole} -> {user_input.targetRole}")
    
    # Initialize clients
    weaviate_client = None
    comet_client = get_comet_client()
    
    # Debug: Log Comet client status
    logger.info(f"Comet client initialized: {comet_client.client is not None}")
    logger.info(f"Comet API key present: {bool(comet_client.api_key)}")
    logger.info(f"Comet project: {comet_client.project_name}")
    
    # Start Comet trace for complete workflow
    with comet_client.trace_request("career_path_generation", {
        "current_role": user_input.currentRole,
        "target_role": user_input.targetRole
    }):
        try:
            # Step 1: Query Weaviate for relevant job knowledge
            weaviate_start = time.time()
            weaviate_client = get_weaviate_client()
            
            if not weaviate_client.connect():
                raise HTTPException(
                    status_code=503,
                    detail="Failed to connect to Weaviate knowledge base"
                )
            
            # Perform semantic search based on target role
            job_knowledge = weaviate_client.query_job_knowledge(
                target_role=user_input.targetRole,
                limit=5,
                certainty=0.7
            )
            
            if not job_knowledge:
                logger.warning(f"No job knowledge found for: {user_input.targetRole}")
                job_knowledge = []
            
            weaviate_latency = time.time() - weaviate_start
            logger.info(f"Retrieved {len(job_knowledge)} relevant documents from Weaviate")
            
            # Log Weaviate query to Comet
            comet_client.log_weaviate_query(
                target_role=user_input.targetRole,
                limit=5,
                certainty=0.7,
                documents=job_knowledge,
                latency=weaviate_latency
            )
            
            # Step 2: Analyze with FriendliAI to identify top 3 skills
            friendli_start = time.time()
            friendli_client = get_friendli_client()
            
            try:
                skills_to_learn = friendli_client.analyze_skill_gap(
                    current_role=user_input.currentRole,
                    target_role=user_input.targetRole,
                    knowledge_docs=job_knowledge
                )
                friendli_latency = time.time() - friendli_start
                logger.info(f"FriendliAI identified {len(skills_to_learn)} skills to learn")
                
                # Log FriendliAI analysis to Comet
                comet_client.log_friendli_analysis(
                    current_role=user_input.currentRole,
                    target_role=user_input.targetRole,
                    skills=skills_to_learn,
                    latency=friendli_latency
                )
                
            except Exception as e:
                logger.error(f"FriendliAI analysis failed: {str(e)}")
                skills_to_learn = [
                    "Core Technical Skills",
                    "Domain Knowledge",
                    "Best Practices & Tools"
                ]
                logger.warning("Using fallback skills due to FriendliAI error")
                
                # Log error to Comet
                comet_client.log_error(
                    component="friendli_ai",
                    error_message=str(e),
                    error_type=type(e).__name__
                )
            
            # Step 3: Use aci.dev to get course recommendations for each skill
            aci_start = time.time()
            aci_client = get_aci_client()
            skills_with_courses = []
            
            try:
                # Get course recommendations for all skills
                courses_by_skill = aci_client.search_courses_for_skills(skills_to_learn)
                
                # Format the response
                for skill in skills_to_learn:
                    courses = courses_by_skill.get(skill, [])
                    course_models = [
                        Course(
                            title=course["title"],
                            url=course["url"],
                            platform=course["platform"],
                            duration=course.get("duration"),
                            level=course.get("level")
                        )
                        for course in courses[:3]
                    ]
                    
                    skills_with_courses.append(
                        SkillWithCourses(
                            skill=skill,
                            courses=course_models
                        )
                    )
                
                aci_latency = time.time() - aci_start
                logger.info(f"Successfully retrieved courses for {len(skills_with_courses)} skills")
                
                # Log aci.dev course search to Comet
                comet_client.log_aci_course_search(
                    skills=skills_to_learn,
                    courses_by_skill=courses_by_skill,
                    latency=aci_latency
                )
                
            except Exception as e:
                logger.error(f"aci.dev course search failed: {str(e)}")
                for skill in skills_to_learn:
                    skills_with_courses.append(
                        SkillWithCourses(
                            skill=skill,
                            courses=[
                                Course(
                                    title=f"Learn {skill}",
                                    url=f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}",
                                    platform="YouTube",
                                    duration="Varies",
                                    level="All Levels"
                                )
                            ]
                        )
                    )
                logger.warning("Using fallback courses due to aci.dev error")
                
                # Log error to Comet
                comet_client.log_error(
                    component="aci_dev",
                    error_message=str(e),
                    error_type=type(e).__name__
                )
            
            # Step 4: Generate code snippet for the first skill
            code_gen_start = time.time()
            first_skill_code = None
            if skills_to_learn:
                try:
                    logger.info(f"Generating code snippet for first skill: {skills_to_learn[0]}")
                    code_data = friendli_client.generate_code_snippet(skills_to_learn[0])
                    
                    first_skill_code = CodeSnippet(
                        code=code_data["code"],
                        language=code_data["language"],
                        description=code_data["description"]
                    )
                    
                    code_gen_latency = time.time() - code_gen_start
                    logger.info(f"Successfully generated {code_data['language']} code snippet")
                    
                    # Log code generation to Comet
                    comet_client.log_code_generation(
                        skill=skills_to_learn[0],
                        code=code_data["code"],
                        language=code_data["language"],
                        description=code_data["description"],
                        latency=code_gen_latency
                    )
                    
                except Exception as e:
                    logger.error(f"Code generation failed: {str(e)}")
                    first_skill_code = None
                    
                    # Log error to Comet
                    comet_client.log_error(
                        component="code_generation",
                        error_message=str(e),
                        error_type=type(e).__name__
                    )
            
            # Add code snippet to first skill
            if first_skill_code and skills_with_courses:
                skills_with_courses[0].code_snippet = first_skill_code
            
            # Step 5: Validate code with Daytona
            validation_result = None
            if first_skill_code:
                try:
                    daytona_start = time.time()
                    logger.info(f"Validating code snippet with Daytona")
                    daytona_client = get_daytona_client()
                    
                    validation_result = daytona_client.validate_code_with_daytona(
                        code=first_skill_code.code,
                        language=first_skill_code.language,
                        skill=skills_to_learn[0]
                    )
                    
                    daytona_latency = time.time() - daytona_start
                    
                    # Add validation result to code snippet
                    skills_with_courses[0].code_snippet.validation = CodeValidationResult(**validation_result)
                    
                    logger.info(f"Code validation completed: {validation_result['status']}")
                    
                    # Log Daytona validation to Comet
                    comet_client.log_daytona_validation(
                        code=first_skill_code.code,
                        language=first_skill_code.language,
                        skill=skills_to_learn[0],
                        validation_result=validation_result,
                        latency=daytona_latency
                    )
                    
                except Exception as e:
                    logger.error(f"Code validation failed: {str(e)}")
                    
                    # Log error to Comet
                    comet_client.log_error(
                        component="daytona",
                        error_message=str(e),
                        error_type=type(e).__name__
                    )
            
            # Build final response
            response = CareerPath(
                title=f"Your Path from {user_input.currentRole} to {user_input.targetRole}",
                skillsToLearn=skills_to_learn,
                skillsWithCourses=skills_with_courses,
                codeValidationResult=CodeValidation(
                    skill=skills_to_learn[0] if skills_to_learn else "General Skills",
                    status=validation_result.get("status", "Pending") if validation_result else "Skipped",
                    details=validation_result.get("details", "No code generated") if validation_result else "No code snippet generated"
                )
            )
            
            logger.info("Successfully generated career path")
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error generating career path: {str(e)}")
            
            # Log error to Comet
            try:
                comet_client.log_error(
                    component="orchestrator",
                    error_message=str(e),
                    error_type=type(e).__name__
                )
            except:
                pass
            
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
        finally:
            # Always disconnect from Weaviate
            if weaviate_client:
                weaviate_client.disconnect()


# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)