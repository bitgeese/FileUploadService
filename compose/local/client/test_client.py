import os
import time
import random
import string
import requests
from typing import Optional
from pathlib import Path


def generate_random_file(size_gb: int, path: Path) -> Path:
    """Generate a random file of specified size in GB."""
    # Create parent directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate random data in chunks to avoid memory issues
    chunk_size = 1024 * 1024  # 1MB chunks
    num_chunks = size_gb * 1024  # Convert GB to MB chunks
    
    with open(path, 'wb') as f:
        for _ in range(num_chunks):
            chunk = os.urandom(chunk_size)
            f.write(chunk)
    
    return path


def upload_file(file_path: Path, api_url: str) -> Optional[dict]:
    """Upload a file to the API with metadata."""
    if not file_path.exists():
        print(f"File {file_path} does not exist")
        return None
    
    # Generate random storage path
    storage_path = f"/storage/{''.join(random.choices(string.ascii_lowercase, k=8))}"
    
    # Prepare metadata
    metadata = {
        'intended_path': storage_path,
        'description': 'Test file upload'
    }
    
    # Prepare multipart form data
    files = {
        'file': (file_path.name, open(file_path, 'rb')),
        'metadata': (None, str(metadata))
    }
    
    try:
        response = requests.post(f"{api_url}/api/v1/files/upload/", files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error uploading file: {e}")
        return None
    finally:
        # Clean up the generated file
        file_path.unlink()


def main():
    """Main function to generate and upload a file."""
    api_url = os.environ.get('API_URL', 'http://django:8000')
    
    # Generate a random file between 4-8GB
    size_gb = random.randint(4, 8)
    file_path = Path('/tmp/test_file.dat')
    
    print(f"Generating {size_gb}GB test file...")
    generated_file = generate_random_file(size_gb, file_path)
    
    print("Uploading file...")
    result = upload_file(generated_file, api_url)
    
    if result:
        print(f"Upload successful: {result}")
    else:
        print("Upload failed")
        exit(1)


if __name__ == '__main__':
    # Add a small random delay to avoid all clients starting at exactly the same time
    time.sleep(random.uniform(0, 2))
    main() 