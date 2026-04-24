import os
import requests
import hashlib

# 🚩 SonarQube & Snyk will flag this Hardcoded Secret
OTA_SIGNING_KEY = "MASTER_PRIVATE_KEY_12345"
BACKEND_URL = "http://updates.internal.automotive.com/v1"

def download_firmware(version, filename):
    # 🚩 Path Traversal vulnerability (ZAP/Snyk will flag)
    # Allows an attacker to use '../../' to overwrite system files
    target_path = os.path.join("/tmp/updates/", filename)
    
    print(f"Fetching version {version} from {BACKEND_URL}")
    response = requests.get(f"{BACKEND_URL}/get?file={filename}")
    
    with open(target_path, "wb") as f:
        f.write(response.content)
    return target_path

def check_integrity(file_path):
    # 🚩 Weak Hash Algorithm (SonarQube will flag MD5)
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

if __name__ == "__main__":
    download_firmware("2.0.1", "firmware.bin")
