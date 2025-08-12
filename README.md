Edutech Website


A comprehensive web application designed to analyze questions and answers generated from PDF documents uploaded by users. It uses advanced Natural Language Processing (NLP) models for Question Generation (QG) and Question Answering (QA), along with evaluation techniques to ensure answer accuracy and quality.

Project Overview
This application enables users to upload PDF files containing study material or any textual content. It then automatically:

Extracts relevant content from the PDFs.

Generates meaningful questions based on the extracted text using a Question Generation model.

Answers those questions using a powerful Question Answering model.

Evaluates the answers for accuracy and readability using fuzzy matching and text statistics.

This makes it a powerful educational tool for self-assessment, tutoring, and exam preparation.

Models & Libraries Used
1. Question Generation Model
Model: google/flan-t5-large

Pipeline: text2text-generation from Hugging Face Transformers

Purpose: To generate relevant, contextual questions from the text extracted from the PDF.

Details: This is a large pretrained T5 model fine-tuned for text-to-text tasks including question generation, providing high-quality, natural language questions.

2. Question Answering Model
Model: deepset/roberta-base-squad2

Pipeline: question-answering from Hugging Face Transformers

Purpose: To answer the generated or user-asked questions based on the uploaded content.

Details: A RoBERTa-based model fine-tuned on SQuAD2.0 dataset, effective in handling answerable and unanswerable questions with high accuracy.

3. Evaluation and Scoring Libraries
fuzzywuzzy: For fuzzy string matching to compare generated answers with expected answers, calculating similarity scores.

python-Levenshtein: Optional, but speeds up fuzzywuzzy computations.

textstat: Provides readability scores and text complexity metrics to ensure the answers are understandable and meet quality benchmarks.



Detailed Project Structure :


EDUTECH-WEBSITE/
│
├── huggingface_models/          # Cached Hugging Face models stored locally to speed up loading
│
├── media/                       # Temporary folder where uploaded PDFs and related media files are stored
│
├── One/                        # Main Django app folder containing all backend logic and templates
│   ├── __pycache__/            # Auto-generated Python cache files
│   ├── templates/              # HTML templates for rendering pages
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── upload.html
│   │   └── user.html
│   ├── __init__.py             # Marks the folder as a Python package
│   ├── asgi.py                 # ASGI interface config for asynchronous support
│   ├── db.py                   # Handles database operations and models
│   ├── model.py                # Contains code to load, initialize, and interact with ML models
│   ├── question.py             # Logic related to question generation, answering, and processing
│   ├── settings.py             # Django project settings (database, static files, middleware, etc.)
│   ├── urls.py                 # URL routing to connect views with endpoints
│   ├── views.py                # Web views/controllers processing requests and rendering responses
│   └── wsgi.py                 # WSGI interface for deployment (production use)
│
├── project/                    # Additional backend modules (optional/extendable)
│
├── static/                     # Static files served to frontend (CSS, JavaScript, images)
│   ├── css/
│   │   ├── home.css
│   │   ├── login.css
│   │   ├── signup.css
│   │   └── upload.css
│   └── js/
│       ├── home.js
│       ├── login.js
│       ├── signup.js
│       └── upload.js
│
├── db.sqlite3                  # SQLite database file storing user info, sessions, etc.
├── manage.py                  # Django management script for running server, migrations, etc.
├── model1.py                  # Python script to download and load the ML models
├── requirements.txt           # List of Python dependencies and libraries needed to run the project




Step-by-Step Setup Guide
Clone the repository
git clone https://github.com/BilluriPavan1903/Edutech-Website.git
cd EDUTECH-WEBSITE
Create and activate a Python virtual environment

On Windows:

python -m venv venv
venv\Scripts\activate
On macOS/Linux:

python3 -m venv venv
source venv/bin/activate
Install dependencies

pip install -r requirements.txt
Load and cache the ML models

Run the following to download Hugging Face models and cache them locally:
python model1.py
This creates the huggingface_models folder and ensures models are cached to avoid repeated downloads.

The media folder is also created if missing, for temporarily storing uploaded PDFs.

Run the Django development server

python manage.py runserver
The app will be available at http://localhost:8000.

Open your browser and start using the app

Upload PDFs, generate questions, get answers, and view evaluation metrics—all via the web interface!


Contact Me :
+91 7013799733
billuripavan891@gmail.com




