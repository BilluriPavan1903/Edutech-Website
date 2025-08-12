
# Edutech Website

A comprehensive web application that analyzes questions and answers generated from uploaded PDF documents. It uses advanced NLP models for **Question Generation (QG)** and **Question Answering (QA)** and evaluates answers for accuracy and readability. This tool is useful for self-assessment, tutoring, and exam preparation.

---

## Features

- Upload PDF study material and extract text automatically.
- Generate meaningful questions from the extracted text (QG).
- Answer generated or user-asked questions using a QA model.
- Evaluate answers using fuzzy matching and readability metrics.
- Local caching of Hugging Face models to speed up inference.

---

## Models & Libraries

**Question Generation**
- `google/flan-t5-large`
  - Pipeline: `text2text-generation` (Hugging Face Transformers)

**Question Answering**
- `deepset/roberta-base-squad2`
  - Pipeline: `question-answering` (Hugging Face Transformers)

**Evaluation & Utilities**
- `fuzzywuzzy` (string similarity)
- `python-Levenshtein` (optional, speeds fuzzywuzzy)
- `textstat` (readability and complexity metrics)
- Django (for the web app)

---



---

## Step-by-Step Setup Guide

### 1. Clone the repository
git clone https://github.com/BilluriPavan1903/Edutech-Website.git
cd EDUTECH-WEBSITE

text

### 2. Create and activate a Python virtual environment
**On Windows:**


python -m venv venv
venv\Scripts\activate

text
**On macOS/Linux:**


python3 -m venv venv
source venv/bin/activate

text

### 3. Install dependencies
pip install -r requirements.txt

text

### 4. Load and cache the ML models
Run the following to download Hugging Face models and cache them locally:
python model1.py

text
- This creates the `huggingface_models` folder and ensures models are cached to avoid repeated downloads.
- The `media` folder is also created if missing, for temporarily storing uploaded PDFs.

### 5. Run the Django development server
python manage.py runserver

text
- The app will be available at http://localhost:8000.

---

## Usage

- Upload PDFs, generate questions, get answers, and view evaluation metrics—all via the web interface!

---

## 📬 Contact

If you have any questions or feedback, feel free to reach out:

- **Name:** Pavan Billuri  
- **Email:** billuripavan891@gmail.com  
 
- **GitHub:** [github.com/BilluriPavan1903](https://github.com/BilluriPavan1903)  


## Notes

- This project is best run on a machine with sufficient memory for NLP model inference.
- If you experience issues running model downloads, double-check your environment and Python version.


## Project Structure

```text
EDUTECH-WEBSITE/
├── huggingface_models/          # Cached Hugging Face models
├── media/                       # Temporary uploaded PDFs and outputs
├── One/                         # Main Django app
│   ├── templates/
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── upload.html
│   │   └── user.html
│   ├── _init_.py
│   ├── asgi.py
│   ├── db.py                    # DB models/operations (your custom module)
│   ├── model.py                 # ML model loader & wrapper
│   ├── question.py              # QG & QA processing logic
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── project/                     # Optional/extendable backend modules
├── static/
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
├── db.sqlite3
├── manage.py
├── model1.py                    # Script to download & cache models locally
├── requirements.txt
└── README.md

