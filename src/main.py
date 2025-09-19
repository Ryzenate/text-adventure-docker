#!/usr/bin/env python3
"""
Main entry point for the Docker Adventure Game
"""

import sys
import signal
import time
from pathlib import Path

from game_engine import GameEngine
from utils import Logger

def signal_handler(sig, frame):
    """Handle graceful shutdown"""
    print("\n\nGame shutting down gracefully...")
    sys.exit(0)

def main():
    """Main game loop"""
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize logger
    logger = Logger()
    logger.log("=== Docker Adventure Game Starting ===")
    logger.log("Game initialized successfully")
    
    try:
        # Initialize game engine
        game = GameEngine(logger)
        
        # Welcome message
        print("\n" + "="*50)
        print("    🏰 WELCOME TO DOCKER ADVENTURE GAME 🏰")
        print("="*50)
        print("Type 'help' for commands or 'quit' to exit")
        print("Commands support abbreviations (e.g., 'm n' for 'move north')")
        print("-"*50)
        
        # Main game loop
        while True:
            try:
                # Get user input
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                    
                # Log user input
                logger.log(f"User input: {user_input}")
                
                # Process command
                result = game.process_command(user_input)
                
                # Handle special commands
                if result == "QUIT":
                    print("\nThanks for playing! Goodbye! 👋")
                    logger.log("Game ended by user")
                    break
                elif result == "HELP":
                    game.show_help()
                else:
                    # Print command result
                    if result:
                        print(result)
                        logger.log(f"Command result: {result}")
                        
            except KeyboardInterrupt:
                print("\n\nUse 'quit' to exit gracefully.")
                continue
            except Exception as e:
                error_msg = f"Error processing command: {str(e)}"
                print(f"❌ {error_msg}")
                logger.log(f"ERROR: {error_msg}")
                
    except Exception as e:
        error_msg = f"Fatal error: {str(e)}"
        print(f"💥 {error_msg}")
        logger.log(f"FATAL: {error_msg}")
        return 1
    
    logger.log("=== Docker Adventure Game Ended ===")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)