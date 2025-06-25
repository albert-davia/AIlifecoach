# AI Life Coach - LangGraph Agent

An artificial intelligence agent for life coaching, built with LangGraph and LangChain.

## 🚀 Quick Setup

### 1. Activate the virtual environment
```bash
# Option 1: Use the helper script
./activate_env.sh

# Option 2: Manual activation
source venv/bin/activate
```

### 2. Verify installation
```bash
# Test Python imports
python -c "import agent; print('✅ All imports successful!')"

# Check LangGraph CLI
langgraph --help
```

## 🔧 Using LangGraph CLI

### Development server
```bash
# Start the development server
langgraph dev --config langgraph.json --port 8123 --no-browser

# Access the web interface
open http://localhost:8123/docs
```

### Other CLI commands
```bash
# Create a new project
langgraph new my-project --template new-langgraph-project-python

# Build a Docker image
langgraph build --config langgraph.json

# Generate a Dockerfile
langgraph dockerfile --config langgraph.json

# Deploy to production
langgraph up --config langgraph.json
```

## 📁 Project Structure

```
AIlifecoach/
├── venv/                    # Python virtual environment
├── agent.py                 # Main life coaching agent
├── requirements.txt         # Python dependencies
├── langgraph.json          # LangGraph CLI configuration
├── activate_env.sh         # Environment activation script
└── README.md               # This file
```

## 🐍 Python Usage

### Run the agent directly
```bash
# Make sure the virtual environment is activated
source venv/bin/activate

# Run the agent
python agent.py
```

### Import in Python
```python
import agent

# Access the compiled graph
graph = agent.graph

# Use the graph
result = graph.invoke({
    "messages": [],
    "tasks": []
})
```

## 🔑 Environment Variables

Create a `.env` file in the project root:
```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: LangGraph API Key (for production)
LANGGRAPH_API_KEY=your_langgraph_api_key_here
```

## 🌐 REST API

Once the server is started, the API is available at:
- **Interactive documentation**: http://localhost:8123/docs
- **OpenAPI specification**: http://localhost:8123/openapi.json
- **Main endpoints**:
  - `/assistants` - Assistant management
  - `/threads` - Conversation management
  - `/runs` - Task execution

## 🚀 Deployment Options

### 1. Local Development
```bash
langgraph dev --config langgraph.json
```

### 2. Docker Deployment
```bash
# Generate Dockerfile
langgraph dockerfile --config langgraph.json

# Build the image
langgraph build --config langgraph.json

# Run the container
docker run -p 8123:8123 your-app-name
```

### 3. Cloud Deployment
LangGraph CLI supports deployment on various cloud platforms. Check the LangGraph documentation for specific instructions.

## 🛠️ Troubleshooting

### Import errors
If you see import errors:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install missing packages
pip install python-dotenv langgraph-cli[inmem]
```

### Virtual environment issues
```bash
# Recreate the virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### LangGraph CLI not found
```bash
# Reinstall LangGraph CLI
pip install --upgrade langgraph-cli[inmem]
```

## 📚 Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph CLI Guide](https://langchain-ai.github.io/langgraph/how-tos/cli/)
- [LangChain Documentation](https://python.langchain.com/)

## 🎯 Next Steps

1. Configure your `.env` file with API keys
2. Test the agent with `python agent.py`
3. Start the development server with `langgraph dev --config langgraph.json`
4. Customize the agent logic in `agent.py`
5. Deploy to production when ready

## ✅ Current Status

- ✅ Virtual environment configured
- ✅ LangGraph CLI installed and functional
- ✅ Development server operational
- ✅ REST API accessible
- ✅ Interactive documentation available