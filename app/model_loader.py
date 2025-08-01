import os
import pickle
import requests

def download_model_from_drive(file_id, dest_path):
    print("Checking if model exists...")
    if os.path.exists(dest_path):
        print("Model already exists.")
        return

    print("Downloading model from Google Drive...")
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(response.content)
    print("Model downloaded and saved to:", dest_path)

# Set your Google Drive File ID here
FILE_ID = "1VgjFrEtSTXAl3ks-dYLBaIe17bdpWSIk"  # <-- replace with yours
MODEL_PATH = "model/model.pkl"

# Download the model if not present
download_model_from_drive(FILE_ID, MODEL_PATH)

# Load the model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def load_ridge_model():
    return model


