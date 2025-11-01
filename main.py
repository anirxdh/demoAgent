
import os
from dotenv import load_dotenv
from agent import AIAgent
import sys


def print_banner():
    """Print welcome banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                      🤖 AI AGENT DEMO - OpenAI SDK 🤖                     ║
║                                                                           ║
║  This agent can use tools to help answer your questions:                 ║
║    🌤️  Get Weather - Check weather in any city                           ║
║    📍 Get Location - Detect your current location                        ║
║    🕐 Get Time - Check time in any timezone                              ║
║    🔢 Calculate - Perform math calculations                              ║
║                                                                           ║
║  Watch as the agent thinks, plans, and uses tools to answer!             ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point for the AI agent demo."""
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required API keys are set
    if not os.getenv("OPENAI_API_KEY"):
        print("\033[91m❌ ERROR: OPENAI_API_KEY not found in .env file\033[0m")
        print("Please create a .env file with your OpenAI API key.")
        print("You can copy .env.example and fill in your API keys.")
        sys.exit(1)
    
    # Print welcome banner
    print_banner()
    
    # Initialize the agent
    try:
        agent = AIAgent()
        print("\033[92m✅ Agent initialized successfully!\033[0m")
        print(f"\033[92m   Using model: {agent.model}\033[0m\n")
    except Exception as e:
        print(f"\033[91m❌ ERROR: Failed to initialize agent: {e}\033[0m")
        sys.exit(1)
    
    # Main interaction loop
    print("\033[96m" + "="*80 + "\033[0m")
    print("\033[96mReady! Type your question below (Ctrl+C to exit)\033[0m")
    print("\033[96m" + "="*80 + "\033[0m\n")
    
    try:
        while True:
            # Get user input
            try:
                user_input = input("\033[1m👤 YOU: \033[0m").strip()
            except EOFError:
                print("\n\nGoodbye! 👋")
                break
            
            if not user_input:
                continue
            
            # Process user input with the agent
            try:
                agent.run(user_input)
            except Exception as e:
                print(f"\033[91m❌ ERROR: {e}\033[0m\n")
                continue
    
    except KeyboardInterrupt:
        print("\n\n\033[96mGoodbye! 👋\033[0m")
        sys.exit(0)


if __name__ == "__main__":
    main()


