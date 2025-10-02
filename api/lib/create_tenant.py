"""Script to create a tenant in Weaviate JobKnowledge collection."""

import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.tenants import Tenant

load_dotenv()

url = os.getenv("WEAVIATE_URL")
api_key = os.getenv("WEAVIATE_API_KEY")
tenant_name = os.getenv("WEAVIATE_TENANT", "default")

print(f"Connecting to Weaviate...")
client = weaviate.connect_to_wcs(
    cluster_url=url,
    auth_credentials=weaviate.auth.AuthApiKey(api_key)
)

print("✅ Connected")

# Get collection
collection = client.collections.get("JobKnowledge")

# Create tenant
print(f"\nCreating tenant: {tenant_name}")
try:
    collection.tenants.create(
        tenants=[Tenant(name=tenant_name)]
    )
    print(f"✅ Created tenant: {tenant_name}")
except Exception as e:
    print(f"Error creating tenant: {e}")
    print("(Tenant might already exist)")

# List tenants to verify
print("\nCurrent tenants:")
try:
    tenants = collection.tenants.get()
    for tenant in tenants:
        print(f"  - {tenant.name}")
except Exception as e:
    print(f"Error listing tenants: {e}")

client.close()
print("\n✅ Done! Now restart your backend server.")