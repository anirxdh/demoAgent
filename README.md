# 🤖 OpenAI AI Agent Demo

A demonstration of an AI agent built with OpenAI's SDK that can use multiple tools to answer questions. Watch as the agent thinks, plans, and executes tool calls in real-time!

## 🎯 Features

The agent has access to 4 powerful tools:

- **🌤️ Get Weather** - Fetch current weather for any city using OpenWeatherMap API
- **📍 Get Location** - Detect user's location via IP geolocation
- **🕐 Get Time** - Get current time in any timezone
- **🔢 Calculate** - Perform mathematical calculations

## 🚀 Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install openai requests python-dotenv
```

### 2. Configure API Keys

Copy the `.env.example` file to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add:
- **OPENAI_API_KEY**: Your OpenAI API key (get it from https://platform.openai.com/)
- **OPENWEATHER_API_KEY**: Already configured with demo key

### 3. Run the Agent

```bash
python main.py
```

## 💬 Example Queries

Try asking the agent:

- "What's the weather in London?"
- "What's the weather like where I am?"
- "What time is it in Tokyo?"
- "Calculate 25 * 4 + 100"
- "Where am I located?"
- "What's the weather in Paris and what time is it there?"

## 🧠 How It Works

The agent uses OpenAI's **function calling** feature to:

1. **Analyze** your question
2. **Plan** which tools to use
3. **Execute** tool calls with appropriate parameters
4. **Synthesize** results into a helpful response

You'll see detailed logging showing:
- 🤔 Agent's thinking process
- 🔧 Tool calls being made
- ✅ Results from each tool
- 🤖 Final response

## 📁 Project Structure

```
.
├── main.py          # Entry point with CLI interface
├── agent.py         # Core agent logic with OpenAI integration
├── tools.py         # Tool implementations and definitions
├── requirements.txt # Python dependencies
├── .env            # Your API keys (not committed)
├── .env.example    # Template for API keys
└── README.md       # This file
```

## 🎨 Terminal Output

The agent provides color-coded output:
- 💭 **Purple**: User input
- 🤔 **Cyan**: Agent thinking
- 🔧 **Yellow**: Tool calls
- ✅ **Green**: Tool results
- 🤖 **Blue**: Final responses
- ❌ **Red**: Errors

## 🔧 Models

The demo uses **GPT-4o** (latest and most capable model). Alternative models are commented out in `agent.py`:
- `gpt-4-turbo` - Previous generation
- `gpt-3.5-turbo` - Faster and cheaper
- `gpt-4` - Original GPT-4

## 📝 Commands

While chatting with the agent:
- `help` - Show example questions
- `reset` - Clear conversation history
- `exit` or `quit` - Exit the program
- `Ctrl+C` - Force quit

## 🔒 API Keys

- **OpenAI**: Required - Get from https://platform.openai.com/
- **OpenWeatherMap**: Already configured for demo purposes

## 🐛 Troubleshooting

**"OPENAI_API_KEY not found"**
- Make sure you created a `.env` file with your OpenAI API key

**Rate limits or quota errors**
- Check your OpenAI account has available credits
- The free tier has limited requests per minute

**Weather API errors**
- The demo includes a working OpenWeatherMap key
- If it expires, get a free key from https://openweathermap.org/api

## 📚 Learn More

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [OpenWeatherMap API](https://openweathermap.org/api)

## 🎓 Educational Purpose

This demo is designed to showcase:
- AI agent reasoning and planning
- Function calling / tool use
- Multi-step problem solving
- Real-world API integration
- Transparent agent behavior

Enjoy experimenting! 🚀


