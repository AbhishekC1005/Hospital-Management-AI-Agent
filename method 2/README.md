# Healthcare Decision Support System (CrewAI Implementation)

An advanced healthcare decision support system built on the CrewAI framework, implementing a multi-agent collaborative approach with specialized agents for different aspects of hospital management. This implementation features persistent session management and agent-specific expertise distribution.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Latest-orange)
![LangChain](https://img.shields.io/badge/LangChain-OpenAI-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-brightgreen)

## System Architecture

![CrewAI Function Architecture](images/crewai_diagram.png)

![Google ADK Function Architecture](images/GoogleADK_diagram.png)

```plaintext
Healthcare Decision Support System (CrewAI)
├── Web Layer (FastAPI)
│   ├── API Endpoints
│   │   ├── /query - Main interaction point
│   │   └── /static - Static file serving
│   └── CORS Configuration
│
├── Session Management
│   ├── Session Manager
│   │   ├── Context Tracking
│   │   └── State Persistence
│   │
│   └── Environment Variables
│       └── OpenAI Configuration
│
├── Agent Network
│   ├── Specialized Agents
│   │   ├── Hospital Analysis Agent
│   │   │   ├── Capacity Analysis
│   │   │   └── Trend Analysis
│   │   │
│   │   ├── Resource Management Agent
│   │   │   ├── Staff Allocation
│   │   │   └── Equipment Distribution
│   │   │
│   │   └── Decision Support Agent
│   │       ├── Recommendation Generation
│   │       └── Strategy Optimization
│   │
│   └── Tool Integration
│       ├── Hospital Tools
│       │   ├── Basic Analytics
│       │   │   ├── get_hospital_count_tool()
│       │   │   ├── get_hospital_names_tool()
│       │   │   └── get_hospital_details_tool()
│       │   │
│       │   ├── Advanced Analytics
│       │   │   ├── analyze_capacity_trends_tool()
│       │   │   ├── compare_hospitals_tool()
│       │   │   └── get_system_statistics_tool()
│       │   │
│       │   └── Spatial Analysis
│       │       ├── calculate_distance_tool()
│       │       ├── get_all_distances_tool()
│       │       └── find_nearest_hospital_tool()
│       │
│       └── RAG Integration
│           └── rag_function_tool()
│
├── Data Layer
│   ├── Hospital Data
│   │   └── hospital_trends.csv
│   │
│   └── RAG System
│       └── Vector Store
│
└── Static Content
    ├── HTML Interface
    ├── JavaScript
    └── CSS Styling
```

## Key Features

- **Intelligent Multi-Agent Collaboration**
  - CrewAI-powered agent orchestration
  - Role-specific agents for specialized tasks
  - Dynamic task delegation and coordination

- **Advanced Session Management**
  - Persistent memory across conversations
  - User preference tracking
  - Context-aware responses
  - Persistent interaction history

- **Comprehensive Hospital Analytics**
  - Real-time monitoring of 40+ healthcare metrics
  - Resource utilization tracking
  - Capacity management
  - Staff allocation optimization

- **Spatial Intelligence**
  - Inter-hospital distance calculations
  - Geographic resource distribution
  - Coverage optimization
  - Network analysis

- **Collaborative Decision Making**
  - Multi-agent consensus building
  - Cross-validated recommendations
  - Dynamic resource allocation

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API Key (for GPT-4)
- FastAPI (for web interface)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AbhishekC1005/Hospital-Management-AI-Agent.git
   cd Hospital-Management-AI-Agent/method2
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   Create a `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   PORT=8001
   HOST=0.0.0.0
   ```

5. **Launch the Application**
   ```bash
   python main.py
   ```
   Open http://localhost:8001 in your browser

## 💡 Usage Examples

```python
# Personalized Interaction
"Hello, my name is John"
"What was my previous request about hospital capacity?"

# Hospital Analytics
"How many hospitals are currently in the system?"
"Show me the ICU bed availability at City General Hospital"
"What's the current staff distribution across all facilities?"

# Resource Management
"Calculate the distance between Memorial and Central hospitals"
"Optimize staff allocation for the weekend shift"
"Recommend ventilator redistribution based on current needs"
```

## 🏗️ System Architecture

```
Healthcare Management System
├── Session Manager
│   ├── User context tracking
│   └── Preference management
├── Agent Crew
│   ├── Data Analysis Agent
│   ├── Resource Management Agent
│   └── Decision Support Agent
└── Integration Layer
    ├── FastAPI Interface
    └── Database Connectors
```

## 🛠️ Tech Stack

- **Core Framework**: CrewAI for agent orchestration
- **Language Model**: OpenAI GPT-4
- **Web Framework**: FastAPI
- **Python Version**: 3.10+
- **Database**: SQLite for session management

## 📚 Documentation

For detailed documentation, please refer to:
- [Setup Guide](SETUP.md)
- [API Documentation](docs/API.md)
- [CrewAI Integration](docs/CREW.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CrewAI Team for the collaborative AI framework
- OpenAI for the GPT-4 language model
- FastAPI Team for the excellent web framework
