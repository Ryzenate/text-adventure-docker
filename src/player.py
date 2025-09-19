"""
Player class definition
"""

class Player:
    def __init__(self):
        self.name = "Adventurer"
        self.current_room = None
        self.inventory = []
        self.health = 100
        self.experience = 0
        self.level = 1
    
    def add_item(self, item):
        """Add item to inventory"""
        self.inventory.append(item)
    
    def remove_item(self, item):
        """Remove item from inventory"""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def has_item(self, item):
        """Check if player has item"""
        return item in self.inventory
    
    def get_status(self):
        """Get player status"""
        return {
            "name": self.name,
            "health": self.health,
            "level": self.level,
            "experience": self.experience,
            "inventory_count": len(self.inventory)
        }