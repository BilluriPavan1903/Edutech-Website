from .db import saved_collection

def save_qa_to_mongo(username, pdf_name, qa_pairs):
    doc = {
        "username": username,
        "pdf_name": pdf_name,
        "questions": []
    }

    for idx, (question, answer) in enumerate(qa_pairs, 1):
        doc["questions"].append({
            "question_id": f"Q{idx}",
            "question": question,
            "answer": answer
        })

    saved_collection.insert_one(doc)
    print(f"✅ Saved Q&A to MongoDB for user: {username}")
