import requests
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
import subprocess
import time
import os

print("REMINDER: dont print anything with _cache_ included in filename")

videourl = input("video url: ")
audiourl = input("audio url: ")
filename = f"{input('filename (without extension): ') or f"final_{time.time()}"}.mp4"

mp4name = "./_cache_.mp4"
mp3name = "./_cache_.mp3"
cleanmp4name = "./_cache_c.mp4"
cleanmp3name = "./_cache_c.mp3"

def clean_url(url, params_to_remove):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    for param in params_to_remove:
        query_params.pop(param, None)
    cleaned_query = urlencode(query_params, doseq=True)
    cleaned_url = urlunparse(parsed_url._replace(query=cleaned_query))
    
    return cleaned_url

cleaned_url = clean_url(videourl, ['bytestart', 'byteend'])
response = requests.get(cleaned_url)
with open(mp4name, 'wb') as f:
    f.write(response.content)

subprocess.run(["ffmpeg", "-i", mp4name, cleanmp4name], check=True)

cleaned_url = clean_url(audiourl, ['bytestart', 'byteend'])
response = requests.get(cleaned_url)
with open(mp3name, 'wb') as f:
    f.write(response.content)

# Convert the MP3 file explicitly with codec options
subprocess.run([
    "ffmpeg", 
    "-i", mp3name, 
    "-acodec", "libmp3lame", 
    "-ab", "192k", 
    cleanmp3name
], check=True)

# Merge video and audio files
subprocess.run([
    "ffmpeg", 
    "-i", cleanmp4name, 
    "-i", cleanmp3name, 
    "-c:v", "copy", 
    "-c:a", "aac", 
    "-strict", "experimental",
    filename
], check=True)

for item in [mp4name, mp3name, cleanmp4name, cleanmp3name]:
    if os.path.exists(item):
        os.remove(item)
