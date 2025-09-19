"""
Utility functions and helpers
"""

import os
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self):
        self.log_file = os.getenv('GAME_LOG_FILE', '/app/shared/game.log')
        self.ensure_log_dir()
    
    def ensure_log_dir(self):
        """Ensure log directory exists"""
        log_path = Path(self.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log(self, message):
        """Log message to file and optionally to console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Write to file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception as e:
            print(f"Logging error: {e}")
        
        # Also print debug info (optional)
        if os.getenv('DEBUG', '').lower() == 'true':
            print(f"DEBUG: {log_entry}")

def format_text(text, width=70):
    """Format text to specified width"""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line + " " + word) <= width:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return '\n'.join(lines)