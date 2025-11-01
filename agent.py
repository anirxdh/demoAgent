"""
AI Agent implementation using OpenAI's function calling capabilities.
The agent can reason, plan, and use tools to answer user queries.
"""

import os
from openai import OpenAI
from tools import TOOLS, AVAILABLE_FUNCTIONS
import json


class AIAgent:
    def __init__(self):
        """Initialize the AI agent with OpenAI client and configuration."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        
        # Model selection - GPT-4o is the latest and best for function calling
        self.model = "gpt-4o"
        
        # Alternative models (commented out):
        # self.model = "gpt-4-turbo"  # Previous generation, still very capable
        # self.model = "gpt-4-turbo-preview"  # Preview version with extended context
        # self.model = "gpt-3.5-turbo"  # Faster and cheaper, but less capable
        # self.model = "gpt-4"  # Original GPT-4, more expensive
        
        self.messages = []
        self.tools = TOOLS
        
        # System prompt to guide the agent's behavior
        self.system_prompt = """You are a helpful AI assistant with access to several tools.
When a user asks a question, think carefully about what information you need and which tools to use.
Be conversational and explain your reasoning. If you need to use multiple tools, do so step by step.
Always provide helpful, accurate, and friendly responses."""
        
        self.messages.append({"role": "system", "content": self.system_prompt})
    
    def print_thinking(self, message: str, color: str = "\033[96m"):
        """Print agent's thinking process in color."""
        reset = "\033[0m"
        print(f"{color}🤔 AGENT THINKING: {message}{reset}\n")
    
    def print_debug(self, title: str, data: any, color: str = "\033[90m"):
        """Print detailed debug information."""
        reset = "\033[0m"
        print(f"{color}{'─'*80}{reset}")
        print(f"{color}🔍 DEBUG: {title}{reset}")
        print(f"{color}{'─'*80}{reset}")
        if isinstance(data, dict) or isinstance(data, list):
            print(f"{color}{json.dumps(data, indent=2, default=str)}{reset}")
        else:
            print(f"{color}{data}{reset}")
        print(f"{color}{'─'*80}{reset}\n")
    
    def _normalize_message(self, msg):
        """Convert ChatCompletionMessage objects to dict format."""
        if isinstance(msg, dict):
            return msg
        else:
            # Handle ChatCompletionMessage or other object types
            normalized = {
                "role": getattr(msg, "role", "unknown")
            }
            content = getattr(msg, "content", "")
            normalized["content"] = content if content is not None else ""
            
            tool_calls = getattr(msg, "tool_calls", None)
            if tool_calls:
                normalized["tool_calls"] = [
                    {
                        "id": tc.id if hasattr(tc, 'id') else getattr(tc, 'id', ''),
                        "type": getattr(tc, "type", "function"),
                        "function": {
                            "name": tc.function.name if hasattr(tc, 'function') else getattr(tc, 'name', 'unknown'),
                            "arguments": tc.function.arguments if hasattr(tc, 'function') else getattr(tc, 'arguments', '{}')
                        }
                    }
                    for tc in tool_calls
                ]
            
            # Handle tool role messages
            if hasattr(msg, 'name'):
                normalized["name"] = getattr(msg, "name", "")
            if hasattr(msg, 'tool_call_id'):
                normalized["tool_call_id"] = getattr(msg, "tool_call_id", "")
            
            return normalized
    
    def print_message_history(self):
        """Print the current conversation history being sent to OpenAI."""
        print(f"\033[95m{'='*80}\033[0m")
        print(f"\033[95m📜 CONVERSATION HISTORY (being sent to OpenAI):\033[0m")
        print(f"\033[95m{'='*80}\033[0m")
        for i, msg in enumerate(self.messages, 1):
            try:
                # Normalize message to dict format
                msg_dict = self._normalize_message(msg)
                
                role = msg_dict.get("role", "unknown")
                content = msg_dict.get("content", "")
                tool_calls = msg_dict.get("tool_calls", None)
                
                if role == "system":
                    print(f"\n\033[93m[{i}] SYSTEM PROMPT:\033[0m")
                    print(f"   {content[:200]}..." if len(content) > 200 else f"   {content}")
                elif role == "user":
                    print(f"\n\033[94m[{i}] USER MESSAGE:\033[0m")
                    print(f"   {content}")
                elif role == "assistant":
                    print(f"\n\033[96m[{i}] ASSISTANT MESSAGE:\033[0m")
                    if content:
                        print(f"   {content[:200]}..." if len(content) > 200 else f"   {content}")
                    if tool_calls:
                        print(f"   🔧 Tool Calls: {len(tool_calls)}")
                        for tc in tool_calls:
                            if isinstance(tc, dict):
                                func_name = tc.get('function', {}).get('name', 'unknown')
                                func_args = tc.get('function', {}).get('arguments', '{}')
                            else:
                                func_name = getattr(tc, 'function', {}).name if hasattr(tc, 'function') else 'unknown'
                                func_args = getattr(tc, 'function', {}).arguments if hasattr(tc, 'function') else '{}'
                            print(f"      • {func_name}({func_args[:50]}...)")
                elif role == "tool":
                    tool_name = msg_dict.get('name', 'unknown')
                    print(f"\n\033[92m[{i}] TOOL RESULT ({tool_name}):\033[0m")
                    try:
                        result = json.loads(content) if content else {}
                        result_str = json.dumps(result, indent=2)
                        print(f"   {result_str[:300]}..." if len(result_str) > 300 else f"   {result_str}")
                    except:
                        print(f"   {content[:300]}...")
            except Exception as e:
                print(f"\n\033[91m[{i}] ERROR displaying message: {e}\033[0m")
                print(f"\033[91m   Message type: {type(msg)}\033[0m")
        print(f"\033[95m{'='*80}\033[0m\n")
    
    def print_api_request(self, model: str, messages: list, tools: list):
        """Print the API request being sent to OpenAI."""
        print(f"\033[95m{'='*80}\033[0m")
        print(f"\033[95m📤 API REQUEST TO OPENAI:\033[0m")
        print(f"\033[95m{'='*80}\033[0m")
        print(f"\033[95mModel: {model}\033[0m")
        print(f"\033[95mMessages: {len(messages)} message(s)\033[0m")
        print(f"\033[95mAvailable Tools: {len(tools)} tool(s)\033[0m")
        print(f"\033[95m   • {', '.join([t['function']['name'] for t in tools])}\033[0m")
        print(f"\033[95m{'='*80}\033[0m\n")
    
    def print_api_response(self, response):
        """Print detailed API response information."""
        print(f"\033[95m{'='*80}\033[0m")
        print(f"\033[95m📥 API RESPONSE FROM OPENAI:\033[0m")
        print(f"\033[95m{'='*80}\033[0m")
        
        # Response metadata
        print(f"\033[95mResponse ID: {response.id}\033[0m")
        print(f"\033[95mModel: {response.model}\033[0m")
        print(f"\033[95mCreated: {response.created}\033[0m")
        
        # Token usage
        if response.usage:
            print(f"\033[95m\nToken Usage:\033[0m")
            print(f"\033[95m   Prompt tokens: {response.usage.prompt_tokens}\033[0m")
            print(f"\033[95m   Completion tokens: {response.usage.completion_tokens}\033[0m")
            print(f"\033[95m   Total tokens: {response.usage.total_tokens}\033[0m")
        
        # Message details
        message = response.choices[0].message
        print(f"\033[95m\nMessage Role: {message.role}\033[0m")
        
        if message.content:
            print(f"\033[95m\nContent:\033[0m")
            print(f"\033[95m{message.content[:500]}...\033[0m" if len(message.content) > 500 else f"\033[95m{message.content}\033[0m")
        
        if message.tool_calls:
            print(f"\033[95m\nTool Calls: {len(message.tool_calls)}\033[0m")
            for i, tc in enumerate(message.tool_calls, 1):
                print(f"\033[95m   [{i}] Tool Call ID: {tc.id}\033[0m")
                print(f"\033[95m       Function: {tc.function.name}\033[0m")
                print(f"\033[95m       Arguments: {tc.function.arguments}\033[0m")
        
        print(f"\033[95m{'='*80}\033[0m\n")
    
    def print_decision_tree(self, response_message, available_tools):
        """Print the decision-making process."""
        print(f"\033[95m{'='*80}\033[0m")
        print(f"\033[95m🧠 DECISION ANALYSIS:\033[0m")
        print(f"\033[95m{'='*80}\033[0m")
        
        if response_message.tool_calls:
            print(f"\033[95mDecision: USE TOOLS ({len(response_message.tool_calls)} tool call(s))\033[0m")
            print(f"\033[95m\nReasoning:\033[0m")
            print(f"\033[95m   The agent determined that tool(s) are needed to answer the question.\033[0m")
            print(f"\033[95m   Selected tools:\033[0m")
            for tc in response_message.tool_calls:
                tool_name = tc.function.name
                tool_args = tc.function.arguments
                print(f"\033[95m   ✓ {tool_name}\033[0m")
                print(f"\033[95m     Why: Matches user query requirement\033[0m")
                print(f"\033[95m     Args: {tool_args[:100]}...\033[0m" if len(tool_args) > 100 else f"\033[95m     Args: {tool_args}\033[0m")
                
                # Check which tools were NOT selected
                not_selected = [t['function']['name'] for t in available_tools if t['function']['name'] != tool_name]
                if not_selected:
                    print(f"\033[95m     Not selected: {', '.join(not_selected)}\033[0m")
        else:
            print(f"\033[95mDecision: DIRECT RESPONSE (no tools needed)\033[0m")
            print(f"\033[95m\nReasoning:\033[0m")
            print(f"\033[95m   The agent determined it has enough information to answer directly.\033[0m")
            print(f"\033[95m   Available tools: {', '.join([t['function']['name'] for t in available_tools])}\033[0m")
            print(f"\033[95m   Why not use tools: Question doesn't require real-time data or calculations\033[0m")
        
        print(f"\033[95m{'='*80}\033[0m\n")
    
    def print_tool_call(self, function_name: str, arguments: dict):
        """Print tool call details."""
        print(f"\033[93m🔧 CALLING TOOL: {function_name}\033[0m")
        print(f"\033[93m   Arguments: {json.dumps(arguments, indent=2)}\033[0m\n")
    
    def print_tool_result(self, function_name: str, result: str):
        """Print tool execution result."""
        print(f"\033[92m✅ TOOL RESULT from {function_name}:\033[0m")
        try:
            # Try to pretty print JSON
            result_dict = json.loads(result)
            print(f"\033[92m{json.dumps(result_dict, indent=2)}\033[0m\n")
        except:
            print(f"\033[92m{result}\033[0m\n")
    
    def print_response(self, content: str):
        """Print final agent response."""
        print(f"\033[94m🤖 AGENT RESPONSE:\033[0m")
        print(f"\033[94m{content}\033[0m\n")
    
    def run(self, user_input: str) -> str:
        """
        Process user input and generate response using tools if needed.
        
        Args:
            user_input: The user's question or request
        
        Returns:
            The agent's final response
        """
        # Add user message to conversation
        self.messages.append({"role": "user", "content": user_input})
        
        print(f"\n\033[95m{'='*80}\033[0m")
        print(f"\033[95m💭 USER INPUT: {user_input}\033[0m")
        print(f"\033[95m{'='*80}\033[0m\n")
        
        # Show conversation history being sent to OpenAI
        self.print_message_history()
        
        iteration = 0
        max_iterations = 10  # Prevent infinite loops
        
        while iteration < max_iterations:
            iteration += 1
            
            print(f"\n\033[96m{'█'*80}\033[0m")
            print(f"\033[96m🔄 ITERATION {iteration}\033[0m")
            print(f"\033[96m{'█'*80}\033[0m\n")
            
            self.print_thinking(f"Iteration {iteration}: Analyzing the request and deciding next steps...")
            
            # Show API request details
            self.print_api_request(self.model, self.messages, self.tools)
            
            # Call OpenAI API with function calling capability
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto"  # Let the model decide when to use tools
            )
            
            # Show API response details
            self.print_api_response(response)
            
            response_message = response.choices[0].message
            
            # Show decision analysis
            self.print_decision_tree(response_message, self.tools)
            
            # Check if the model wants to call functions
            if response_message.tool_calls:
                self.print_thinking(f"I need to use {len(response_message.tool_calls)} tool(s) to answer this question.")
                
                # Convert ChatCompletionMessage to dict format before adding to conversation
                assistant_msg = {
                    "role": response_message.role,
                    "content": response_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in response_message.tool_calls
                    ]
                }
                self.messages.append(assistant_msg)
                
                # Execute each tool call
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"\n\033[93m{'─'*80}\033[0m")
                    print(f"\033[93m🔧 EXECUTING TOOL: {function_name}\033[0m")
                    print(f"\033[93m{'─'*80}\033[0m")
                    self.print_tool_call(function_name, function_args)
                    
                    # Execute the function
                    if function_name in AVAILABLE_FUNCTIONS:
                        function_to_call = AVAILABLE_FUNCTIONS[function_name]
                        print(f"\033[93m   ⚙️  Executing function...\033[0m\n")
                        function_response = function_to_call(**function_args)
                        
                        self.print_tool_result(function_name, function_response)
                        
                        # Add function response to conversation
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": function_response
                        })
                        
                        print(f"\033[93m   ✅ Tool result added to conversation history\033[0m\n")
                    else:
                        error_msg = f"Function {function_name} not found"
                        print(f"\033[91m❌ ERROR: {error_msg}\033[0m\n")
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps({"error": error_msg})
                        })
                
                # Show updated conversation history
                print(f"\n\033[95m📜 UPDATED CONVERSATION HISTORY (after tool execution):\033[0m")
                self.print_message_history()
                
                # Continue the loop to get the final response
                continue
            
            else:
                # No more tool calls - we have the final response
                final_content = response_message.content
                self.print_thinking("I have all the information I need. Formulating final response...")
                print(f"\n\033[95m{'='*80}\033[0m")
                print(f"\033[95m✅ FINAL DECISION: Ready to respond (no more tools needed)\033[0m")
                print(f"\033[95m{'='*80}\033[0m\n")
                self.print_response(final_content)
                
                # Add assistant's response to conversation history
                self.messages.append({"role": "assistant", "content": final_content})
                
                return final_content
        
        # If we hit max iterations
        error_msg = "Maximum iterations reached. The agent might be stuck in a loop."
        print(f"\033[91m❌ ERROR: {error_msg}\033[0m\n")
        return error_msg
    
    def reset(self):
        """Reset the conversation history."""
        self.messages = [{"role": "system", "content": self.system_prompt}]
        print("\n\033[93m🔄 Conversation history cleared.\033[0m\n")


