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
- Django for the web app

---








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
│   ├── __init__.py
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

That final  










