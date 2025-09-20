"""
Core game engine for the adventure game
"""

from player import Player
from world import World
from commands import CommandParser
from ollama_client import OllamaClient
from items import ItemManager

class GameEngine:
    def __init__(self, logger):
        self.logger = logger
        self.player = Player()
        self.world = World()
        self.command_parser = CommandParser()
        self.ollama_client = OllamaClient(logger)
        self.item_manager = ItemManager()
        
        # Place player in starting room
        self.player.current_room = "forest_entrance"
        
        # Show initial room description
        self._show_room_description()
        
    def process_command(self, user_input):
        """Process user command and return result"""
        if user_input.lower() in ['quit', 'exit', 'q']:
            return "QUIT"
        elif user_input.lower() in ['help', 'h', '?']:
            return "HELP"
            
        # Parse command
        command, subcommand, args = self.command_parser.parse(user_input)
        
        if not command:
            return "❓ I don't understand that command. Type 'help' for available commands."
            
        # Execute command
        return self._execute_command(command, subcommand, args)
    
    def _execute_command(self, command, subcommand, args):
        """Execute parsed command"""
        try:
            if command == "look":
                return self._handle_look(subcommand)
            elif command == "move":
                return self._handle_move(subcommand)
            elif command == "grab":
                return self._handle_grab(args)
            elif command == "inventory":
                return self._handle_inventory()
            elif command == "use":
                return self._handle_use(args)
            elif command == "examine":
                return self._handle_examine(args)
            elif command == "fight":
                return self._handle_fight(args)
            else:
                return f"❓ Unknown command: {command}"
                
        except Exception as e:
            self.logger.log(f"Command execution error: {str(e)}")
            return f"❌ Error executing command: {str(e)}"
    
    def _handle_look(self, direction=None):
        """Handle look command"""
        current_room = self.world.get_room(self.player.current_room)
        
        if not direction:
            # Look around current room
            result = f"🏠 {current_room['name']}\n"
            result += f"📝 {current_room['description']}\n"
            
            # Show items
            if current_room.get('items'):
                result += f"📦 Items here: {', '.join(current_room['items'])}\n"
                
            # Show exits
            exits = [direction for direction in ['north', 'south', 'east', 'west'] 
                    if current_room.get('exits', {}).get(direction)]
            if exits:
                result += f"🚪 Exits: {', '.join(exits)}"
            else:
                result += "🚪 No obvious exits"
                
            return result
        else:
            # Look in specific direction
            exit_room = current_room.get('exits', {}).get(direction)
            if exit_room:
                target_room = self.world.get_room(exit_room)
                return f"👀 To the {direction}: {target_room['name']} - {target_room.get('short_desc', 'A mysterious area')}"
            else:
                return f"👀 You see nothing interesting to the {direction}."
    
    def _handle_move(self, direction):
        """Handle move command"""
        if not direction:
            return "🚶 Move where? Specify a direction (north, south, east, west)"
            
        current_room = self.world.get_room(self.player.current_room)
        exit_room = current_room.get('exits', {}).get(direction)
        
        if not exit_room:
            return f"🚫 You can't go {direction} from here."
            
        # Move player
        self.player.current_room = exit_room
        self.logger.log(f"Player moved {direction} to {exit_room}")
        
        # Show new room description
        return self._show_room_description()
    
    def _handle_grab(self, item_name):
        """Handle grab command"""
        if not item_name:
            return "🤏 Grab what? Specify an item name."
            
        current_room = self.world.get_room(self.player.current_room)
        room_items = current_room.get('items', [])
        
        # Find item (case insensitive)
        item_to_grab = None
        for item in room_items:
            if item.lower() == item_name.lower():
                item_to_grab = item
                break
                
        if not item_to_grab:
            return f"📦 There's no '{item_name}' here to grab."
            
        # Add to inventory and remove from room
        self.player.inventory.append(item_to_grab)
        room_items.remove(item_to_grab)
        
        self.logger.log(f"Player grabbed: {item_to_grab}")
        return f"✅ You grabbed the {item_to_grab}!"
    
    def _handle_inventory(self):
        """Handle inventory command"""
        if not self.player.inventory:
            return "🎒 Your inventory is empty."
            
        result = "🎒 Inventory:\n"
        for item in self.player.inventory:
            item_obj = self.item_manager.get_item(item)
            if item_obj:
                result += f"  • {item} - {item_obj.description[:50]}...\n"
            else:
                result += f"  • {item}\n"
        
        return result.rstrip()
    
    def _handle_use(self, item_name):
        """Handle use command"""
        if not item_name:
            return "🔧 Use what? Specify an item name."
            
        if not self.player.has_item(item_name):
            return f"❌ You don't have '{item_name}' in your inventory."
            
        item = self.item_manager.get_item(item_name)
        if not item:
            return f"❓ Unknown item: {item_name}"
            
        if not item.usable:
            return f"🚫 You can't use the {item_name}."
            
        # Use the item
        result = item.use(self.player, self)
        
        # Remove consumable items
        if item.consumable:
            self.player.remove_item(item_name)
            result += f" The {item_name} is consumed."
            
        self.logger.log(f"Player used: {item_name}")
        return result
    
    def _handle_examine(self, item_name):
        """Handle examine command"""
        if not item_name:
            return "🔍 Examine what? Specify an item name."
            
        # Check if item is in inventory
        if self.player.has_item(item_name):
            description = self.item_manager.get_item_description(item_name)
            if description:
                return f"🔍 {description}"
            else:
                return f"❓ You can't find details about '{item_name}'."
        
        # Check if item is in current room
        current_room = self.world.get_room(self.player.current_room)
        room_items = current_room.get('items', [])
        
        for item in room_items:
            if item.lower() == item_name.lower():
                description = self.item_manager.get_item_description(item_name)
                if description:
                    return f"🔍 {description}"
                else:
                    return f"❓ You can't find details about '{item_name}'."
        
        return f"❌ There's no '{item_name}' here or in your inventory."
    
    def _handle_fight(self, target):
        """Handle fight command with AI assistance"""
        if not target:
            return "⚔️ Fight what? You need to specify a target."
            
        current_room = self.world.get_room(self.player.current_room)
        
        # Check if there are enemies in the room
        enemies = current_room.get('enemies', [])
        if not enemies:
            return "⚔️ There's nothing to fight here."
            
        # Check for weapons in inventory
        weapons = []
        for item_name in self.player.inventory:
            item = self.item_manager.get_item(item_name)
            if item and hasattr(item, 'damage'):
                weapons.append(item)
        
        weapon_text = ""
        if weapons:
            weapon_text = f" You are wielding: {', '.join([w.name for w in weapons])}"
        
        # Use AI to generate fight scenario
        fight_prompt = f"""
        The player is fighting a {target} in {current_room['name']}. 
        The room description: {current_room['description']}
        Player inventory: {', '.join(self.player.inventory) if self.player.inventory else 'empty'}
        {weapon_text}
        
        Generate a short, exciting fight outcome (2-3 sentences). 
        Make it adventurous but not too violent.
        """
        
        ai_response = self.ollama_client.generate_response(fight_prompt)
        
        if ai_response:
            self.logger.log(f"Fight with {target}: {ai_response}")
            return f"⚔️ {ai_response}"
        else:
            return f"⚔️ You engage the {target} in combat! The battle is fierce but you emerge victorious!"
    
    def _show_room_description(self):
        """Show current room description"""
        return self._handle_look()
    
    def show_help(self):
        """Show help information"""
        help_text = """
🎮 GAME COMMANDS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 LOOK (l)          - Look around current room
   look <direction>  - Look in specific direction (n/s/e/w)

🚶 MOVE (m)          - Move in a direction
   move <direction>  - Move north/south/east/west (n/s/e/w)

🤏 GRAB (g)          - Pick up an item
   grab <item>       - Grab specific item

🎒 INVENTORY (i)     - Show your inventory

🔧 USE (u)           - Use an item from inventory
   use <item>        - Use specific item

🔍 EXAMINE (x)       - Examine an item in detail
   examine <item>    - Get detailed item information

⚔️ FIGHT (f)         - Fight an enemy
   fight <enemy>     - Fight specific enemy

❓ HELP (h)          - Show this help
🚪 QUIT (q)          - Exit game

💡 TIP: You can use abbreviations! 
   'm n' = 'move north', 'l e' = 'look east', etc.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        print(help_text)