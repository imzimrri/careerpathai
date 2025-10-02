# CareerPath AI - Backend API

This directory contains the Python FastAPI backend for CareerPath AI, implementing the Weaviate RAG integration for semantic job knowledge retrieval.

## Story 1.2: Weaviate RAG Integration

This implementation covers Story 1.2 from the project documentation, providing:

- ✅ Weaviate Cloud Service connection with authentication
- ✅ Semantic search using `near_text` for job knowledge retrieval
- ✅ Structured response parsing from the `JobKnowledge` collection
- ✅ Comprehensive error handling for connection and query failures
- ✅ FastAPI endpoint structure for frontend integration

## Project Structure

```
api/
├── index.py              # Main FastAPI application and endpoint
├── weaviate_client.py    # Weaviate client wrapper and query logic
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd api
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp ../.env.example ../.env
```

Edit `.env` and add your Weaviate credentials:

```env
WEAVIATE_URL=https://your-cluster-url.weaviate.network
WEAVIATE_API_KEY=your-weaviate-api-key-here
```

### 3. Run Locally (Development)

```bash
# From the api directory
python index.py
```

The API will be available at `http://localhost:8000`

### 4. Test the API

#### Health Check

```bash
curl http://localhost:8000/api/health
```

#### Generate Career Path

```bash
curl -X POST http://localhost:8000/api/generate-career-path \
  -H "Content-Type: application/json" \
  -d '{
    "currentRole": "Frontend Developer",
    "targetRole": "Machine Learning Engineer"
  }'
```

## API Endpoints

### `GET /`

Health check endpoint returning service status.

### `GET /api/health`

Detailed health check including Weaviate connection status.

### `POST /api/generate-career-path`

Main endpoint for generating career paths.

**Request Body:**

```json
{
  "currentRole": "string",
  "targetRole": "string"
}
```

**Response:**

```json
{
  "title": "string",
  "skillsToLearn": ["string"],
  "recommendedCourses": [
    {
      "skill": "string",
      "url": "string"
    }
  ],
  "codeValidationResult": {
    "skill": "string",
    "status": "Success|Failure",
    "details": "string"
  }
}
```

## Weaviate Integration Details

### Collection Schema

- **Collection Name:** `JobKnowledge`
- **Properties:**
  - `title` (text): Job role or skill title
  - `description` (text): Detailed description
  - `category` (text): Category classification
- **Vectorizer:** `text2vec-transformers`

### Query Configuration

- **Method:** `near_text` semantic search
- **Default Limit:** 5 documents
- **Certainty Threshold:** 0.7 (configurable)

### Error Handling

The implementation includes comprehensive error handling for:

- ❌ Authentication failures
- ❌ Connection timeouts
- ❌ Empty result sets
- ❌ Network errors
- ❌ Invalid queries

All errors are logged and return appropriate HTTP status codes.

## Testing

### Manual Testing (MVP Approach)

1. **Test Weaviate Connection:**

   ```bash
   python weaviate_client.py
   ```

2. **Test with Valid Target Role:**

   ```bash
   curl -X POST http://localhost:8000/api/generate-career-path \
     -H "Content-Type: application/json" \
     -d '{"currentRole": "Frontend Developer", "targetRole": "Machine Learning Engineer"}'
   ```

3. **Test with Unknown Target Role:**

   ```bash
   curl -X POST http://localhost:8000/api/generate-career-path \
     -H "Content-Type: application/json" \
     -d '{"currentRole": "Developer", "targetRole": "Quantum Computing Specialist"}'
   ```

4. **Test Error Handling:**
   - Remove Weaviate credentials from `.env`
   - Restart the server
   - Attempt to generate a career path
   - Should receive 503 error

## Deployment (Vercel)

This API is designed to run as a Vercel Serverless Function.

### Prerequisites

- Vercel account
- Vercel CLI installed: `npm i -g vercel`

### Deploy Steps

1. **Set Environment Variables in Vercel:**

   ```bash
   vercel env add WEAVIATE_URL
   vercel env add WEAVIATE_API_KEY
   ```

2. **Deploy:**
   ```bash
   vercel --prod
   ```

The API will be available at your Vercel deployment URL.

## Future Stories Integration

This implementation is designed to integrate with upcoming stories:

- **Story 1.3:** FriendliAI LLM integration for skill gap analysis
- **Story 1.4:** aci.dev tool calling for course recommendations
- **Story 1.5:** Daytona code validation
- **Story 1.6:** Comet observability and logging

The current mock response in [`index.py`](index.py:147) will be replaced with actual orchestration logic.

## Troubleshooting

### Connection Issues

- Verify Weaviate URL and API key in `.env`
- Check Weaviate Cloud Service status
- Ensure network connectivity

### Empty Results

- Verify the `JobKnowledge` collection exists in Weaviate
- Check if collection has data
- Lower the certainty threshold if needed

### Import Errors

- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use Python 3.11 or higher

## Development Notes

- The implementation follows the architecture defined in [`docs/architecture.md`](../docs/architecture.md)
- All acceptance criteria from [`docs/stories/1.2.Implement-Weaviate-RAG-Integration.md`](../docs/stories/1.2.Implement-Weaviate-RAG-Integration.md) are met
- Code includes comprehensive logging for debugging
- Error messages are user-friendly and informative

## Contact

For questions or issues, refer to the project documentation in the `docs/` directory.
