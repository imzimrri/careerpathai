"""
Script to set up Weaviate JobKnowledge collection with sample data.
Run this once to populate your Weaviate instance with job/skill knowledge.
"""

import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.config import Property, DataType

# Load environment variables
load_dotenv()

# Sample job knowledge data
SAMPLE_DATA = [
    {
        "title": "Machine Learning Engineer",
        "description": "Designs, builds, and deploys machine learning models and systems. Requires strong programming skills in Python, understanding of ML algorithms, deep learning frameworks like TensorFlow or PyTorch, and experience with data preprocessing and model optimization.",
        "category": "AI/ML"
    },
    {
        "title": "Python Programming",
        "description": "Core programming language for data science, machine learning, and backend development. Essential skills include object-oriented programming, data structures, algorithms, and familiarity with libraries like NumPy, Pandas, and scikit-learn.",
        "category": "Programming"
    },
    {
        "title": "Deep Learning",
        "description": "Advanced machine learning technique using neural networks. Requires understanding of architectures like CNNs, RNNs, Transformers, and frameworks like TensorFlow, PyTorch, or Keras. Applications include computer vision, NLP, and generative AI.",
        "category": "AI/ML"
    },
    {
        "title": "Data Structures and Algorithms",
        "description": "Fundamental computer science concepts essential for efficient programming. Includes arrays, linked lists, trees, graphs, sorting, searching, dynamic programming, and complexity analysis. Critical for technical interviews and system design.",
        "category": "Computer Science"
    },
    {
        "title": "Natural Language Processing",
        "description": "Field of AI focused on enabling computers to understand and generate human language. Involves text preprocessing, tokenization, embeddings, transformers, and applications like chatbots, translation, and sentiment analysis.",
        "category": "AI/ML"
    },
    {
        "title": "Software Engineer",
        "description": "Designs, develops, and maintains software applications. Requires proficiency in programming languages, software design patterns, version control (Git), testing, debugging, and collaboration in agile teams.",
        "category": "Software Development"
    },
    {
        "title": "Data Scientist",
        "description": "Analyzes complex data to extract insights and build predictive models. Requires statistics, machine learning, data visualization, SQL, Python/R programming, and business acumen to translate findings into actionable recommendations.",
        "category": "Data Science"
    },
    {
        "title": "Cloud Computing (AWS/Azure/GCP)",
        "description": "Deploying and managing applications on cloud platforms. Includes understanding of compute services, storage, databases, networking, security, and infrastructure as code. Essential for modern scalable applications.",
        "category": "Infrastructure"
    },
    {
        "title": "Docker and Kubernetes",
        "description": "Containerization and orchestration technologies for deploying applications. Docker packages applications with dependencies, while Kubernetes manages container deployment, scaling, and operations at scale.",
        "category": "DevOps"
    },
    {
        "title": "SQL and Database Management",
        "description": "Querying and managing relational databases. Includes writing complex queries, database design, indexing, optimization, transactions, and understanding of both SQL and NoSQL databases.",
        "category": "Data Engineering"
    },
    {
        "title": "React and Frontend Development",
        "description": "Building modern web user interfaces with React. Requires JavaScript/TypeScript, component architecture, state management, hooks, and understanding of web fundamentals (HTML, CSS, responsive design).",
        "category": "Frontend Development"
    },
    {
        "title": "API Development and RESTful Services",
        "description": "Designing and implementing web APIs. Includes REST principles, HTTP methods, authentication, API documentation, versioning, and frameworks like FastAPI, Express, or Django REST Framework.",
        "category": "Backend Development"
    },
    {
        "title": "Computer Vision",
        "description": "Enabling computers to interpret and understand visual information. Involves image processing, object detection, segmentation, CNNs, and applications in autonomous vehicles, medical imaging, and facial recognition.",
        "category": "AI/ML"
    },
    {
        "title": "Git and Version Control",
        "description": "Managing code changes and collaboration. Includes branching strategies, merging, pull requests, conflict resolution, and best practices for team development workflows.",
        "category": "Development Tools"
    },
    {
        "title": "System Design and Architecture",
        "description": "Designing scalable, reliable software systems. Covers distributed systems, microservices, load balancing, caching, databases, message queues, and trade-offs in architectural decisions.",
        "category": "Software Architecture"
    }
]


def setup_collection():
    """Set up the JobKnowledge collection in Weaviate."""
    
    # Get credentials
    url = os.getenv("WEAVIATE_URL")
    api_key = os.getenv("WEAVIATE_API_KEY")
    
    if not url or not api_key:
        print("❌ Error: WEAVIATE_URL and WEAVIATE_API_KEY must be set in .env")
        return False
    
    print(f"Connecting to Weaviate at {url}...")
    
    try:
        # Connect to Weaviate
        client = weaviate.connect_to_wcs(
            cluster_url=url,
            auth_credentials=weaviate.auth.AuthApiKey(api_key),
        )
        
        if not client.is_ready():
            print("❌ Failed to connect to Weaviate")
            return False
        
        print("✅ Connected to Weaviate")
        
        # Check if collection already exists
        if client.collections.exists("JobKnowledge"):
            print("⚠️  JobKnowledge collection already exists")
            response = input("Do you want to delete and recreate it? (yes/no): ")
            if response.lower() == 'yes':
                client.collections.delete("JobKnowledge")
                print("🗑️  Deleted existing collection")
            else:
                print("Keeping existing collection")
                client.close()
                return True
        
        # Note: Collection should be created via Weaviate Console UI
        # This script only adds data to an existing collection
        print("\n📝 Please create the JobKnowledge collection in Weaviate Console first:")
        print("   1. Go to your Weaviate Console")
        print("   2. Create collection named: JobKnowledge")
        print("   3. Add properties: title, description, category (all text)")
        print("   4. Select a vectorizer (e.g., text2vec-cohere or text2vec-openai)")
        print("   5. Then run this script again to add sample data")
        
        client.close()
        return False
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def add_sample_data():
    """Add sample job knowledge data to the collection."""
    
    # Get credentials
    url = os.getenv("WEAVIATE_URL")
    api_key = os.getenv("WEAVIATE_API_KEY")
    
    print(f"Connecting to Weaviate at {url}...")
    
    try:
        # Connect to Weaviate
        client = weaviate.connect_to_wcs(
            cluster_url=url,
            auth_credentials=weaviate.auth.AuthApiKey(api_key),
        )
        
        if not client.is_ready():
            print("❌ Failed to connect to Weaviate")
            return False
        
        print("✅ Connected to Weaviate")
        
        # Check if collection exists
        if not client.collections.exists("JobKnowledge"):
            print("❌ JobKnowledge collection does not exist")
            print("   Please create it in Weaviate Console first")
            client.close()
            return False
        
        # Get the collection
        collection = client.collections.get("JobKnowledge")
        
        # Add sample data
        print(f"\n📥 Adding {len(SAMPLE_DATA)} sample records...")
        
        with collection.batch.dynamic() as batch:
            for i, data in enumerate(SAMPLE_DATA, 1):
                batch.add_object(properties=data)
                print(f"   {i}. Added: {data['title']}")
        
        print(f"\n✅ Successfully added {len(SAMPLE_DATA)} records to JobKnowledge collection")
        
        # Verify by querying
        print("\n🔍 Verifying data with a test query...")
        response = collection.query.near_text(
            query="Machine Learning Engineer",
            limit=3
        )
        
        print(f"   Found {len(response.objects)} results for 'Machine Learning Engineer'")
        for obj in response.objects:
            print(f"   - {obj.properties['title']}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("WEAVIATE JOBKNOWLEDGE SETUP")
    print("=" * 60)
    print()
    
    # First check if collection exists
    if not setup_collection():
        print("\n⚠️  Collection not ready. Please create it in Weaviate Console.")
        print("   After creating the collection, run this script again to add data.")
    else:
        # Add sample data
        if add_sample_data():
            print("\n🎉 Setup complete! You can now run the tests:")
            print("   python test_weaviate.py")
        else:
            print("\n❌ Failed to add sample data")