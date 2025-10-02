"""Script to list tenants in Weaviate JobKnowledge collection."""

import os
from dotenv import load_dotenv
import weaviate

load_dotenv()

url = os.getenv("WEAVIATE_URL")
api_key = os.getenv("WEAVIATE_API_KEY")

print("Connecting to Weaviate...")
client = weaviate.connect_to_wcs(
    cluster_url=url,
    auth_credentials=weaviate.auth.AuthApiKey(api_key)
)

print("✅ Connected")

# Get collection
collection = client.collections.get("JobKnowledge")

# List tenants
print("\nListing tenants in JobKnowledge collection:")
try:
    tenants = collection.tenants.get()
    if tenants:
        for tenant in tenants:
            print(f"  - {tenant.name}")
    else:
        print("  No tenants found")
except Exception as e:
    print(f"Error listing tenants: {e}")

client.close()