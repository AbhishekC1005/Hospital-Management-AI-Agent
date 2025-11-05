# Setup Guide - Healthcare Decision Support System (CrewAI)

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- OpenAI API Key
- MongoDB Atlas account (optional, for RAG features)

## Installation Steps

### 1. Navigate to Method 2 Directory

```bash
cd "method 2"
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `method 2` directory:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux
```

Edit the `.env` file with your API keys:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for RAG features)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=rag_database
MONGODB_COLLECTION=documents
MONGODB_VECTOR_INDEX=vector_index
```

### 5. Get API Keys

#### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and paste it in your `.env` file

#### MongoDB Atlas (Optional)
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get your connection string
4. Add it to your `.env` file

### 6. Verify Data Files

Ensure the CSV data file exists:
```
method 2/agent/data/hospital_trends.csv
```

### 7. Run the Application

```bash
python main.py
```

The application will start on http://localhost:8001

### 8. Access the Application

Open your browser and navigate to:
```
http://localhost:8001
```

## Testing the Application

Try these sample queries:

1. **Basic Information:**
   - "How many hospitals are in the system?"
   - "List all hospital names"
   - "What dates are available?"

2. **Detailed Analysis:**
   - "Show me details for City General Hospital on 2024-10-20"
   - "What is the bed occupancy for Regional Medical Center?"

3. **Distance Calculations:**
   - "Calculate distance between City General Hospital and Metropolitan Hospital"
   - "Show me all hospital distances"

4. **Strategic Insights:**
   - "Recommend resource transfers between hospitals"
   - "What are the top priorities for today?"

## Troubleshooting

### Issue: Module not found errors
**Solution:** Make sure you're in the virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: OpenAI API errors
**Solution:** Verify your API key is correct in the `.env` file and you have credits available.

### Issue: Port 8001 already in use
**Solution:** Change the port in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8002)  # Change to 8002 or any available port
```

### Issue: CSV file not found
**Solution:** Ensure the data file exists at `agent/data/hospital_trends.csv`

## Architecture Overview

### CrewAI Multi-Agent System

This implementation uses CrewAI with 4 specialized agents:

1. **Data Analyst Agent**
   - Retrieves hospital counts, names, locations
   - Analyzes detailed metrics
   - Provides data-driven insights

2. **Distance Calculator Agent**
   - Calculates distances between hospitals
   - Provides spatial analysis
   - Optimizes resource transfers

3. **Knowledge Retriever Agent**
   - Retrieves healthcare best practices
   - Provides evidence-based recommendations
   - Accesses knowledge base via RAG

4. **Decision Support Agent**
   - Synthesizes information from all agents
   - Provides strategic recommendations
   - Coordinates agent collaboration

### Process Flow

1. User submits query
2. CrewAI creates a crew with all agents
3. Agents work sequentially on assigned tasks
4. Decision Support Agent synthesizes results
5. Final response returned to user

## Differences from Method 1

| Feature | Method 1 (Google ADK) | Method 2 (CrewAI) |
|---------|----------------------|-------------------|
| Framework | Google ADK | CrewAI |
| Model | OpenAI via LiteLLM | OpenAI GPT-4 |
| Architecture | Single agent with tools | Multi-agent crew |
| Session Management | Built-in | Stateless |
| Preference Learning | Yes | No |
| Port | 8000 | 8001 |

## Next Steps

1. Explore the different query types
2. Test the multi-agent collaboration
3. Compare responses with Method 1
4. Customize agents for your use case
5. Add more tools and capabilities

## Support

For issues or questions:
- Check the troubleshooting section
- Review the README.md
- Check CrewAI documentation: https://docs.crewai.com/

## License

MIT License
