# CareerPath AI - Quick Start Guide

## 🚀 How to Run the Complete Application

This guide will walk you through running the complete CareerPath AI MVP with all integrated services.

---

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Git
- API keys for all services (see Configuration section)

---

## Step 1: Clone and Setup

```bash
# Navigate to project directory
cd /Users/zimrrigudino/Documents/hackathon_projects/careerpathai

# Verify you're in the right directory
pwd
# Should output: /Users/zimrrigudino/Documents/hackathon_projects/careerpathai
```

---

## Step 2: Configure Environment Variables

### Create `.env` file from template

```bash
# Copy the example file
cp .env.example .env

# Open .env in your editor
code .env  # or use nano, vim, etc.
```

### Add Your API Keys

Edit `.env` and add your actual API keys:

```bash
# Weaviate Configuration
WEAVIATE_URL=https://your-actual-cluster.weaviate.network
WEAVIATE_API_KEY=your_actual_weaviate_api_key

# FriendliAI Configuration
FRIENDLI_TOKEN=your_actual_friendli_token
FRIENDLI_MODEL=meta-llama-3.1-8b-instruct
FRIENDLI_BASE_URL=https://api.friendli.ai/serverless/v1

# aci.dev Configuration
ACI_API_KEY=your_actual_aci_api_key
ACI_BASE_URL=https://api.aci.dev/v1

# Daytona Configuration
DAYTONA_API_KEY=dtn_4a60a3966183609c88a3e6d4362a5ea05c0264e6fe0534fb8a4103cb7fa86929
DAYTONA_BASE_URL=https://api.daytona.io/v1
DAYTONA_TIMEOUT=30

# Comet Configuration
COMET_API_KEY=your_actual_comet_api_key
COMET_PROJECT_NAME=careerpathai
COMET_WORKSPACE=default
```

**Note:** You already have the Daytona API key configured!

---

## Step 3: Setup Backend (Python/FastAPI)

### Install Python Dependencies

```bash
# Navigate to api directory
cd api

# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install all dependencies
pip install -r requirements.txt
```

### Verify Backend Installation

```bash
# Test individual components
python test_weaviate.py    # Test Weaviate connection
python test_friendli.py    # Test FriendliAI integration
python test_aci.py         # Test aci.dev integration
python test_daytona.py     # Test Daytona validation
python test_comet.py       # Test Comet observability
```

---

## Step 4: Setup Frontend (React/Vite)

### Install Frontend Dependencies

```bash
# Navigate to frontend directory (from project root)
cd ../frontend

# Install npm dependencies
npm install
```

---

## Step 5: Run the Application

### Option A: Run Backend and Frontend Separately (Recommended for Development)

**Terminal 1 - Backend:**

```bash
# From project root
cd api
source venv/bin/activate  # Activate venv
python index.py

# Backend will start on: http://localhost:8000
# API endpoint: http://localhost:8000/api/generate-career-path
```

**Terminal 2 - Frontend:**

```bash
# From project root
cd frontend
npm run dev

# Frontend will start on: http://localhost:5173
```

### Option B: Run Backend Only (API Testing)

```bash
cd api
source venv/bin/activate
python index.py

# Test with curl:
curl -X POST http://localhost:8000/api/generate-career-path \
  -H "Content-Type: application/json" \
  -d '{"currentRole": "Frontend Developer", "targetRole": "ML Engineer"}'
```

---

## Step 6: Test the Complete Workflow

### Using the Frontend UI

1. **Open Browser**

   - Navigate to: http://localhost:5173

2. **Enter Career Information**

   - Current Role: "Frontend Developer"
   - Target Role: "Machine Learning Engineer"

3. **Click "Generate Career Path"**

   - Wait for response (6-8 seconds)

4. **View Results**
   - Top 3 skills to learn
   - Course recommendations for each skill
   - Code snippet with validation result
   - Execution output

### Using API Directly (curl or Postman)

```bash
curl -X POST http://localhost:8000/api/generate-career-path \
  -H "Content-Type: application/json" \
  -d '{
    "currentRole": "Frontend Developer",
    "targetRole": "Machine Learning Engineer"
  }'
```

---

## Step 7: View Observability in Comet Dashboard

1. **Login to Comet**

   - Go to: https://www.comet.com
   - Login with your account

2. **Navigate to Project**

   - Find project: "careerpathai"
   - Click on project name

3. **View Traces**

   - Click on "Traces" tab
   - Find your recent request
   - Click to view details

4. **Explore Trace Details**
   - See all workflow steps (spans)
   - View latency breakdown
   - Check input/output for each step
   - Verify validation results

---

## Step 8: Verify All Components

### Health Check

```bash
# Check API health
curl http://localhost:8000/api/health

# Expected response:
# {
#   "api": "healthy",
#   "weaviate": "connected"
# }
```

### Component Tests

```bash
cd api
source venv/bin/activate

# Test each component
python test_weaviate.py     # Should show: ✓ Weaviate connection validated
python test_friendli.py     # Should show: ✓ FriendliAI connection validated
python test_aci.py          # Should show: ✓ aci.dev integration working
python test_code_generation.py  # Should show: ✓ Code generation working
python test_daytona.py      # Should show: 4/6 tests passed (Python validation works)
python test_comet.py        # Should show: 4/4 tests passed
```

---

## Troubleshooting

### Backend Won't Start

**Problem:** `ModuleNotFoundError` or import errors

**Solution:**

```bash
cd api
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Won't Start

**Problem:** `npm` errors or missing dependencies

**Solution:**

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### API Returns Errors

**Problem:** 503 Service Unavailable or 500 Internal Server Error

**Solution:**

1. Check `.env` file has all API keys
2. Verify Weaviate connection: `python test_weaviate.py`
3. Check backend logs for specific error
4. Verify all services are accessible

### Weaviate Connection Failed

**Problem:** "Failed to connect to Weaviate"

**Solution:**

1. Verify `WEAVIATE_URL` and `WEAVIATE_API_KEY` in `.env`
2. Check Weaviate cluster is running
3. Test connection: `python test_weaviate.py`

### Code Validation Fails

**Problem:** Daytona validation returns "Failure"

**Solution:**

1. This is expected for non-Python code (MVP supports Python only)
2. Check Daytona API key is correct
3. Verify disk quota not exceeded
4. Test: `python test_daytona.py`

### No Traces in Comet

**Problem:** Comet dashboard shows no traces

**Solution:**

1. Verify `COMET_API_KEY` in `.env`
2. Check project name matches: "careerpathai"
3. Test: `python test_comet.py`
4. Wait a few minutes for traces to appear

---

## Quick Test Commands

### Test Complete Workflow

```bash
# Terminal 1: Start backend
cd api && source venv/bin/activate && python index.py

# Terminal 2: Test API
curl -X POST http://localhost:8000/api/generate-career-path \
  -H "Content-Type: application/json" \
  -d '{"currentRole": "Frontend Developer", "targetRole": "ML Engineer"}'
```

### Test Individual Components

```bash
cd api && source venv/bin/activate

# Quick test all components
python test_weaviate.py && \
python test_friendli.py && \
python test_aci.py && \
python test_code_generation.py && \
python test_daytona.py && \
python test_comet.py
```

---

## Demo Script for Hackathon

### 1. Start Services (Before Demo)

```bash
# Terminal 1: Backend
cd api && source venv/bin/activate && python index.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

### 2. Demo Flow

1. **Show Frontend** (http://localhost:5173)

   - Clean, professional UI
   - Two input fields

2. **Enter Example**

   - Current Role: "Frontend Developer"
   - Target Role: "Machine Learning Engineer"
   - Click "Generate Career Path"

3. **Show Results**

   - Top 3 skills displayed
   - Course recommendations
   - Code snippet with validation
   - Execution output

4. **Show Comet Dashboard**

   - Open Comet in browser
   - Navigate to "careerpathai" project
   - Show the trace for this request
   - Highlight:
     - Complete workflow visibility
     - Latency breakdown
     - Validation results
     - Error handling (if any)

5. **Explain Stack**
   - Weaviate: RAG for job knowledge
   - FriendliAI: LLM for skill analysis
   - aci.dev: Tool calling for courses
   - Daytona: Secure code validation
   - Comet: End-to-end observability

---

## Production Deployment (Vercel)

### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts to:
# 1. Link to project
# 2. Configure build settings
# 3. Add environment variables
# 4. Deploy
```

### Configure Environment Variables in Vercel

1. Go to Vercel Dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add all variables from `.env`:
   - WEAVIATE_URL
   - WEAVIATE_API_KEY
   - FRIENDLI_TOKEN
   - ACI_API_KEY
   - DAYTONA_API_KEY
   - COMET_API_KEY
   - etc.

---

## Support & Documentation

### Documentation Files

- **[`README.md`](README.md)** - Project overview
- **[`docs/prd.md`](docs/prd.md)** - Product requirements
- **[`docs/architecture.md`](docs/architecture.md)** - Technical architecture
- **[`api/README_CODE_GENERATION.md`](api/README_CODE_GENERATION.md)** - Code generation guide
- **[`api/README_DAYTONA.md`](api/README_DAYTONA.md)** - Daytona integration guide

### Story Documentation

- [`docs/stories/1.1.Implement-Frontend-UI.md`](docs/stories/1.1.Implement-Frontend-UI.md)
- [`docs/stories/1.2.Implement-Weaviate-RAG-Integration.md`](docs/stories/1.2.Implement-Weaviate-RAG-Integration.md)
- [`docs/stories/1.3.Implement-FriendliAI-LLM-Integration.md`](docs/stories/1.3.Implement-FriendliAI-LLM-Integration.md)
- [`docs/stories/1.4.Implement-aci.dev-Tool-Calling.md`](docs/stories/1.4.Implement-aci.dev-Tool-Calling.md)
- [`docs/stories/1.5.Implement-Code-Snippet-Generation.md`](docs/stories/1.5.Implement-Code-Snippet-Generation.md)
- [`docs/stories/1.6.Implement-Daytona-Code-Validation.md`](docs/stories/1.6.Implement-Daytona-Code-Validation.md)
- [`docs/stories/1.7.Implement-Comet-Observability.md`](docs/stories/1.7.Implement-Comet-Observability.md)

---

## Success Checklist

Before your demo, verify:

- [ ] All API keys configured in `.env`
- [ ] Backend starts without errors: `cd api && python index.py`
- [ ] Frontend starts without errors: `cd frontend && npm run dev`
- [ ] Health check passes: `curl http://localhost:8000/api/health`
- [ ] Test request works: `curl -X POST http://localhost:8000/api/generate-career-path ...`
- [ ] Frontend displays results correctly
- [ ] Comet dashboard shows traces
- [ ] All component tests pass

---

## Quick Reference

### Start Backend

```bash
cd api && source venv/bin/activate && python index.py
```

### Start Frontend

```bash
cd frontend && npm run dev
```

### Test API

```bash
curl -X POST http://localhost:8000/api/generate-career-path \
  -H "Content-Type: application/json" \
  -d '{"currentRole": "Frontend Developer", "targetRole": "ML Engineer"}'
```

### View Logs

```bash
# Backend logs appear in Terminal 1
# Frontend logs appear in Terminal 2
# Comet traces: https://www.comet.com → careerpathai project
```

---

## 🎉 You're Ready!

Your CareerPath AI MVP is now fully functional with:

- ✅ React frontend
- ✅ FastAPI backend
- ✅ Weaviate RAG
- ✅ FriendliAI LLM
- ✅ aci.dev tool calling
- ✅ Daytona code validation
- ✅ Comet observability

**Good luck with your hackathon demo!** 🚀
