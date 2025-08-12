# One/model.py

import re
from transformers import pipeline

# ✅ Load pre-downloaded models (no need for cache_dir)
qg_pipeline = pipeline("text2text-generation", model="google/flan-t5-large")
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

# ✅ Utility: Split long text into sentences
def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

# ✅ Utility: Clean generated questions
def clean_questions(raw_text):
    questions = [q.strip() + '?' for q in raw_text.split('?') if q.strip()]
    return questions

# ✅ Main function: Generate question-answer pairs
def generate_qa_pairs(full_paragraph, chunk_size=2):
    sentences = split_sentences(full_paragraph)
    chunks = [' '.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]

    qa_pairs = []

    for i, chunk in enumerate(chunks, 1):
        try:
            prompt = f"Generate 3 questions from the following context:\n{chunk}"
            questions_output = qg_pipeline(prompt, max_length=256, do_sample=False)
            raw_questions = questions_output[0]['generated_text']
            questions = clean_questions(raw_questions)

            for q in questions:
                try:
                    answer = qa_pipeline(question=q, context=chunk)['answer']
                    qa_pairs.append((q, answer))
                except Exception:
                    qa_pairs.append((q, "[Answer not found]"))

        except Exception as e:
            print(f"❌ Error in chunk {i}: {e}")

    return qa_pairs
