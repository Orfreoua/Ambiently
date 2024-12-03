import requests
import time
from pathlib import Path
from typing import Dict, Any, Optional

class ReMusicAPI:
    """API client for ReMusicAI service"""
    
    def __init__(self, token: str) -> None:
        """Initialize API client with authentication token"""
        self.base_url = "https://remusic.ai/api/v1"
        self.headers = {
            "User-Agent": "ReMusicAPI/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Token": token,
            "Origin": "https://remusic.ai",
            "Referer": "https://remusic.ai/en/ai-music-generator"
        }

    def generate_music(self, prompt: str, duration: int = 90, supplier: int = 3) -> Dict[str, Any]:
        """Generate music with the given prompt"""
        url = f"{self.base_url}/ai-music/music"
        payload = {
            "duration": duration,
            "prompt": prompt,
            "supplier": supplier
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def check_music_status(self, song_id: str) -> Dict[str, Any]:
        """Check the status of generated music"""
        url = f"{self.base_url}/ai-music/music/{song_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_credits(self) -> Dict[str, Any]:
        """Get user credits information"""
        url = f"{self.base_url}/user/credits"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, song_id: str, check_interval: int = 5) -> Dict[str, Any]:
        """Wait for music generation to complete"""
        while True:
            status = self.check_music_status(song_id)
            if status["code"] == 100000:
                data = status["data"]
                if data["status"] == "success":
                    return data
                elif data["status"] == "pending":
                    print(f"Progress: {data['percentage']}%")
                    time.sleep(check_interval)
                else:
                    raise Exception(f"Generation failed: {data['status']}")

    def download_file(self, url: str, song_id: str, file_type: str) -> Optional[str]:
        """Download a file from the given URL"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            downloads_dir = Path.home() / "Downloads"
            downloads_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"remusic_{song_id}.{file_type}"
            filepath = downloads_dir / filename
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    if total_size:
                        percent = int(100 * downloaded / total_size)
                        print(f"\rDownloading: {percent}%", end='')
            
            print(f"\nFile saved to: {filepath}")
            return str(filepath)
        
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None

    def download_audio(self, url: str, song_id: str) -> Optional[str]:
        """Download audio file"""
        return self.download_file(url, song_id, "mp3")

    def download_image(self, url: str, song_id: str) -> Optional[str]:
        """Download image file"""
        return self.download_file(url, song_id, "webp")

def main() -> None:
    # Load token from environment variable or config file
    token = "YOUR_TOKEN_HERE"
    api = ReMusicAPI(token)

    try:
        credits = api.get_credits()
        if credits['message'] == 'success':
            print("Credits:", credits['data']['available'], "/", credits['data']['total'])

        prompt = "Futuristic electronic ambient"
        result = api.generate_music(prompt)
        
        if result["code"] == 100000:
            song_id = result["data"][0]["song_id"]
            print(f"Generation started. Song ID: {song_id}")
            
            final_result = api.wait_for_completion(song_id)
            print("Generation completed!")
            
            if audio_path := api.download_audio(final_result['audio_url'], song_id):
                print("Audio downloaded successfully!")
            if image_path := api.download_image(final_result['image_large_url'], song_id):
                print("Image downloaded successfully!")
        else:
            print("Error:", result["message"])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
