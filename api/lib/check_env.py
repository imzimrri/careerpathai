"""Quick script to check if environment variables are loaded correctly."""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*60)
print("ENVIRONMENT VARIABLES CHECK")
print("="*60)

env_vars = [
    "WEAVIATE_URL",
    "WEAVIATE_API_KEY",
    "WEAVIATE_TENANT",
    "FRIENDLI_TOKEN",
    "ACI_API_KEY",
    "DAYTONA_API_KEY",
    "COMET_API_KEY"
]

for var in env_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if "KEY" in var or "TOKEN" in var:
            masked = value[:10] + "..." if len(value) > 10 else "***"
            print(f"✅ {var}: {masked}")
        else:
            print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var}: NOT SET")

print("="*60)

# Check Weaviate tenant specifically
tenant = os.getenv("WEAVIATE_TENANT", "default")
print(f"\nWeaviate Tenant: {tenant}")
print("\nIf WEAVIATE_TENANT shows 'default' but you didn't set it,")
print("that means it's using the fallback value.")
print("Please add 'WEAVIATE_TENANT=default' to your .env file")
print("and restart the backend server.")