# Setup Guide

## Step-by-Step Installation

### 1. Clone the Repository
```bash
git clone https://github.com/AbhishekC1005/Hospital-Management-AI-Agent.git
cd Hospital-Management-AI-Agent
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
GOOGLE_API_KEY=your_actual_google_api_key
OPENAI_API_KEY=your_actual_openai_api_key
```

### 5. (Optional) Setup MongoDB for RAG

If you want to use the RAG functionality:

1. Create a free MongoDB Atlas account at https://www.mongodb.com/cloud/atlas
2. Create a cluster and get your connection string
3. Add MongoDB URI to `.env`
4. Run setup scripts:
```bash
python scripts/create_vector_index_simple.py
python scripts/add_documents.py
```

### 6. Run the Agent
```bash
adk web .
```

Open http://localhost:8000 in your browser.

## Getting API Keys

### Google API Key
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key to your `.env` file

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key to your `.env` file

### MongoDB Atlas (Optional)
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a cluster (M0 free tier)
4. Click "Connect" → "Connect your application"
5. Copy the connection string to your `.env` file

## Troubleshooting

### "Module not found" errors
Make sure you're in the virtual environment and have installed all dependencies:
```bash
pip install -r requirements.txt
```

### "API key not found" errors
Check that your `.env` file exists and contains valid API keys.

### MongoDB connection errors
- Ensure you're using MongoDB Atlas (not local MongoDB)
- Check that your IP is whitelisted in MongoDB Atlas Network Access
- Verify the connection string format

## Next Steps

Once setup is complete, try these example queries:
- "How many hospitals are there?"
- "List all hospitals"
- "Show me details for City General Hospital on 2024-10-20"
- "Calculate distance between hospitals"

For more information, see the main [README.md](README.md).
