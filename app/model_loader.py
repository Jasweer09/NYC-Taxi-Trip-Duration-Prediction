import gdown
import os

def download_model_from_drive():
    model_path = "model/model.pkl"
    if not os.path.exists(model_path):
        print("Downloading model from Google Drive...")
        os.makedirs("model", exist_ok=True)
        
        # Replace FILE_ID with your actual file ID from the shareable link
        file_id = "YOUR_FILE_ID_HERE"
        url = f"https://drive.google.com/uc?id={file_id}"
        
        gdown.download(url, model_path, quiet=False)
        print(f"Model downloaded and saved to: {model_path}")
    else:
        print("Model already exists.")

# Call it when loading model
download_model_from_drive()

# Then load it as usual
import pickle

with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)
