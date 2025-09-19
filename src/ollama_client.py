"""
Ollama client for AI-powered responses
"""

import requests
import json
import os

class OllamaClient:
    def __init__(self, logger):
        self.logger = logger
        self.host = os.getenv('OLLAMA_HOST', 'localhost:11434')
        self.model = 'gemma2'
        self.base_url = f"http://{self.host}"
        
    def generate_response(self, prompt, max_tokens=150):
        """Generate AI response using Ollama"""
        try:
            url = f"{self.base_url}/api/generate"
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7
                }
            }
            
            self.logger.log(f"Sending request to Ollama: {prompt[:100]}...")
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '').strip()
                self.logger.log(f"Ollama response: {ai_response[:100]}...")
                return ai_response
            else:
                self.logger.log(f"Ollama error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            self.logger.log("Cannot connect to Ollama service")
            return None
        except requests.exceptions.Timeout:
            self.logger.log("Ollama request timed out")
            return None
        except Exception as e:
            self.logger.log(f"Ollama client error: {str(e)}")
            return None
    
    def is_available(self):
        """Check if Ollama service is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False