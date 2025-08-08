# Blog Generator API

An AI-powered blog generation service built with FastAPI and LangGraph, featuring robust error handling and retry mechanisms.

## Features

- ✅ **AI-Powered Content Generation**: Uses Groq LLM for high-quality blog content
- ✅ **Robust Error Handling**: Comprehensive error recovery with user intervention options
- ✅ **Interactive Topic Input**: Prompts for topic if not provided
- ✅ **Retry Logic**: Automatic retries with exponential backoff for LLM failures
- ✅ **FastAPI Integration**: Production-ready REST API with automatic documentation
- ✅ **State Management**: Sophisticated state tracking through LangGraph
- ✅ **Fallback Mechanisms**: Graceful degradation when components fail

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   LangGraph      │    │   Groq LLM      │
│   (REST API)    │───▶│   (Workflow)     │───▶│   (Content Gen) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Error         │    │   State          │    │   Retry         │
│   Handling      │    │   Management     │    │   Logic         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
LANGSMITH_API_KEY=your_langsmith_key_here  # Optional
```

### 3. Run the Server

```bash
python app.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /blogs
Generate a blog post

**Request:**
```json
{
  "topic": "The Future of Artificial Intelligence",
  "language": "English"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "topic": "The Future of Artificial Intelligence",
    "language": "English",
    "blog": {
      "title": "AI Revolution: Shaping Tomorrow's World",
      "content": "## Introduction\n\nArtificial Intelligence..."
    }
  },
  "message": "Blog generated successfully"
}
```

### GET /health
Health check endpoint

### GET /
API information and available endpoints

### GET /docs
Automatic API documentation (Swagger UI)

## Error Handling

The system handles various error scenarios:

1. **Missing Topic**: Prompts user for input interactively
2. **LLM Failures**: Automatic retries with user intervention options
3. **API Key Issues**: Clear error messages and configuration guidance
4. **Network Issues**: Graceful degradation with fallback responses

## Testing

Run the test suite:

```bash
python test_api.py
```

Or test manually with curl:

```bash
# Test with topic
curl -X POST "http://localhost:8000/blogs" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Machine Learning Trends", "language": "English"}'

# Health check
curl "http://localhost:8000/health"
```

## Project Structure

```
Blog Generator/
├── app.py                 # FastAPI application
├── main.py               # Entry point
├── test_api.py           # API test suite
├── requirements.txt      # Dependencies
├── .env                 # Environment variables
└── src/
    ├── __init__.py
    ├── graphs/
    │   ├── __init__.py
    │   └── graph_builder.py    # LangGraph workflow builder
    ├── llms/
    │   ├── __init__.py
    │   └── groqllm.py          # Groq LLM wrapper
    ├── nodes/
    │   ├── __init__.py
    │   └── blog_node.py        # Blog generation nodes
    └── states/
        ├── __init__.py
        └── blogstate.py        # State management
```

## Development

### Key Components

1. **BlogState**: Pydantic model for state management
2. **BlogNode**: Core logic for title and content generation
3. **GraphBuilder**: LangGraph workflow orchestration
4. **GroqLLM**: LLM client with error handling

### Error Recovery Flow

```
Topic Missing? ──► Prompt User ──► Continue
     │                              │
     ▼                              ▼
LLM Failed? ──► Retry (3x) ──► User Decision ──► Retry/Skip/Cancel
     │                              │
     ▼                              ▼
Max Retries? ──► Fallback ──► Continue/End
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details
