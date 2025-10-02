# CareerPath AI

A personalized AI career coach that helps developers transition between roles using RAG (Retrieval-Augmented Generation) and agentic workflows.

## 🎯 Project Overview

CareerPath AI demonstrates a complete end-to-end AI agent system that:

- Uses **Weaviate** for semantic job knowledge retrieval (RAG)
- Leverages **FriendliAI** for intelligent skill gap analysis
- Calls **aci.dev** tools for course recommendations
- Validates code with **Daytona** secure sandboxes
- Tracks everything with **Comet** observability

## 🏗️ Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────────────────────┐
│     Vercel Platform                 │
│  ┌──────────────┐  ┌─────────────┐ │
│  │ React SPA    │  │ Python API  │ │
│  │ (Frontend)   │◄─┤ (FastAPI)   │ │
│  └──────────────┘  └──────┬──────┘ │
└────────────────────────────┼────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
   ┌─────────┐         ┌──────────┐        ┌─────────┐
   │Weaviate │         │FriendliAI│        │ aci.dev │
   │  (RAG)  │         │  (LLM)   │        │ (Tools) │
   └─────────┘         └──────────┘        └─────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                    ┌─────────────────┐
                    │ Daytona & Comet │
                    └─────────────────┘
```

## 📁 Project Structure

```
careerpathai/
├── api/                      # Python FastAPI backend
│   ├── index.py             # Main API endpoint
│   ├── weaviate_client.py   # Weaviate RAG integration
│   ├── requirements.txt     # Python dependencies
│   ├── test_weaviate.py     # Test suite
│   └── README.md            # Backend documentation
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   └── services/        # API service layer
│   └── package.json
├── docs/                     # Project documentation
│   ├── prd.md               # Product requirements
│   ├── architecture.md      # Technical architecture
│   └── stories/             # User stories
├── .env.example             # Environment variables template
├── vercel.json              # Vercel deployment config
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Weaviate Cloud account
- Vercel account (for deployment)

### 1. Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd careerpathai

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../api
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
# Required for Story 1.2:
# - WEAVIATE_URL
# - WEAVIATE_API_KEY
```

### 3. Run Locally

**Backend (Terminal 1):**

```bash
cd api
python index.py
# API runs on http://localhost:8000
```

**Frontend (Terminal 2):**

```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

### 4. Test the Integration

```bash
# Run Weaviate integration tests
cd api
python test_weaviate.py
```

## 📊 Current Implementation Status

### ✅ Completed Stories

- **Story 1.1:** Frontend UI Implementation

  - Two-field form (Current Role, Target Role)
  - Result display with skills and courses
  - Error handling and loading states
  - Responsive Bootstrap design

- **Story 1.2:** Weaviate RAG Integration ⭐ **CURRENT**
  - Weaviate Cloud Service connection
  - Semantic search with `near_text`
  - Query `JobKnowledge` collection
  - Comprehensive error handling
  - Structured response parsing

### 🔄 Upcoming Stories

- **Story 1.3:** FriendliAI LLM Integration
- **Story 1.4:** aci.dev Tool Calling
- **Story 1.5:** Daytona Code Validation
- **Story 1.6:** Comet Observability

## 🧪 Testing

### Manual Testing (MVP Approach)

The project follows a manual testing strategy suitable for hackathon MVPs:

1. **Frontend Testing:**

   - Open http://localhost:5173
   - Enter roles and submit
   - Verify UI updates correctly

2. **Backend Testing:**

   - Run test suite: `python api/test_weaviate.py`
   - Test API endpoint: `curl http://localhost:8000/api/health`
   - Test career path generation (see API README)

3. **Integration Testing:**
   - Submit form from frontend
   - Verify backend receives request
   - Check Weaviate query execution
   - Confirm response rendering

## 📚 API Documentation

### Main Endpoint

**POST** `/api/generate-career-path`

**Request:**

```json
{
  "currentRole": "Frontend Developer",
  "targetRole": "Machine Learning Engineer"
}
```

**Response:**

```json
{
  "title": "Your Path from Frontend Developer to Machine Learning Engineer",
  "skillsToLearn": ["Python", "ML Fundamentals", "Data Structures"],
  "recommendedCourses": [
    {
      "skill": "Python",
      "url": "https://example.com/course"
    }
  ],
  "codeValidationResult": {
    "skill": "Python",
    "status": "Success",
    "details": "Code executed successfully"
  }
}
```

See [`api/README.md`](api/README.md) for complete API documentation.

## 🔧 Technology Stack

| Component     | Technology            | Purpose             |
| ------------- | --------------------- | ------------------- |
| Frontend      | React 18 + Vite       | User interface      |
| UI Library    | Bootstrap 5           | Styling and layout  |
| Backend       | Python 3.11 + FastAPI | API orchestration   |
| Vector DB     | Weaviate Cloud        | RAG knowledge base  |
| LLM           | FriendliAI            | Skill analysis      |
| Tools         | aci.dev               | Course search       |
| Sandbox       | Daytona               | Code validation     |
| Observability | Comet                 | Logging and tracing |
| Deployment    | Vercel                | Hosting             |

## 🚢 Deployment

### Deploy to Vercel

1. **Install Vercel CLI:**

   ```bash
   npm i -g vercel
   ```

2. **Set Environment Variables:**

   ```bash
   vercel env add WEAVIATE_URL
   vercel env add WEAVIATE_API_KEY
   # Add other variables as needed
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

The application will be available at your Vercel deployment URL.

## 📖 Documentation

- [`docs/prd.md`](docs/prd.md) - Product Requirements Document
- [`docs/architecture.md`](docs/architecture.md) - Technical Architecture
- [`docs/stories/`](docs/stories/) - User Stories and Implementation Details
- [`api/README.md`](api/README.md) - Backend API Documentation

## 🐛 Troubleshooting

### Weaviate Connection Issues

```bash
# Verify credentials
cat .env | grep WEAVIATE

# Test connection
cd api
python test_weaviate.py
```

### Frontend Not Connecting to Backend

- Ensure backend is running on port 8000
- Check CORS configuration in [`api/index.py`](api/index.py:28)
- Verify API endpoint in [`frontend/src/services/api.js`](frontend/src/services/api.js:2)

### Import Errors

```bash
# Reinstall dependencies
cd api
pip install -r requirements.txt

cd ../frontend
npm install
```

## 🤝 Contributing

This is a hackathon project. For questions or issues:

1. Check the documentation in `docs/`
2. Review the story files in `docs/stories/`
3. Run the test suite: `python api/test_weaviate.py`

## 📝 License

This project is created for hackathon demonstration purposes.

## 🎉 Acknowledgments

Built with:

- [Weaviate](https://weaviate.io/) - Vector database
- [FriendliAI](https://friendli.ai/) - LLM inference
- [aci.dev](https://aci.dev/) - Agent tools
- [Daytona](https://daytona.io/) - Secure runtime
- [Comet](https://www.comet.com/) - ML observability
- [Vercel](https://vercel.com/) - Deployment platform

---

**Current Status:** Story 1.2 (Weaviate RAG Integration) - ✅ Complete

**Next Up:** Story 1.3 (FriendliAI LLM Integration)
