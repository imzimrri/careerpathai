"""
Weaviate client module for RAG-based job knowledge retrieval.
Implements semantic search for career path recommendations.
"""

import os
import logging
from typing import List, Dict, Optional
import weaviate
from weaviate.classes.query import MetadataQuery

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeaviateClient:
    """
    Client for interacting with Weaviate Cloud Service.
    Handles connection, authentication, and semantic search queries.
    """
    
    def __init__(self):
        """Initialize Weaviate client with environment configuration."""
        self.url = os.getenv("WEAVIATE_URL")
        self.api_key = os.getenv("WEAVIATE_API_KEY")
        self.tenant = os.getenv("WEAVIATE_TENANT", "default")  # Default tenant
        self.client = None
        self.collection_name = "JobKnowledge"
        
        if not self.url or not self.api_key:
            logger.warning("Weaviate credentials not found in environment variables")
    
    def connect(self) -> bool:
        """
        Establish connection to Weaviate Cloud Service.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Get OpenAI API key for vectorization
            openai_key = os.getenv("OPENAI_APIKEY") or os.getenv("OPENAI_API_KEY")
            
            # Prepare headers for OpenAI integration
            headers = {}
            if openai_key:
                headers["X-OpenAI-Api-Key"] = openai_key
            
            # Connect to Weaviate Cloud Service
            # Note: Removed proxies parameter for compatibility with weaviate-client 4.4.0
            self.client = weaviate.connect_to_wcs(
                cluster_url=self.url,
                auth_credentials=weaviate.auth.AuthApiKey(self.api_key),
                headers=headers if headers else None
            )
            
            # Validate connection
            if self.client.is_ready():
                logger.info("Successfully connected to Weaviate")
                return True
            else:
                logger.error("Weaviate client is not ready")
                return False
                
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate: {str(e)}")
            return False
    
    def disconnect(self):
        """Close the Weaviate client connection."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from Weaviate")
    
    def query_job_knowledge(
        self, 
        target_role: str, 
        limit: int = 5, 
        certainty: float = 0.7
    ) -> List[Dict[str, str]]:
        """
        Perform semantic search for job knowledge based on target role.
        
        Args:
            target_role: The desired job role to search for
            limit: Maximum number of results to return (default: 5)
            certainty: Minimum certainty threshold for results (default: 0.7)
        
        Returns:
            List of dictionaries containing job knowledge documents with fields:
            - title: Job role or skill title
            - description: Detailed description
            - category: Category classification
        
        Raises:
            Exception: If query fails or connection is not established
        """
        if not self.client:
            raise Exception("Weaviate client not connected. Call connect() first.")
        
        try:
            # Get the collection with tenant support
            collection = self.client.collections.get(self.collection_name)
            
            # Check if collection has multi-tenancy enabled
            # If so, we need to specify a tenant
            try:
                # Try with tenant first
                collection_with_tenant = collection.with_tenant(self.tenant)
                response = collection_with_tenant.query.near_text(
                    query=target_role,
                    limit=limit,
                    certainty=certainty,
                    return_metadata=MetadataQuery(certainty=True)
                )
            except Exception as tenant_error:
                # If tenant fails, try without tenant (collection might not have multi-tenancy)
                logger.debug(f"Tenant query failed, trying without tenant: {str(tenant_error)}")
                response = collection.query.near_text(
                    query=target_role,
                    limit=limit,
                    certainty=certainty,
                    return_metadata=MetadataQuery(certainty=True)
                )
            
            # Parse and structure results
            results = []
            for obj in response.objects:
                result = {
                    "title": obj.properties.get("title", ""),
                    "description": obj.properties.get("description", ""),
                    "category": obj.properties.get("category", ""),
                    "certainty": obj.metadata.certainty if obj.metadata else None
                }
                results.append(result)
            
            logger.info(f"Retrieved {len(results)} documents for target role: {target_role}")
            
            if not results:
                logger.warning(f"No results found for target role: {target_role}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error querying Weaviate: {str(e)}")
            raise Exception(f"Failed to query job knowledge: {str(e)}")


def get_weaviate_client() -> WeaviateClient:
    """
    Factory function to create and return a Weaviate client instance.
    
    Returns:
        WeaviateClient: Configured Weaviate client instance
    """
    return WeaviateClient()


# Example usage and testing
if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create client
    client = get_weaviate_client()
    
    # Test connection
    if client.connect():
        try:
            # Test query
            results = client.query_job_knowledge("Machine Learning Engineer")
            print(f"\nFound {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   Category: {result['category']}")
                print(f"   Certainty: {result.get('certainty', 'N/A')}")
                print(f"   Description: {result['description'][:100]}...")
        finally:
            client.disconnect()
    else:
        print("Failed to connect to Weaviate")