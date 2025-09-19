"""
Command parsing and handling
"""

class CommandParser:
    def __init__(self):
        # Command mappings with abbreviations
        self.commands = {
            'look': ['look', 'l'],
            'move': ['move', 'm', 'go'],
            'grab': ['grab', 'g', 'take', 'get'],
            'inventory': ['inventory', 'i', 'inv'],
            'fight': ['fight', 'f', 'attack', 'battle']
        }
        
        # Direction mappings
        self.directions = {
            'north': ['north', 'n'],
            'south': ['south', 's'],
            'east': ['east', 'e'],
            'west': ['west', 'w']
        }
    
    def parse(self, user_input):
        """Parse user input into command, subcommand, and arguments"""
        if not user_input:
            return None, None, None
            
        parts = user_input.lower().strip().split()
        if not parts:
            return None, None, None
            
        # Find command
        command = self._find_command(parts[0])
        if not command:
            return None, None, None
            
        # Parse subcommand and arguments
        subcommand = None
        args = None
        
        if len(parts) > 1:
            # Check if second part is a direction
            direction = self._find_direction(parts[1])
            if direction and command in ['look', 'move']:
                subcommand = direction
            else:
                # Treat as argument
                args = ' '.join(parts[1:])
        
        return command, subcommand, args
    
    def _find_command(self, input_cmd):
        """Find command from input (including abbreviations)"""
        for cmd, aliases in self.commands.items():
            if input_cmd in aliases:
                return cmd
        return None
    
    def _find_direction(self, input_dir):
        """Find direction from input (including abbreviations)"""
        for direction, aliases in self.directions.items():
            if input_dir in aliases:
                return direction
        return None