import os

def create_folders():
    folders = [
        "downloads",
        "temp",
        "logs",
        "cache"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
