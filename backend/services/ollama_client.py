import requests
import time

class OllamaClient:
    def __init__(self, model="llama3"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model
        self.timeout = 180  # 3 minutes for slow responses

    def generate_response(self, prompt):
        """Generate response from Ollama with better error handling"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }

            print(f"🤖 Sending request to Ollama (model: {self.model})...")
            start_time = time.time()
            
            res = requests.post(self.url, json=payload, timeout=self.timeout)
            
            elapsed = time.time() - start_time
            print(f"⏱️  Ollama responded in {elapsed:.2f} seconds")
            
            res.raise_for_status()
            
            response_data = res.json()
            if "response" not in response_data:
                raise ValueError("Invalid response from Ollama - missing 'response' field")
            
            return response_data["response"]
            
        except requests.exceptions.ConnectionError:
            error_msg = f"""
❌ Cannot connect to Ollama!

Please ensure:
1. Ollama is running: Open a terminal and run 'ollama serve'
2. Ollama is accessible at: {self.url}

If Ollama is not installed, download from: https://ollama.ai/download
"""
            print(error_msg)
            raise ConnectionError("Ollama is not running. Please start Ollama with 'ollama serve'")
            
        except requests.exceptions.Timeout:
            error_msg = f"""
⏱️ Ollama request timed out after {self.timeout} seconds!

This usually means:
1. The model is very slow (first run can be slow)
2. Your system is under heavy load
3. The model might be too large for your hardware

Try:
- Wait a bit and try again
- Use a smaller model
- Check Ollama logs
"""
            print(error_msg)
            raise TimeoutError(f"Ollama took too long to respond (>{self.timeout}s)")
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                error_msg = f"""
❌ Model '{self.model}' not found!

Please pull the model first:
    ollama pull {self.model}

Available models: ollama list
"""
                print(error_msg)
                raise ValueError(f"Model '{self.model}' not found. Run: ollama pull {self.model}")
            else:
                print(f"❌ HTTP Error from Ollama: {e}")
                raise
                
        except Exception as e:
            print(f"❌ Unexpected error calling Ollama: {e}")
            raise
