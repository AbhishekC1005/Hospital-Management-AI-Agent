# Healthcare Decision Support System (CrewAI Method)

A sophisticated healthcare management system built on CrewAI framework that enables intelligent multi-agent collaboration for comprehensive hospital resource management. This implementation features advanced session management and personalized interactions.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Latest-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Architecture

```plaintext
Healthcare Decision Support System (CrewAI)
├── Session Management Layer
│   ├── Context Manager
│   │   ├── User State Tracker
│   │   └── Preference Store
│   │
│   └── History Service
│       ├── Interaction Logger
│       └── Analytics Processor
│
├── Agent Network
│   ├── Coordinator Agent
│   │   ├── Task Distributor
│   │   └── Response Aggregator
│   │
│   ├── Specialist Agents
│   │   ├── Data Analysis Agent
│   │   ├── Resource Manager Agent
│   │   └── Decision Support Agent
│   │
│   └── Communication Bus
│       ├── Message Router
│       └── State Synchronizer
│
└── Infrastructure Layer
    ├── FastAPI Server
    ├── Database Connectors
    └── Monitoring Service

```

## Key Features

- **🤖 Intelligent Multi-Agent Collaboration**
  - CrewAI-powered agent orchestration
  - Role-specific agents for specialized tasks
  - Dynamic task delegation and coordination

- **🧠 Advanced Session Management**
  - Persistent memory across conversations
  - User preference tracking
  - Context-aware responses
  - Personalized interaction history

- **📊 Comprehensive Hospital Analytics**
  - Real-time monitoring of 40+ healthcare metrics
  - Resource utilization tracking
  - Capacity management
  - Staff allocation optimization

- **🗺️ Spatial Intelligence**
  - Inter-hospital distance calculations
  - Geographic resource distribution
  - Coverage optimization
  - Network analysis

- **🤝 Collaborative Decision Making**
  - Multi-agent consensus building
  - Cross-validated recommendations
  - Dynamic resource allocation
  - Real-time adaptation

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
