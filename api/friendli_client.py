"""
FriendliAI client module for LLM-based skill gap analysis.
Implements career transition analysis using FriendliAI's API via HTTP requests.
Supports tool calling for course recommendations via aci.dev.
Includes code snippet generation for educational purposes.
"""

import os
import json
import logging
import re
from typing import List, Dict, Optional, Any, Tuple
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Security validation constants
PROHIBITED_PATTERNS = [
    r'os\.system',
    r'subprocess\.',
    r'eval\(',
    r'exec\(',
    r'__import__',
    r'open\(',
    r'file\(',
    r'requests\.',
    r'urllib\.',
    r'socket\.',
    r'pickle\.',
]

PROHIBITED_IMPORTS = [
    'os', 'sys', 'subprocess', 'socket',
    'pickle', 'shelve', 'marshal',
    'requests', 'urllib', 'http',
]

# Safe fallback code examples
SAFE_FALLBACKS = {
    "python": """# Simple Python example
numbers = [1, 2, 3, 4, 5]
squared = [n**2 for n in numbers]
print(f"Squared numbers: {squared}")
""",
    "javascript": """// Simple JavaScript example
const numbers = [1, 2, 3, 4, 5];
const squared = numbers.map(n => n ** 2);
console.log('Squared numbers:', squared);
""",
    "java": """// Simple Java example
public class Example {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5};
        System.out.println("Sum: " + sum(numbers));
    }
    static int sum(int[] arr) {
        int total = 0;
        for (int n : arr) total += n;
        return total;
    }
}
""",
    "sql": """-- Simple SQL example
SELECT name, COUNT(*) as total
FROM users
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY total DESC;
"""
}

# Skill-to-language mapping
SKILL_LANGUAGE_MAP = {
    # Python skills
    "machine learning": "python",
    "data science": "python",
    "tensorflow": "python",
    "pytorch": "python",
    "pandas": "python",
    "numpy": "python",
    "django": "python",
    "flask": "python",
    "python": "python",
    "scikit-learn": "python",
    "keras": "python",
    
    # JavaScript skills
    "react": "javascript",
    "vue": "javascript",
    "angular": "javascript",
    "node.js": "javascript",
    "nodejs": "javascript",
    "express": "javascript",
    "next.js": "javascript",
    "nextjs": "javascript",
    "javascript": "javascript",
    "typescript": "javascript",
    
    # Java skills
    "java": "java",
    "spring boot": "java",
    "spring": "java",
    "android": "java",
    
    # SQL skills
    "sql": "sql",
    "database": "sql",
    "postgresql": "sql",
    "mysql": "sql",
    "mongodb": "sql",
    
    # Go skills
    "go": "go",
    "golang": "go",
    "microservices": "go",
}


class FriendliAIClient:
    """
    Client for interacting with FriendliAI API.
    Handles authentication, prompt engineering, and skill gap analysis.
    """
    
    def __init__(self):
        """Initialize FriendliAI client with environment configuration."""
        self.api_key = os.getenv("FRIENDLI_TOKEN")
        self.model = os.getenv("FRIENDLI_MODEL", "meta-llama-3.1-8b-instruct")
        base_url = os.getenv("FRIENDLI_BASE_URL", "https://api.friendli.ai/serverless/v1")
        self.base_url = f"{base_url}/chat/completions"
        self.timeout = 30  # seconds
        
        if not self.api_key:
            logger.warning("FriendliAI token not found in environment variables")
    
    def validate_connection(self) -> bool:
        """
        Validate connection to FriendliAI API.
        
        Returns:
            bool: True if connection is valid, False otherwise
        """
        if not self.api_key:
            logger.error("FriendliAI token is not configured")
            return False
        
        try:
            # Test with a minimal request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            test_payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": "Hello"}
                ],
                "max_tokens": 10
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=test_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Successfully validated FriendliAI connection")
                return True
            else:
                logger.error(f"FriendliAI validation failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to validate FriendliAI connection: {str(e)}")
            return False
    
    def _build_prompt(
        self, 
        current_role: str, 
        target_role: str, 
        knowledge_docs: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        Build the prompt messages for FriendliAI.
        
        Args:
            current_role: User's current job title
            target_role: User's desired job title
            knowledge_docs: Retrieved documents from Weaviate
        
        Returns:
            List of message dictionaries for the API
        """
        # Format knowledge documents
        knowledge_text = ""
        if knowledge_docs:
            knowledge_text = "\n\n".join([
                f"**{doc.get('title', 'Unknown')}** ({doc.get('category', 'General')})\n{doc.get('description', '')}"
                for doc in knowledge_docs
            ])
        else:
            knowledge_text = "No specific knowledge documents available."
        
        # System message
        system_message = {
            "role": "system",
            "content": "You are a career advisor AI helping developers transition between roles. Your task is to analyze career transitions and identify the most important skills needed."
        }
        
        # User message with structured prompt
        user_message = {
            "role": "user",
            "content": f"""Current Role: {current_role}
Target Role: {target_role}

Based on the following knowledge about the target role:

{knowledge_text}

Identify the top 3 most important skills this person needs to learn to successfully transition from their current role to the target role.

Return your response as a JSON array of exactly 3 skill names. Format:
["Skill 1", "Skill 2", "Skill 3"]

Only return the JSON array, nothing else."""
        }
        
        return [system_message, user_message]
    
    def _parse_skills_response(self, response_text: str) -> List[str]:
        """
        Parse the LLM response to extract skills.
        
        Args:
            response_text: Raw response text from FriendliAI
        
        Returns:
            List of exactly 3 skill names
        
        Raises:
            ValueError: If response cannot be parsed or doesn't contain 3 skills
        """
        try:
            # Try to find JSON array in the response
            response_text = response_text.strip()
            
            # Handle cases where response might have extra text
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")
            
            json_str = response_text[start_idx:end_idx]
            skills = json.loads(json_str)
            
            # Validate response
            if not isinstance(skills, list):
                raise ValueError("Response is not a list")
            
            if len(skills) != 3:
                logger.warning(f"Expected 3 skills, got {len(skills)}. Adjusting...")
                if len(skills) > 3:
                    skills = skills[:3]
                elif len(skills) < 3:
                    # Pad with generic skills if needed
                    while len(skills) < 3:
                        skills.append(f"Additional Skill {len(skills) + 1}")
            
            # Ensure all skills are strings
            skills = [str(skill).strip() for skill in skills]
            
            logger.info(f"Successfully parsed {len(skills)} skills from response")
            return skills
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from response: {str(e)}")
            raise ValueError(f"Invalid JSON in response: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing skills response: {str(e)}")
            raise ValueError(f"Failed to parse skills: {str(e)}")
    
    def analyze_skill_gap(
        self,
        current_role: str,
        target_role: str,
        knowledge_docs: List[Dict[str, str]]
    ) -> List[str]:
        """
        Analyze skill gap between current and target roles using FriendliAI.
        
        Args:
            current_role: User's current job title
            target_role: User's desired job title
            knowledge_docs: Retrieved documents from Weaviate with fields:
                - title: Job role or skill title
                - description: Detailed description
                - category: Category classification
        
        Returns:
            List of exactly 3 skill names as strings
        
        Raises:
            Exception: If API call fails or response is invalid
        """
        if not self.api_key:
            raise Exception("FriendliAI token is not configured")
        
        try:
            # Build the prompt
            messages = self._build_prompt(current_role, target_role, knowledge_docs)
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            logger.info(f"Sending skill gap analysis request to FriendliAI")
            logger.debug(f"Model: {self.model}, Current: {current_role}, Target: {target_role}")
            
            # Make API request
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            # Handle response
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract content from response
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    content = response_data["choices"][0]["message"]["content"]
                    logger.info("Successfully received response from FriendliAI")
                    
                    # Parse and return skills
                    skills = self._parse_skills_response(content)
                    return skills
                else:
                    raise Exception("Invalid response format from FriendliAI")
            
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API key")
            
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded: Too many requests")
            
            elif response.status_code == 408 or response.status_code == 504:
                raise Exception("Request timeout: FriendliAI API is not responding")
            
            else:
                error_msg = f"FriendliAI API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg += f" - {error_data['error']}"
                except:
                    error_msg += f" - {response.text}"
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            logger.error("Request to FriendliAI timed out")
            raise Exception("Request timeout: FriendliAI API is not responding")
        
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to FriendliAI API")
            raise Exception("Connection error: Unable to reach FriendliAI API")
        
        except Exception as e:
            logger.error(f"Error in skill gap analysis: {str(e)}")
            raise


    def analyze_with_tools(
        self,
        current_role: str,
        target_role: str,
        knowledge_docs: List[Dict[str, str]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze skill gap and use tools to get course recommendations.
        
        This method enables function calling where the LLM can decide to call
        registered tools (like search_learning_content) to enhance its response.
        
        Args:
            current_role: User's current job title
            target_role: User's desired job title
            knowledge_docs: Retrieved documents from Weaviate
            tools: List of tool definitions for function calling
        
        Returns:
            Dictionary containing:
                - skills: List of 3 skill names
                - tool_calls: List of tool calls made by the LLM (if any)
        
        Raises:
            Exception: If API call fails or response is invalid
        """
        if not self.api_key:
            raise Exception("FriendliAI token is not configured")
        
        try:
            # Build the prompt
            messages = self._build_prompt(current_role, target_role, knowledge_docs)
            
            # Prepare API request with tools
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000,
                "tools": tools,
                "tool_choice": "auto"  # Let the model decide when to use tools
            }
            
            logger.info(f"Sending tool-enabled request to FriendliAI")
            logger.debug(f"Model: {self.model}, Tools: {len(tools)}")
            
            # Make API request
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            # Handle response
            if response.status_code == 200:
                response_data = response.json()
                
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    choice = response_data["choices"][0]
                    message = choice["message"]
                    
                    # Check if the model made tool calls
                    if "tool_calls" in message and message["tool_calls"]:
                        logger.info(f"LLM made {len(message['tool_calls'])} tool calls")
                        return {
                            "has_tool_calls": True,
                            "tool_calls": message["tool_calls"],
                            "content": message.get("content", "")
                        }
                    else:
                        # No tool calls, parse skills from content
                        content = message.get("content", "")
                        logger.info("No tool calls made, parsing skills from content")
                        skills = self._parse_skills_response(content)
                        return {
                            "has_tool_calls": False,
                            "skills": skills,
                            "content": content
                        }
                else:
                    raise Exception("Invalid response format from FriendliAI")
            
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API key")
            
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded: Too many requests")
            
            elif response.status_code == 408 or response.status_code == 504:
                raise Exception("Request timeout: FriendliAI API is not responding")
            
            else:
                error_msg = f"FriendliAI API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg += f" - {error_data['error']}"
                except:
                    error_msg += f" - {response.text}"
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            logger.error("Request to FriendliAI timed out")
            raise Exception("Request timeout: FriendliAI API is not responding")
        
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to FriendliAI API")

    def _detect_language(self, skill: str) -> str:
        """
        Detect the appropriate programming language for a given skill.
        
        Args:
            skill: The skill name
        
        Returns:
            Language identifier (e.g., "python", "javascript")
        """
        skill_lower = skill.lower().strip()
        
        # Check direct mapping
        if skill_lower in SKILL_LANGUAGE_MAP:
            return SKILL_LANGUAGE_MAP[skill_lower]
        
        # Check if skill contains any mapped keywords
        for keyword, language in SKILL_LANGUAGE_MAP.items():
            if keyword in skill_lower:
                return language
        
        # Default to Python
        logger.info(f"No language mapping found for '{skill}', defaulting to Python")
        return "python"
    
    def _validate_code_safety(self, code: str) -> Tuple[bool, str]:
        """
        Validate that generated code doesn't contain dangerous patterns.
        
        Args:
            code: The code to validate
        
        Returns:
            Tuple of (is_safe, reason)
        """
        # Check for prohibited patterns
        for pattern in PROHIBITED_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                logger.warning(f"Code contains prohibited pattern: {pattern}")
                return False, f"Contains prohibited pattern: {pattern}"
        
        # Check for prohibited imports
        import_lines = [line.strip() for line in code.split('\n') if 'import' in line.lower()]
        for line in import_lines:
            for prohibited in PROHIBITED_IMPORTS:
                if prohibited in line:
                    logger.warning(f"Code contains prohibited import: {prohibited}")
                    return False, f"Contains prohibited import: {prohibited}"
        
        return True, "Code passed safety validation"
    
    def _build_code_generation_prompt(self, skill: str, language: str) -> List[Dict[str, str]]:
        """
        Build the prompt for code generation.
        
        Args:
            skill: The skill to generate code for
            language: The programming language to use
        
        Returns:
            List of message dictionaries for the API
        """
        system_message = {
            "role": "system",
            "content": "You are an expert programming instructor. Generate clean, educational code examples that demonstrate core concepts. Always include explanatory comments."
        }
        
        user_message = {
            "role": "user",
            "content": f"""Generate a short, functional code snippet (5-10 lines) demonstrating the skill: {skill}.

Requirements:
- Use {language} programming language
- Include 2-3 explanatory comments
- Make it a complete, runnable example
- Keep it simple and educational
- Focus on the core concept of {skill}
- Do NOT use file operations, network calls, or system commands

Return only the code snippet with comments, no additional explanation."""
        }
        
        return [system_message, user_message]
    
    def generate_code_snippet(self, skill: str) -> Dict[str, str]:
        """
        Generate a code snippet demonstrating a specific skill.
        
        Args:
            skill: The skill to generate code for
        
        Returns:
            Dictionary containing:
                - code: The generated code snippet
                - language: Programming language used
                - description: Brief description of what the code does
        
        Raises:
            Exception: If code generation fails
        """
        if not self.api_key:
            logger.warning("FriendliAI token not configured, using fallback code")
            language = self._detect_language(skill)
            return {
                "code": SAFE_FALLBACKS.get(language, SAFE_FALLBACKS["python"]),
                "language": language,
                "description": f"Simple {language} example demonstrating basic concepts"
            }
        
        try:
            # Detect appropriate language
            language = self._detect_language(skill)
            logger.info(f"Generating {language} code for skill: {skill}")
            
            # Build prompt
            messages = self._build_code_generation_prompt(skill, language)
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 300
            }
            
            # Make API request
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=10  # Shorter timeout for code generation
            )
            
            # Handle response
            if response.status_code == 200:
                response_data = response.json()
                
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    generated_code = response_data["choices"][0]["message"]["content"].strip()
                    
                    # Clean up code (remove markdown code blocks if present)
                    if "```" in generated_code:
                        # Extract code from markdown code blocks
                        code_match = re.search(r'```(?:\w+)?\n(.*?)\n```', generated_code, re.DOTALL)
                        if code_match:
                            generated_code = code_match.group(1).strip()
                    
                    # Validate code safety
                    is_safe, reason = self._validate_code_safety(generated_code)
                    
                    if not is_safe:
                        logger.warning(f"Generated code failed safety check: {reason}")
                        logger.warning("Using safe fallback code")
                        generated_code = SAFE_FALLBACKS.get(language, SAFE_FALLBACKS["python"])
                        description = f"Safe {language} example (original code failed validation)"
                    else:
                        # Extract description from comments or generate one
                        description = f"Practical {language} example demonstrating {skill}"
                    
                    logger.info(f"Successfully generated code snippet for {skill}")
                    
                    return {
                        "code": generated_code,
                        "language": language,
                        "description": description
                    }
                else:
                    raise Exception("Invalid response format from FriendliAI")
            
            else:
                logger.error(f"FriendliAI API error: {response.status_code}")
                raise Exception(f"API error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            logger.error("Code generation request timed out")
            # Use fallback
            language = self._detect_language(skill)
            return {
                "code": SAFE_FALLBACKS.get(language, SAFE_FALLBACKS["python"]),
                "language": language,
                "description": f"Safe {language} example (timeout fallback)"
            }
        
        except Exception as e:
            logger.error(f"Error generating code snippet: {str(e)}")
            # Use fallback
            language = self._detect_language(skill)
            return {
                "code": SAFE_FALLBACKS.get(language, SAFE_FALLBACKS["python"]),
                "language": language,
                "description": f"Safe {language} example (error fallback)"
            }

            raise Exception("Connection error: Unable to reach FriendliAI API")
        
        except Exception as e:
            logger.error(f"Error in tool-enabled analysis: {str(e)}")
            raise


def get_friendli_client() -> FriendliAIClient:
    """
    Factory function to create and return a FriendliAI client instance.
    
    Returns:
        FriendliAIClient: Configured FriendliAI client instance
    """
    return FriendliAIClient()


# Example usage and testing
if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create client
    client = get_friendli_client()
    
    # Test connection
    if client.validate_connection():
        print("✓ FriendliAI connection validated")
        
        # Test skill gap analysis
        try:
            mock_docs = [
                {
                    "title": "Machine Learning Engineer",
                    "description": "Requires strong Python skills, understanding of ML algorithms, and experience with frameworks like TensorFlow or PyTorch.",
                    "category": "Technical Skills"
                },
                {
                    "title": "Data Science Fundamentals",
                    "description": "Statistical analysis, data visualization, and predictive modeling are essential.",
                    "category": "Core Competencies"
                }
            ]
            
            skills = client.analyze_skill_gap(
                current_role="Frontend Developer",
                target_role="Machine Learning Engineer",
                knowledge_docs=mock_docs
            )
            
            print(f"\n✓ Skill gap analysis completed")
            print(f"Top 3 skills to learn:")
            for i, skill in enumerate(skills, 1):
                print(f"  {i}. {skill}")
                
        except Exception as e:
            print(f"✗ Skill gap analysis failed: {str(e)}")
    else:
        print("✗ FriendliAI connection validation failed")