"""
Item definitions and management system
"""

class Item:
    """Base item class"""
    def __init__(self, name, description, value=0, usable=False, consumable=False):
        self.name = name
        self.description = description
        self.value = value
        self.usable = usable
        self.consumable = consumable
    
    def use(self, player, game_engine):
        """Use item (override in subclasses)"""
        if not self.usable:
            return f"You can't use the {self.name}."
        return f"You use the {self.name}."
    
    def __str__(self):
        return self.name

class Weapon(Item):
    """Weapon item class"""
    def __init__(self, name, description, damage, value=0):
        super().__init__(name, description, value, usable=True)
        self.damage = damage
    
    def use(self, player, game_engine):
        return f"You brandish the {self.name} menacingly! (Damage: {self.damage})"

class ConsumableItem(Item):
    """Consumable item class"""
    def __init__(self, name, description, effect_type, effect_value, value=0):
        super().__init__(name, description, value, usable=True, consumable=True)
        self.effect_type = effect_type  # 'health', 'mana', etc.
        self.effect_value = effect_value
    
    def use(self, player, game_engine):
        if self.effect_type == 'health':
            player.health = min(100, player.health + self.effect_value)
            return f"You consume the {self.name} and restore {self.effect_value} health!"
        return f"You use the {self.name}."

class ItemManager:
    """Manages all game items"""
    
    def __init__(self):
        self.items = self._initialize_items()
    
    def _initialize_items(self):
        """Initialize all game items"""
        items = {}
        
        # Basic items
        items['stick'] = Item(
            name='stick',
            description='A sturdy wooden stick, perfect for poking things or as a makeshift weapon.',
            value=1
        )
        
        items['stone'] = Item(
            name='stone',
            description='A smooth river stone that fits perfectly in your palm.',
            value=1
        )
        
        items['rope'] = Item(
            name='rope',
            description='A length of weathered but strong rope. Could be useful for climbing.',
            value=5
        )
        
        items['coin'] = Item(
            name='coin',
            description='An old golden coin with mysterious symbols etched on both sides.',
            value=10
        )
        
        items['flowers'] = ConsumableItem(
            name='flowers',
            description='Beautiful wildflowers that seem to glow with an inner light.',
            effect_type='health',
            effect_value=10,
            value=3
        )
        
        items['berries'] = ConsumableItem(
            name='berries',
            description='Sweet forest berries that look delicious and nourishing.',
            effect_type='health',
            effect_value=15,
            value=5
        )
        
        items['crystal'] = Item(
            name='crystal',
            description='A mysterious crystal that pulses with magical energy.',
            value=25,
            usable=True
        )
        
        items['torch'] = Item(
            name='torch',
            description='A wooden torch wrapped in oil-soaked cloth. Perfect for dark places.',
            value=8,
            usable=True
        )
        
        items['gem'] = Item(
            name='gem',
            description='A precious gem that sparkles with inner fire.',
            value=50
        )
        
        # Weapons
        items['rusty_sword'] = Weapon(
            name='rusty sword',
            description='An old sword with a rusty blade, but still sharp enough to be dangerous.',
            damage=15,
            value=20
        )
        
        items['magic_wand'] = Weapon(
            name='magic wand',
            description='A slender wand carved from ancient wood, thrumming with arcane power.',
            damage=20,
            value=40
        )
        
        return items
    
    def get_item(self, item_name):
        """Get item by name"""
        return self.items.get(item_name.lower())
    
    def get_all_items(self):
        """Get all items"""
        return self.items
    
    def add_item(self, item):
        """Add new item to the manager"""
        self.items[item.name.lower()] = item
    
    def item_exists(self, item_name):
        """Check if item exists"""
        return item_name.lower() in self.items
    
    def get_item_description(self, item_name):
        """Get detailed item description"""
        item = self.get_item(item_name)
        if not item:
            return None
            
        desc = f"📦 {item.name.title()}\n"
        desc += f"📝 {item.description}\n"
        
        if hasattr(item, 'damage'):
            desc += f"⚔️ Damage: {item.damage}\n"
        
        if hasattr(item, 'effect_value'):
            desc += f"💚 Restores: {item.effect_value} {item.effect_type}\n"
        
        if item.value > 0:
            desc += f"💰 Value: {item.value} gold"
        
        return desc