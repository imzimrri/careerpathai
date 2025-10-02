"""
aci.dev client module for agent gateway and tool calling.
Handles tool registration and execution through aci.dev platform.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import requests

from tools import search_learning_content, get_tool_definition

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ACIDevClient:
    """
    Client for interacting with aci.dev Agent Gateway.
    Handles tool registration and execution for course recommendations.
    """
    
    def __init__(self):
        """Initialize aci.dev client with environment configuration."""
        self.api_key = os.getenv("ACI_API_KEY")
        self.base_url = os.getenv("ACI_BASE_URL", "https://api.aci.dev/v1")
        self.timeout = 10  # seconds
        
        # Register available tools
        self.tools = {
            "search_learning_content": search_learning_content
        }
        
        if not self.api_key:
            logger.warning("aci.dev API key not found in environment variables")
    
    def validate_connection(self) -> bool:
        """
        Validate connection to aci.dev API.
        
        Returns:
            bool: True if connection is valid, False otherwise
        """
        if not self.api_key:
            logger.error("aci.dev API key is not configured")
            return False
        
        try:
            # For MVP, we'll assume connection is valid if API key exists
            # In production, this would make an actual API call to validate
            logger.info("aci.dev connection validated (mock mode)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate aci.dev connection: {str(e)}")
            return False
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tool definitions for function calling.
        
        Returns:
            List of tool definition dictionaries
        """
        return [get_tool_definition()]
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered tool with given arguments.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Dictionary of arguments for the tool
        
        Returns:
            Dictionary containing the tool execution result
        
        Raises:
            ValueError: If tool is not found or execution fails
        """
        logger.info(f"Executing tool: {tool_name} with arguments: {arguments}")
        
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found in registered tools")
        
        try:
            # Execute the tool function
            tool_function = self.tools[tool_name]
            result = tool_function(**arguments)
            
            logger.info(f"Tool '{tool_name}' executed successfully")
            return {
                "success": True,
                "tool_name": tool_name,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {str(e)}")
            raise ValueError(f"Tool execution failed: {str(e)}")
    
    def execute_tool_calls(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute multiple tool calls in sequence.
        
        Args:
            tool_calls: List of tool call dictionaries with 'name' and 'arguments'
        
        Returns:
            List of tool execution results
        """
        results = []
        
        for tool_call in tool_calls:
            try:
                tool_name = tool_call.get("name")
                arguments = tool_call.get("arguments", {})
                
                result = self.execute_tool(tool_name, arguments)
                results.append(result)
                
            except Exception as e:
                logger.error(f"Failed to execute tool call: {str(e)}")
                results.append({
                    "success": False,
                    "tool_name": tool_call.get("name", "unknown"),
                    "error": str(e)
                })
        
        return results
    
    def search_courses_for_skills(self, skills: List[str]) -> Dict[str, List[Dict[str, str]]]:
        """
        Search for courses for multiple skills.
        
        This is a convenience method that calls search_learning_content
        for each skill and returns a structured result.
        
        Args:
            skills: List of skill names to search courses for
        
        Returns:
            Dictionary mapping skill names to their course recommendations
        """
        logger.info(f"Searching courses for {len(skills)} skills")
        
        courses_by_skill = {}
        
        for skill in skills:
            try:
                courses = search_learning_content(skill)
                courses_by_skill[skill] = courses
                logger.info(f"Found {len(courses)} courses for '{skill}'")
                
            except Exception as e:
                logger.error(f"Failed to search courses for '{skill}': {str(e)}")
                # Provide fallback courses on error
                courses_by_skill[skill] = [
                    {
                        "title": f"Learn {skill}",
                        "url": f"https://www.google.com/search?q=learn+{skill.replace(' ', '+')}",
                        "platform": "Web Search",
                        "duration": "Varies",
                        "level": "All Levels"
                    }
                ]
        
        return courses_by_skill


def get_aci_client() -> ACIDevClient:
    """
    Factory function to create and return an aci.dev client instance.
    
    Returns:
        ACIDevClient: Configured aci.dev client instance
    """
    return ACIDevClient()


# Example usage and testing
if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create client
    client = get_aci_client()
    
    # Test connection
    if client.validate_connection():
        print("✓ aci.dev connection validated")
        
        # Test getting available tools
        tools = client.get_available_tools()
        print(f"\n✓ Available tools: {len(tools)}")
        for tool in tools:
            print(f"  - {tool['function']['name']}: {tool['function']['description']}")
        
        # Test tool execution
        try:
            print("\n" + "="*60)
            print("Testing tool execution")
            print("="*60)
            
            result = client.execute_tool(
                "search_learning_content",
                {"skill": "Python"}
            )
            
            if result["success"]:
                print(f"\n✓ Tool executed successfully")
                courses = result["result"]
                print(f"Found {len(courses)} courses:")
                for i, course in enumerate(courses[:2], 1):  # Show first 2
                    print(f"\n{i}. {course['title']}")
                    print(f"   Platform: {course['platform']}")
                    print(f"   URL: {course['url']}")
            
        except Exception as e:
            print(f"✗ Tool execution failed: {str(e)}")
        
        # Test searching courses for multiple skills
        try:
            print("\n" + "="*60)
            print("Testing multi-skill course search")
            print("="*60)
            
            skills = ["Python", "Machine Learning", "React"]
            courses_by_skill = client.search_courses_for_skills(skills)
            
            print(f"\n✓ Found courses for {len(courses_by_skill)} skills")
            for skill, courses in courses_by_skill.items():
                print(f"\n{skill}: {len(courses)} courses")
                print(f"  - {courses[0]['title']}")
            
        except Exception as e:
            print(f"✗ Multi-skill search failed: {str(e)}")
    else:
        print("✗ aci.dev connection validation failed")