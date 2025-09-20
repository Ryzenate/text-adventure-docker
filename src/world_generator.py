import requests
import json
import os

class WorldGenerator:
    """
    Generates world data as a JSON string and loads it.
    """

    def __init__(self, api_url="http://localhost:1234/v1/chat/completions"):
        self.api_url = api_url
        self.headers = {"Content-Type": "application/json"}
        self.generated_world = None

    def _create_prompt(self, world_theme, rooms_to_generate, example_json_structure):
        """
        Constructs the system and user prompts to request JSON output.
        """
        system_prompt = f"""
        You are a highly-specialized AI assistant for generating data for text-based adventure games.
        Your task is to generate a JSON object representing the rooms of a game world.
        The output must be a single, complete, valid JSON object and nothing else. Do not include any conversational text, explanations, or code blocks.
        The top-level JSON object should have a single key, "rooms", which contains a dictionary of room objects.
        The room keys should be lowercase, using underscores instead of spaces (e.g., 'forest_entrance').
        """
        
        user_prompt = f"""
        Generate a JSON object for a game world with the theme: **{world_theme}**.
        The world should contain {rooms_to_generate} rooms.
        The structure for each room must exactly match this example:
        {example_json_structure}
        """

        return system_prompt, user_prompt

    def generate_world_data(self, world_theme, rooms_to_generate, example_json_structure):
        """
        Calls the LM Studio API to generate the world data as a JSON string.
        """
        print("Generating new world data as JSON with LM Studio...")
        system_prompt, user_prompt = self._create_prompt(world_theme, rooms_to_generate, example_json_structure)

        payload = {
            "model": "YOUR_MODEL_NAME_HERE", # Replace with your specific model name
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            generated_json_string = response.json()["choices"][0]["message"]["content"]
            
            # --- Attempt to clean and parse the JSON string ---
            print("Parsing generated JSON data...")
            # Some models might wrap the JSON in markdown code blocks
            if generated_json_string.startswith("```json"):
                generated_json_string = generated_json_string.split("```json")[1]
            if generated_json_string.endswith("```"):
                generated_json_string = generated_json_string.rsplit("```", 1)[0]

            # Attempt to load the JSON string into a Python dictionary
            world_data = json.loads(generated_json_string)
            
            # Now we can create the World class and instance
            class World:
                def __init__(self, rooms):
                    self.rooms = rooms
            
            self.generated_world = World(world_data.get("rooms", {}))
            print("World object created successfully from JSON.")

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to LM Studio API: {e}")
            self.generated_world = None
        except json.JSONDecodeError as e:
            print(f"Error parsing generated JSON: {e}")
            self.generated_world = None
        except KeyError as e:
            print(f"Error accessing key in API response: {e}")
            self.generated_world = None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.generated_world = None

        return self.generated_world

    def save_world_to_json(self, filename="generated_world.json"):
        """Saves the rooms dictionary of the generated world to a JSON file."""
        if self.generated_world:
            try:
                with open(filename, "w") as f:
                    json.dump(self.generated_world.rooms, f, indent=4)
                print(f"World data successfully saved to {filename}")
            except Exception as e:
                print(f"An error occurred while saving the file: {e}")
        else:
            print("No world object to save. Please generate one first.")

    def load_world_from_json(self, filename="generated_world.json"):
        """Loads world data from a JSON file and creates a new World object."""
        try:
            with open(filename, "r") as f:
                rooms_data = json.load(f)
            
            class World:
                def __init__(self, rooms):
                    self.rooms = rooms
            
            self.generated_world = World(rooms_data)
            print(f"World data successfully loaded from {filename}")
            return self.generated_world
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading file: {e}")
            return None

# --- Example Usage ---
if __name__ == "__main__":
    example_json = """
    {
        "rooms": {
            "forest_entrance": {
                "name": "Forest Entrance",
                "description": "You stand at the edge of a mysterious forest.",
                "short_desc": "The entrance to a mysterious forest",
                "exits": {
                    "north": "forest_path"
                },
                "items": ["stick"],
                "enemies": []
            }
        }
    }
    """

    generator = WorldGenerator()
    new_world = generator.generate_world_data(
        world_theme="an alien jungle planet",
        rooms_to_generate=4,
        example_json_structure=example_json
    )

    if new_world:
        print("\n--- Generated World Data ---")
        print(f"Number of rooms: {len(new_world.rooms)}")
        generator.save_world_to_json()