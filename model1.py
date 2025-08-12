# model1.py
import os
from transformers import pipeline

# Define a folder to store models locally
local_model_dir = os.path.join(os.getcwd(), "huggingface_models")
os.makedirs(local_model_dir, exist_ok=True)

print("🔁 Downloading and caching models into:", local_model_dir)

# Download and cache Question Generation model
qg_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    cache_dir=local_model_dir
)
print("✅ Question Generation model downloaded.")

# Download and cache Question Answering model
qa_pipeline = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2",
    cache_dir=local_model_dir
)
print("✅ Question Answering model downloaded.")

print("🎉 All models cached successfully at:", local_model_dir)
