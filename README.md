# Healthcare Decision Support System

A comprehensive healthcare resource optimization platform implementing two distinct artificial intelligence approaches for hospital management and decision support. The system provides real-time analytics, resource tracking, and intelligent recommendations through different agent architectures.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)

## System Architecture

```plaintext
Healthcare Decision Support System
├── Common Infrastructure
│   ├── Web Layer
│   │   ├── FastAPI Server
│   │   ├── CORS Middleware
│   │   └── Static File Hosting
│   │
│   ├── Data Layer
│   │   ├── Hospital Metrics Store
│   │   └── Vector Database (RAG)
│   │
│   └── Authentication
│       └── API Key Management
│
├── Method 1 - ADK Implementation
│   ├── Core Components
│   │   ├── LLM Agent (Google ADK)
│   │   └── Session Management
│   │
│   ├── Tool Integration
│   │   ├── Hospital Analytics
│   │   ├── Preference Management
│   │   └── RAG Functions
│   │
│   └── Features
│       ├── Hospital Data Analysis
│       ├── Distance Calculations
│       └── Resource Tracking
│
└── Method 2 - CrewAI Implementation
    ├── Agent Network
    │   ├── Analysis Agent
    │   ├── Resource Agent
    │   └── Decision Agent
    │
    ├── Session Management
    │   ├── Context Tracking
    │   └── State Management
    │
    └── Features
        ├── Multi-Agent Collaboration
        ├── Hospital Comparisons
        └── Capacity Analysis

```

## Implementation Overview

This repository contains two different implementations of the same healthcare decision support system:

### Method 1: Google ADK Implementation
- **Framework**: Google Agent Development Kit (ADK)
- **Model**: OpenAI GPT-4o-mini via LiteLLM
- **Architecture**: Single agent with multiple tools
- **Features**: Session management, preference learning, user feedback
- **Port**: 8000

### Method 2: CrewAI Implementation
- **Framework**: CrewAI
- **Model**: OpenAI GPT-4o-mini
- **Architecture**: Multi-agent crew with specialized roles
- **Features**: Session memory, conversational AI, adaptive query routing
- **Port**: 8001

## 🚀 Quick Start

### Method 1 (Google ADK)

```bash
cd "method 1"
pip install -r requirements.txt
# Configure .env with GOOGLE_API_KEY and OPENAI_API_KEY
adk web .
```

Open http://localhost:8000

### Method 2 (CrewAI)

```bash
cd "method 2"
pip install -r requirements.txt
# Configure .env with OPENAI_API_KEY
python main.py
```

Open http://localhost:8001

## 📊 Features Comparison

| Feature | Method 1 (Google ADK) | Method 2 (CrewAI) |
|---------|----------------------|-------------------|
| Framework | Google ADK | CrewAI |
| Architecture | Single Agent | Multi-Agent Crew |
| Session Management | ✅ Built-in | ✅ Custom |
| Preference Learning | ✅ Yes | ❌ No |
| User Feedback | ✅ Like/Dislike | ❌ No |
| Conversational AI | ⚠️ Basic | ✅ Advanced |
| Query Routing | ❌ No | ✅ Adaptive |
| Response Speed | Fast | Moderate |
| Setup Complexity | Medium | Easy |

## 🎯 Use Cases

### When to Use Method 1 (Google ADK)
- Need preference learning and user feedback
- Want built-in session management
- Prefer Google's ecosystem
- Need faster response times

### When to Use Method 2 (CrewAI)
- Need multi-agent collaboration
- Want better conversational AI
- Prefer OpenAI-only stack
- Need adaptive query routing

## 📋 Common Features

Both implementations provide:

- **Hospital Data Analysis**: 40+ metrics per hospital
- **Distance Calculations**: Between hospitals with travel time estimates
- **Resource Tracking**: Beds, ICU, ventilators, staff, supplies
- **Analytics**: Trends, comparisons, system-wide statistics
- **Web Interface**: Modern, responsive UI
- **Session Memory**: Remembers user context

## 🛠️ Technology Stack

### Common Technologies
- Python 3.10+
- FastAPI (web framework)
- Pandas (data analysis)
- OpenAI (embeddings)
- MongoDB Atlas (optional RAG)

### Method 1 Specific
- Google ADK
- LiteLLM
- Google Gemini models

### Method 2 Specific
- CrewAI
- OpenAI GPT-4o-mini

## 📊 Sample Data

Both methods use the same sample dataset:
- **5 Hospitals** across different regions
- **7 Days** of data (2024-10-20 to 2024-10-26)
- **40+ Metrics** per hospital including:
  - Bed capacity and utilization
  - ICU and ventilator status
  - Staff availability
  - Patient activity
  - Supplies and equipment
  - Infectious disease cases

## 🔧 Configuration

### Environment Variables

**Method 1 (.env)**:
```env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=your_mongodb_uri (optional)
```

**Method 2 (.env)**:
```env
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=your_mongodb_uri (optional)
```

## 📖 Documentation

- [Method 1 README](method%201/README.md) - Detailed Google ADK documentation
- [Method 2 README](method%202/README.md) - Detailed CrewAI documentation
- [Method 2 SETUP](method%202/SETUP.md) - Step-by-step setup guide

## 💬 Example Queries

Try these queries with either implementation:

### Conversational
```
"Hello"
"My name is John"
"What is my name?"
```

### Data Queries
```
"How many hospitals are there?"
"List all hospitals"
"Show me beds at City General Hospital"
"What's the ICU capacity?"
```

### Analytics
```
"Compare City General Hospital and Regional Medical Center"
"Show system-wide statistics"
"Analyze capacity trends"
```

### Distance & Location
```
"Calculate distance between City General Hospital and Metropolitan Hospital"
"Show all hospital distances"
"Find nearest hospital to District Hospital"
```

## 🏗️ Architecture Diagrams

### Method 1: Google ADK Architecture
```
User → FastAPI → Google ADK Agent → Tools → Data/MongoDB
                      ↓
              Session Service
              (Preference Learning)
```

### Method 2: CrewAI Architecture
```
User → FastAPI → Session Manager → Query Router
                                        ↓
                                   CrewAI Crew
                                   ├── Data Analyst
                                   ├── Location Specialist
                                   ├── Clinical Advisor
                                   └── Orchestrator
                                        ↓
                                     Tools → Data/MongoDB
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License

## 🙏 Acknowledgments

- [Google ADK](https://github.com/google/adk)
- [CrewAI](https://www.crewai.com/)
- [OpenAI](https://openai.com/)
- [FastAPI](https://fastapi.tiangolo.com/)

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Note**: This is a demonstration system with sample data. For production use, integrate with real hospital data sources and implement appropriate security measures.
