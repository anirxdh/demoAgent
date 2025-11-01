# 📖 Usage Guide - AI Agent Demo

## Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Your OpenAI API Key

Edit the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key:

```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

The OpenWeatherMap API key is already configured.

### Step 3: Run the Agent

```bash
python main.py
```

## What You'll See

When you run the agent, you'll see a detailed breakdown of how it thinks and acts:

### Example Session

```
YOU: What's the weather in London and what time is it there?

================================================================================
💭 USER INPUT: What's the weather in London and what time is it there?
================================================================================

🤔 AGENT THINKING: Iteration 1: Analyzing the request and deciding next steps...

🤔 AGENT THINKING: I need to use 2 tool(s) to answer this question.

🔧 CALLING TOOL: get_weather
   Arguments: {
     "location": "London"
   }

✅ TOOL RESULT from get_weather:
{
  "location": "London",
  "country": "GB",
  "temperature": "12°C",
  "feels_like": "10°C",
  "conditions": "light rain",
  "humidity": "82%",
  "wind_speed": "5.1 m/s"
}

🔧 CALLING TOOL: get_time
   Arguments: {
     "timezone": "Europe/London"
   }

✅ TOOL RESULT from get_time:
{
  "timezone": "Europe/London",
  "current_time": "14:30:22",
  "current_date": "2025-10-28",
  "day_of_week": "Tuesday",
  "formatted": "Tuesday, October 28, 2025 at 02:30:22 PM GMT"
}

🤔 AGENT THINKING: Iteration 2: Analyzing the request and deciding next steps...

🤔 AGENT THINKING: I have all the information I need. Formulating final response...

🤖 AGENT RESPONSE:
In London, it's currently Tuesday, October 28, 2025 at 2:30 PM GMT. 
The weather is light rain with a temperature of 12°C (feels like 10°C), 
humidity at 82%, and wind speed of 5.1 m/s.
```

## Understanding the Output

### Color Coding

- **💭 Purple** - Your input/question
- **🤔 Cyan** - Agent's internal thinking process
- **🔧 Yellow** - Tool calls being executed
- **✅ Green** - Results from tool execution
- **🤖 Blue** - Final response from the agent
- **❌ Red** - Errors (if any)

### Agent's Process

1. **Receives Input**: Your question or command
2. **Analyzes**: Determines what information is needed
3. **Plans**: Decides which tools to use
4. **Executes**: Calls the appropriate tools with parameters
5. **Synthesizes**: Combines results into a coherent answer
6. **Responds**: Gives you the final answer

## Example Questions

### Weather Queries
```
What's the weather in Tokyo?
How's the weather in New York?
Is it raining in Paris?
```

### Location Queries
```
Where am I?
What's my location?
Where am I located right now?
```

### Time Queries
```
What time is it in Singapore?
What's the current time in America/New_York?
Tell me the time in Tokyo
```

### Calculations
```
Calculate 123 * 456
What is (100 + 50) * 2?
Calculate 1000 / 8 + 25
```

### Combined Queries (Multi-tool)
```
What's the weather where I am?
What's the weather in Sydney and what time is it there?
Where am I and what's the weather here?
Calculate 25 * 4 and tell me the weather in London
```

## Available Commands

While interacting with the agent:

- `help` - Show example questions and commands
- `reset` - Clear conversation history (fresh start)
- `exit` or `quit` - Exit the program
- `Ctrl+C` - Force quit

## Tool Details

### 1. get_weather(location)
**Purpose**: Fetch current weather data for any city

**API**: OpenWeatherMap

**Parameters**:
- `location` (string): City name (e.g., "London", "New York", "Tokyo")

**Returns**:
- Temperature (Celsius)
- Feels like temperature
- Weather conditions
- Humidity percentage
- Wind speed

### 2. get_location()
**Purpose**: Detect your location via IP address

**API**: ipapi.co (free, no key needed)

**Parameters**: None

**Returns**:
- City
- Region/State
- Country
- Coordinates (latitude/longitude)
- Timezone
- IP address

### 3. get_time(timezone)
**Purpose**: Get current time in any timezone

**Parameters**:
- `timezone` (string, optional): Timezone name (defaults to "UTC")
  - Examples: "UTC", "America/New_York", "Europe/London", "Asia/Tokyo"

**Returns**:
- Current time
- Current date
- Day of week
- Formatted datetime string

### 4. calculate(expression)
**Purpose**: Perform mathematical calculations

**Parameters**:
- `expression` (string): Math expression with basic operators

**Supported Operations**:
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Parentheses: `()`

**Examples**:
- `2 + 2`
- `(10 * 5) + 3`
- `100 / 4 - 10`

## Advanced Usage

### Multi-Step Reasoning

The agent can chain multiple tool calls:

```
YOU: What's the weather where I am?

The agent will:
1. Call get_location() to find your location
2. Extract the city name
3. Call get_weather(city) with that city
4. Provide a combined answer
```

### Conversation Context

The agent maintains conversation history:

```
YOU: What's the weather in Paris?
AGENT: [provides weather]

YOU: And what time is it there?
AGENT: [knows "there" refers to Paris, calls get_time]
```

Use the `reset` command to clear history if needed.

## Troubleshooting

### "OPENAI_API_KEY not found"
**Solution**: Make sure your `.env` file exists and contains your OpenAI API key

### "Failed to fetch weather data: 401"
**Solution**: The OpenWeatherMap API key may have expired. Get a free key from https://openweathermap.org/api

### "Maximum iterations reached"
**Solution**: The agent got stuck. Use `reset` to clear history and try again

### Rate Limit Errors
**Solution**: 
- Check your OpenAI account has available credits
- Wait a moment and try again
- Consider upgrading your OpenAI plan

### Import Errors
**Solution**: Make sure all dependencies are installed:
```bash
pip install openai requests python-dotenv
```

## Tips for Best Results

1. **Be Specific**: "Weather in London" is better than "weather"
2. **One Task at a Time**: While the agent can handle multi-step queries, start simple
3. **Use Full Timezone Names**: "America/New_York" instead of "EST"
4. **Reset When Confused**: If the agent seems confused, use `reset`
5. **Check Your Credits**: Make sure your OpenAI account has API credits

## Model Information

**Current Model**: GPT-4o
- Most capable model for function calling
- Best reasoning and planning abilities
- Recommended for this demo

**Alternative Models** (commented out in `agent.py`):
- `gpt-4-turbo`: Previous generation, still very capable
- `gpt-3.5-turbo`: Faster and cheaper, less capable reasoning
- `gpt-4`: Original GPT-4, more expensive

To change models, edit the `self.model` line in `agent.py`.

## API Costs

Typical costs per query (approximate):
- **Simple query** (1-2 tool calls): $0.01 - $0.02
- **Complex query** (3-4 tool calls): $0.02 - $0.05

Weather and location APIs are free tier (included).

## Next Steps

1. **Experiment**: Try different types of questions
2. **Observe**: Watch how the agent reasons and plans
3. **Extend**: Add your own tools in `tools.py`
4. **Customize**: Modify the system prompt in `agent.py`

Enjoy exploring AI agents! 🚀


