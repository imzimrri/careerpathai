"""
Tool functions for aci.dev integration.
Provides mock course recommendations for different skills.
"""

import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Mock course database for MVP
MOCK_COURSES = {
    "python": [
        {
            "title": "Python for Everybody - Full Course",
            "url": "https://www.youtube.com/watch?v=8DvywoWv6fI",
            "platform": "YouTube",
            "duration": "14 hours",
            "level": "Beginner"
        },
        {
            "title": "Complete Python Bootcamp",
            "url": "https://www.udemy.com/course/complete-python-bootcamp/",
            "platform": "Udemy",
            "duration": "22 hours",
            "level": "Beginner to Advanced"
        },
        {
            "title": "Python Programming",
            "url": "https://www.coursera.org/specializations/python",
            "platform": "Coursera",
            "duration": "8 months",
            "level": "Beginner"
        }
    ],
    "machine learning": [
        {
            "title": "Machine Learning Crash Course",
            "url": "https://developers.google.com/machine-learning/crash-course",
            "platform": "Google",
            "duration": "15 hours",
            "level": "Beginner"
        },
        {
            "title": "Machine Learning A-Z™: Hands-On Python",
            "url": "https://www.udemy.com/course/machinelearning/",
            "platform": "Udemy",
            "duration": "44 hours",
            "level": "Intermediate"
        },
        {
            "title": "Machine Learning Specialization",
            "url": "https://www.coursera.org/specializations/machine-learning-introduction",
            "platform": "Coursera",
            "duration": "3 months",
            "level": "Beginner"
        }
    ],
    "tensorflow": [
        {
            "title": "TensorFlow 2.0 Complete Course",
            "url": "https://www.youtube.com/watch?v=tPYj3fFJGjk",
            "platform": "YouTube",
            "duration": "7 hours",
            "level": "Beginner"
        },
        {
            "title": "TensorFlow Developer Certificate",
            "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice",
            "platform": "Coursera",
            "duration": "4 months",
            "level": "Intermediate"
        }
    ],
    "pytorch": [
        {
            "title": "PyTorch for Deep Learning",
            "url": "https://www.youtube.com/watch?v=V_xro1bcAuA",
            "platform": "YouTube",
            "duration": "25 hours",
            "level": "Beginner"
        },
        {
            "title": "Deep Learning with PyTorch",
            "url": "https://www.udemy.com/course/pytorch-for-deep-learning-with-python-bootcamp/",
            "platform": "Udemy",
            "duration": "16 hours",
            "level": "Intermediate"
        }
    ],
    "data science": [
        {
            "title": "Data Science Full Course",
            "url": "https://www.youtube.com/watch?v=ua-CiDNNj30",
            "platform": "YouTube",
            "duration": "12 hours",
            "level": "Beginner"
        },
        {
            "title": "IBM Data Science Professional Certificate",
            "url": "https://www.coursera.org/professional-certificates/ibm-data-science",
            "platform": "Coursera",
            "duration": "11 months",
            "level": "Beginner"
        }
    ],
    "react": [
        {
            "title": "React Course - Beginner's Tutorial",
            "url": "https://www.youtube.com/watch?v=bMknfKXIFA8",
            "platform": "YouTube",
            "duration": "12 hours",
            "level": "Beginner"
        },
        {
            "title": "React - The Complete Guide",
            "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
            "platform": "Udemy",
            "duration": "49 hours",
            "level": "All Levels"
        }
    ],
    "vue": [
        {
            "title": "Vue.js Course for Beginners",
            "url": "https://www.youtube.com/watch?v=FXpIoQ_rT_c",
            "platform": "YouTube",
            "duration": "3 hours",
            "level": "Beginner"
        },
        {
            "title": "Vue - The Complete Guide",
            "url": "https://www.udemy.com/course/vuejs-2-the-complete-guide/",
            "platform": "Udemy",
            "duration": "32 hours",
            "level": "All Levels"
        }
    ],
    "angular": [
        {
            "title": "Angular Tutorial for Beginners",
            "url": "https://www.youtube.com/watch?v=3qBXWUpoPHo",
            "platform": "YouTube",
            "duration": "3 hours",
            "level": "Beginner"
        },
        {
            "title": "Angular - The Complete Guide",
            "url": "https://www.udemy.com/course/the-complete-guide-to-angular-2/",
            "platform": "Udemy",
            "duration": "36 hours",
            "level": "All Levels"
        }
    ],
    "node.js": [
        {
            "title": "Node.js Tutorial for Beginners",
            "url": "https://www.youtube.com/watch?v=TlB_eWDSMt4",
            "platform": "YouTube",
            "duration": "3 hours",
            "level": "Beginner"
        },
        {
            "title": "Node.js, Express, MongoDB & More",
            "url": "https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/",
            "platform": "Udemy",
            "duration": "42 hours",
            "level": "Intermediate"
        }
    ],
    "docker": [
        {
            "title": "Docker Tutorial for Beginners",
            "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo",
            "platform": "YouTube",
            "duration": "3 hours",
            "level": "Beginner"
        },
        {
            "title": "Docker Mastery: with Kubernetes +Swarm",
            "url": "https://www.udemy.com/course/docker-mastery/",
            "platform": "Udemy",
            "duration": "19 hours",
            "level": "All Levels"
        }
    ],
    "kubernetes": [
        {
            "title": "Kubernetes Tutorial for Beginners",
            "url": "https://www.youtube.com/watch?v=X48VuDVv0do",
            "platform": "YouTube",
            "duration": "4 hours",
            "level": "Beginner"
        },
        {
            "title": "Kubernetes Certified Application Developer",
            "url": "https://www.udemy.com/course/certified-kubernetes-application-developer/",
            "platform": "Udemy",
            "duration": "7 hours",
            "level": "Intermediate"
        }
    ],
    "aws": [
        {
            "title": "AWS Certified Cloud Practitioner",
            "url": "https://www.youtube.com/watch?v=SOTamWNgDKc",
            "platform": "YouTube",
            "duration": "4 hours",
            "level": "Beginner"
        },
        {
            "title": "AWS Certified Solutions Architect",
            "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/",
            "platform": "Udemy",
            "duration": "27 hours",
            "level": "Intermediate"
        }
    ],
    "azure": [
        {
            "title": "Azure Fundamentals Certification",
            "url": "https://www.youtube.com/watch?v=NKEFWyqJ5XA",
            "platform": "YouTube",
            "duration": "3 hours",
            "level": "Beginner"
        },
        {
            "title": "Microsoft Azure Fundamentals",
            "url": "https://www.coursera.org/learn/microsoft-azure-fundamentals-az-900",
            "platform": "Coursera",
            "duration": "13 hours",
            "level": "Beginner"
        }
    ],
    "gcp": [
        {
            "title": "Google Cloud Platform Full Course",
            "url": "https://www.youtube.com/watch?v=jpno8FSqpc8",
            "platform": "YouTube",
            "duration": "4 hours",
            "level": "Beginner"
        },
        {
            "title": "Google Cloud Fundamentals",
            "url": "https://www.coursera.org/learn/gcp-fundamentals",
            "platform": "Coursera",
            "duration": "15 hours",
            "level": "Beginner"
        }
    ],
    "default": [
        {
            "title": "Programming Fundamentals",
            "url": "https://www.youtube.com/results?search_query=programming+fundamentals",
            "platform": "YouTube",
            "duration": "Varies",
            "level": "Beginner"
        },
        {
            "title": "Software Development Courses",
            "url": "https://www.coursera.org/browse/computer-science",
            "platform": "Coursera",
            "duration": "Varies",
            "level": "All Levels"
        },
        {
            "title": "Tech Skills Learning Path",
            "url": "https://www.udemy.com/courses/development/",
            "platform": "Udemy",
            "duration": "Varies",
            "level": "All Levels"
        }
    ]
}


def search_learning_content(skill: str) -> List[Dict[str, str]]:
    """
    Search for learning content (courses, tutorials) for a given skill.
    
    This is a mock implementation for MVP that returns hard-coded course
    recommendations based on the skill name.
    
    Args:
        skill: The skill to search courses for (e.g., "Python", "Machine Learning")
    
    Returns:
        List of course dictionaries with title, url, platform, duration, and level
    
    Example:
        >>> courses = search_learning_content("Python")
        >>> print(courses[0]["title"])
        "Python for Everybody - Full Course"
    """
    logger.info(f"Searching learning content for skill: {skill}")
    
    # Normalize skill name for lookup
    skill_normalized = skill.lower().strip()
    
    # Try exact match first
    if skill_normalized in MOCK_COURSES:
        courses = MOCK_COURSES[skill_normalized]
        logger.info(f"Found {len(courses)} courses for '{skill}'")
        return courses
    
    # Try partial match
    for key in MOCK_COURSES.keys():
        if key in skill_normalized or skill_normalized in key:
            courses = MOCK_COURSES[key]
            logger.info(f"Found {len(courses)} courses for '{skill}' (matched '{key}')")
            return courses
    
    # Return default courses if no match found
    logger.warning(f"No specific courses found for '{skill}', returning default courses")
    return MOCK_COURSES["default"]


def get_tool_definition() -> Dict:
    """
    Get the tool definition for aci.dev registration.
    
    Returns:
        Dictionary containing the tool schema for function calling
    """
    return {
        "type": "function",
        "function": {
            "name": "search_learning_content",
            "description": "Search for learning resources (courses, tutorials, documentation) for a specific skill or technology. Returns a list of recommended courses with titles, URLs, platforms, duration, and difficulty level.",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill": {
                        "type": "string",
                        "description": "The skill or technology to search courses for (e.g., 'Python', 'Machine Learning', 'React')"
                    }
                },
                "required": ["skill"]
            }
        }
    }


# Example usage and testing
if __name__ == "__main__":
    # Test the search function
    test_skills = ["Python", "Machine Learning", "React", "Unknown Skill"]
    
    for skill in test_skills:
        print(f"\n{'='*60}")
        print(f"Searching for: {skill}")
        print(f"{'='*60}")
        
        courses = search_learning_content(skill)
        
        for i, course in enumerate(courses, 1):
            print(f"\n{i}. {course['title']}")
            print(f"   Platform: {course['platform']}")
            print(f"   Duration: {course['duration']}")
            print(f"   Level: {course['level']}")
            print(f"   URL: {course['url']}")
    
    # Test tool definition
    print(f"\n{'='*60}")
    print("Tool Definition:")
    print(f"{'='*60}")
    import json
    print(json.dumps(get_tool_definition(), indent=2))