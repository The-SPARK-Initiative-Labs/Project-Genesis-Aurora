# main_agent.py (v3.0 - Class-Based)
#
# This is the final, architecturally improved main entry point for the agent.
# It uses the new Aurora class to encapsulate all complexity, resulting in a
# clean, readable, and professional script.

from aura_engine.aurora import Aurora
import sys

def main():
    """
    Initializes and runs the Aurora agent.
    """
    aurora_agent = None
    try:
        # 1. Create an instance of the Aurora agent.
        #    All initialization logic is handled inside the class.
        aurora_agent = Aurora()
        
        # 2. Start the interactive chat loop.
        aurora_agent.run_chat_loop()

    except ConnectionError as e:
        print(f"❌ Could not start Aurora: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    finally:
        # 3. Ensure a clean shutdown.
        if aurora_agent:
            aurora_agent.shutdown()

if __name__ == "__main__":
    main()
