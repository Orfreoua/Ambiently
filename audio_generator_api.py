import requests
import time
import json
import requests
from pathlib import Path

class ReMusicAPI:
    def __init__(self, token):
        self.base_url = "https://remusic.ai/api/v1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "X-Token": token,
            "Origin": "https://remusic.ai",
            "Referer": "https://remusic.ai/en/ai-music-generator"
        }

    def generate_music(self, prompt, duration=90, supplier=3):
        """Generate music with the given prompt"""
        url = f"{self.base_url}/ai-music/music"
        payload = {
            "duration": duration,
            "prompt": prompt,
            "supplier": supplier
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def check_music_status(self, song_id):
        """Check the status of generated music"""
        url = f"{self.base_url}/ai-music/music/{song_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_credits(self):
        """Get user credits information"""
        url = f"{self.base_url}/user/credits"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def wait_for_completion(self, song_id, check_interval=5):
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

    def download_audio_file(url, song_id):
        """Download the audio file from the given URL"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Create downloads path
            downloads_dir = Path.home() / "Downloads"
            filename = f"remusic_{song_id}.mp3"
            filepath = downloads_dir / filename
            
            # Download with progress
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    # Show download progress
                    if total_size:
                        percent = int(100 * downloaded / total_size)
                        print(f"\rDownloading: {percent}%", end='')
                        
            print(f"\nFile saved to: {filepath}")
            return str(filepath)
        
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None

    def download_image_file(url, song_id):
        """Download the audio file from the given URL"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Create downloads path
            downloads_dir = Path.home() / "Downloads"
            filename = f"remusic_{song_id}.webp"
            filepath = downloads_dir / filename
            
            # Download with progress
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    # Show download progress
                    if total_size:
                        percent = int(100 * downloaded / total_size)
                        print(f"\rDownloading: {percent}%", end='')
                        
            print(f"\nFile saved to: {filepath}")
            return str(filepath)
        
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None


def main():
    # Replace with your actual token from the network request
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYW4iOiJlbiIsInZlciI6InZpcCIsInRpbWVzdGFtcCI6MTczMzE4MTcyNiwiZXhwaXJlIjoxNzMzNDQwOTI2LCJ1c2VyX2lkIjoiUzFac1JWaFhiVW89IiwicHJvZHVjdF9tYXJrIjoiMTAyIiwiZW1haWwiOiJtaW5lY3JhZnQ5NTEwMEBnbWFpbC5jb20iLCJYX1VJRCI6IlMxWnNSVmhYYlVvPSIsIlhfUE5NIjoicmVtdXNpYyJ9.4j2HhGbxBM2Wb7M5LAxsFlzrjKDqibq7xbVVeixrBPg"
    api = ReMusicAPI(token)

    # Check available credits
    credits = api.get_credits()
    print("Credits:", credits)

    # Generate music
    prompt = "Futuristic, tense yet hopeful; electronic ambient with steady beats"
    result = api.generate_music(prompt)
    
    if result["code"] == 100000:
        song_id = result["data"][0]["song_id"]
        print(f"Generation started. Song ID: {song_id}")
        
        # Wait for completion
        final_result = api.wait_for_completion(song_id)
        print("Generation completed!")
        print(f"Audio URL: {final_result['audio_url']}")
        
        filepath = api.download_audio_file(final_result['audio_url'], song_id)
        if filepath:
            print("Download audio completed successfully!")
            
        filepath = api.download_audio_file(final_result['image_large_url'], song_id)
        if filepath:
            print("Download image completed successfully!")
        
    else:
        print("Error:", result["message"])

if __name__ == "__main__":
    main()
