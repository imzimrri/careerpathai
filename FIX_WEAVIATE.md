# Fix Weaviate Multi-Tenancy Issue

## Problem

Your Weaviate collection has multi-tenancy enabled, but the code isn't specifying a tenant.

## Solution (2 Steps)

### Step 1: Add Tenant to .env

Open your `.env` file and add this line after the Weaviate configuration:

```bash
# Weaviate Configuration
WEAVIATE_URL=https://fgw1pzpkswsu2mgtnsankq.c0.us-west3.gcp.weaviate.cloud
WEAVIATE_API_KEY=your_key_here
WEAVIATE_TENANT=default    # ← ADD THIS LINE
```

### Step 2: Restart Backend

```bash
# Stop the current backend (Ctrl+C in the terminal)
# Then restart it:
cd api
source venv/bin/activate
python index.py
```

## Alternative: Disable Multi-Tenancy in Weaviate

If you don't need multi-tenancy:

1. Go to Weaviate Console: https://console.weaviate.cloud
2. Select your cluster
3. Delete the `JobKnowledge` collection
4. Recreate it **without** multi-tenancy enabled
5. Run setup script: `cd api && python setup_weaviate_data.py`

## Test After Fix

```bash
curl -X POST http://localhost:8000/api/generate-career-path \
  -H "Content-Type: application/json" \
  -d '{"currentRole": "Frontend Developer", "targetRole": "ML Engineer"}'
```

Should now work! ✅
