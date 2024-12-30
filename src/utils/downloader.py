import os
import json
import requests
import gzip
import shutil

def read_urls(file_path="data/input/urls.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"URLs file '{file_path}' not found.")
    with open(file_path, "r") as file:
        return json.load(file)

def download_dataset(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        compressed_file = save_path + ".gz" if url.endswith(".gz") else save_path
        
        with open(compressed_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Dataset downloaded and saved to '{compressed_file}'.")
        
        if compressed_file.endswith(".gz"):
            with gzip.open(compressed_file, "rb") as f_in:
                with open(save_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(compressed_file)
            print(f"Extracted '{save_path}'.")
    else:
        print(f"Failed to download {url}. HTTP Status Code: {response.status_code}")

def download_all(datasets, output_dir="data/input/dateset"):
    os.makedirs(output_dir, exist_ok=True)
    for dataset in datasets:
        file_name = os.path.basename(dataset["name"]) + '.txt'
        save_path = os.path.join(output_dir, file_name)
        if not os.path.exists(save_path):
            print(f"Downloading {dataset['name']}...")
            download_dataset(dataset["url"], save_path)
        else:
            print(f"Dataset '{file_name}' already exists. Skipping download.")
