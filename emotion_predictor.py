import torch
from transformers import BertTokenizer, BertForSequenceClassification
import zipfile
import os
import gdown

# === Step 1: Download model from Google Drive using gdown ===
model_dir = "my_emotion_model"
zip_path = "my_emotion_model.zip"
file_id = "1uwqHzeop5TbqpU7Gn8G2vG9MBHV0Wt2f"
gdrive_url = f"https://drive.google.com/uc?id={file_id}"

if not os.path.exists(model_dir):
    print("Downloading model from Google Drive using gdown...")
    gdown.download(gdrive_url, zip_path, quiet=False)

    if not zipfile.is_zipfile(zip_path):
        print("Downloaded file is not a valid zip file. Please check the file ID or try again.")
        exit()

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(model_dir)
    print("Model unzipped successfully.")
    os.remove(zip_path)

# === Step 2: Load tokenizer and model ===
tokenizer = BertTokenizer.from_pretrained(model_dir)
model = BertForSequenceClassification.from_pretrained(model_dir)
model.eval()

# === Step 3: Emotion prediction ===
emotion_labels = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring",
    "confusion", "curiosity", "desire", "disappointment", "disapproval", "embarrassment",
    "excitement", "fear", "gratitude", "grief", "joy", "love",
    "nervousness", "optimism", "pride", "realization", "relief", "remorse",
    "sadness", "surprise", "neutral", "none"
]

def predict_emotion(text, threshold=0.3, top_k=4):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.sigmoid(outputs.logits).squeeze().numpy()

    sorted_indices = probs.argsort()[::-1]
    top_emotions = [emotion_labels[i] for i in sorted_indices[:top_k]]
    predicted = [emotion_labels[i] for i, prob in enumerate(probs) if prob > threshold]

    return predicted, top_emotions

print("\nEmotion Prediction Ready (type 'exit' to quit)\n")
while True:
    user_input = input("Enter a sentence: ")
    if user_input.lower() == "exit":
        break
    predicted_emotions, top_emotions = predict_emotion(user_input)
    print("Predicted Emotions:", predicted_emotions)
    print("Top 4 Emotions:", top_emotions, "\n")
