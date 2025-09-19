"""
World definition and room management
"""

class World:
    def __init__(self):
        self.rooms = {
            "forest_entrance": {
                "name": "Forest Entrance",
                "description": "You stand at the edge of a mysterious forest. Ancient trees tower above you, their branches creating a canopy that filters the sunlight into dancing patterns on the forest floor.",
                "short_desc": "The entrance to a mysterious forest",
                "exits": {
                    "north": "forest_path",
                    "east": "old_well"
                },
                "items": ["stick", "stone"],
                "enemies": []
            },
            "forest_path": {
                "name": "Forest Path",
                "description": "A winding path leads deeper into the forest. You hear the distant sound of running water and the rustling of small creatures in the underbrush.",
                "short_desc": "A winding forest path",
                "exits": {
                    "south": "forest_entrance",
                    "north": "forest_clearing",
                    "west": "dark_cave"
                },
                "items": ["berries"],
                "enemies": ["forest sprite"]
            },
            "old_well": {
                "name": "Old Well",
                "description": "An ancient stone well sits in a small clearing. Moss covers its weathered stones, and a rusty bucket hangs from a frayed rope. The well seems to whisper secrets of ages past.",
                "short_desc": "An ancient stone well",
                "exits": {
                    "west": "forest_entrance",
                    "north": "forest_clearing"
                },
                "items": ["rope", "coin"],
                "enemies": []
            },
            "forest_clearing": {
                "name": "Forest Clearing",
                "description": "A beautiful clearing opens up before you, bathed in golden sunlight. Wildflowers bloom in abundance, and butterflies dance among them. This feels like a place of peace and magic.",
                "short_desc": "A peaceful forest clearing",
                "exits": {
                    "south": "forest_path",
                    "east": "old_well",
                    "west": "dark_cave"
                },
                "items": ["flowers", "crystal"],
                "enemies": []
            },
            "dark_cave": {
                "name": "Dark Cave",
                "description": "The cave entrance yawns before you like a hungry mouth. Cool, damp air flows from within, carrying strange echoes and the scent of earth and mystery.",
                "short_desc": "A dark, mysterious cave",
                "exits": {
                    "east": "forest_path",
                    "south": "forest_clearing"
                },
                "items": ["torch", "gem"],
                "enemies": ["cave troll"]
            }
        }
    
    def get_room(self, room_id):
        """Get room by ID"""
        return self.rooms.get(room_id, {})
    
    def get_all_rooms(self):
        """Get all rooms"""
        return self.rooms