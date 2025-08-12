from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .db import reg_collection, saved_collection, saved_useranswer
from .db import report_collection
from django.utils import timezone
from django.conf import settings
import os
import random
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from .model import generate_qa_pairs
from .question import save_qa_to_mongo
from fuzzywuzzy import fuzz
import textstat

def signup(request):
    return render(request, "signup.html")

@csrf_exempt  # You can remove this if you handle CSRF in JS
def signup_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if not username or not password or not email:
            return JsonResponse({"success": False, "message": "All fields are required."})

        if reg_collection.find_one({"email": email}):
            return JsonResponse({"success": False, "message": "Email already registered."})

        if reg_collection.find_one({"username": username}):
            return JsonResponse({"success": False, "message": "Username already exists."})

        # Storing plain password (not secure – for testing only)
        reg_collection.insert_one({
            "username": username,
            "password": password,
            "email": email,
        })

        return JsonResponse({"success": True, "message": "User registered successfully."})

    return JsonResponse({"success": False, "message": "Invalid request method."})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'success': False, 'message': 'All fields are required.'})

        user = reg_collection.find_one({'username': username})
        if not user:
            return JsonResponse({'success': False, 'message': 'Username does not exist.'})
        if user['password'] != password:
            return JsonResponse({'success': False, 'message': 'Incorrect password.'})

        request.session['username'] = username  # Session storage
        return JsonResponse({'success': True, 'message': 'Login successful.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def home(request):
    username = request.session.get('username')
    return render(request, 'home.html', {'username': username})


def login(request):
    return render(request, 'login.html')


def get_username(request):
    return JsonResponse({'username': request.user.username})


def user_profile(request):
    username = request.session.get('username')
    return render(request, 'user.html', {'username': username})


def extract_text_and_tables(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"
    return all_text


def extract_ocr_text(pdf_path):
    ocr_text = ""
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        ocr_text += f"\n--- OCR Page {i+1} ---\n"
        ocr_text += pytesseract.image_to_string(image)
    return ocr_text


def upload(request):
    extracted_text = None
    qa_pairs = []
    questions_to_ask = []
    message = None

    pdf_name = None
    username = request.session.get('username')

    if request.method == "POST":
        if request.FILES.get("pdf_file"):
            pdf_file = request.FILES["pdf_file"]
            pdf_name = pdf_file.name

            # Save uploaded PDF file
            temp_path = os.path.join(settings.MEDIA_ROOT, pdf_name)
            with open(temp_path, "wb+") as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            # Extract text & generate Q&A pairs
            extracted_text = extract_text_and_tables(temp_path)
            qa_pairs = generate_qa_pairs(extracted_text)

            # Save Q&A in DB
            save_qa_to_mongo(username, pdf_name, qa_pairs)

            # Retrieve latest saved doc to get questions
            user_docs = list(saved_collection.find({"username": username, "pdf_name": pdf_name}).sort("_id", -1))
            if user_docs:
                latest_doc = user_docs[0]
                questions = latest_doc.get("questions", [])
                random_questions = random.sample(questions, min(5, len(questions)))
                questions_to_ask = [{"question_id": q["question_id"], "question": q["question"]} for q in random_questions]
                
                
            try:
                os.remove(temp_path)
            except Exception as e:
                print(f"Error deleting file {temp_path}: {e}")
  

    return render(request, "upload.html", {
        "extracted_text": extracted_text,
        "qa_pairs": qa_pairs,
        "questions_to_ask": questions_to_ask,
        "success": bool(qa_pairs),
        "pdf_name": pdf_name,
        "username": username,
        "message": message
    })


@csrf_exempt
def submit_answers(request):
    if request.method == "POST":
        try:
            username = request.session.get("username")
            pdf_name = request.POST.get("pdf_name")
            total = request.POST.get("total")

            if not username or not pdf_name:
                return JsonResponse({"error": "Missing username or PDF name."})

            if not total or not total.isdigit():
                return JsonResponse({"error": "Invalid total number of answers."})

            total = int(total)

            answers = []
            for i in range(1, total + 1):
                question_id = request.POST.get(f"question_id_{i}")
                question_text = request.POST.get(f"question_text_{i}")
                answer = request.POST.get(f"answer_{i}")

                if not question_id or not question_text or not answer:
                    continue  # skip incomplete answers

                answers.append({
                    "question_id": question_id,
                    "question": question_text,
                    "user_answer": answer
                })

            if not answers:
                return JsonResponse({"error": "No valid answers submitted."})

            # Save user answers to DB
            saved_useranswer.insert_one({
                "username": username,
                "pdf_name": pdf_name,
                "user_answered": True,
                "answers": answers
            })

            return JsonResponse({"message": "✅ Answers submitted and saved successfully!"})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": f"Server error: {str(e)}"})

    return JsonResponse({"error": "Invalid request method."})


def get_random_questions(request):
    if request.method == "GET":
        username = request.session.get('username')
        pdf_name = request.GET.get('pdf_name')

        if not username or not pdf_name:
            return JsonResponse({"error": "Missing username or pdf_name"}, status=400)

        user_docs = list(saved_collection.find({"username": username, "pdf_name": pdf_name}).sort('_id', -1))
        if not user_docs:
            return JsonResponse({"error": "No saved questions found"}, status=404)

        latest_doc = user_docs[0]
        questions = latest_doc.get("questions", [])
        if not questions:
            return JsonResponse({"error": "No questions found in document"}, status=404)

        random_questions = random.sample(questions, min(5, len(questions)))
        questions_to_send = [
            {"question_id": q["question_id"], "question": q["question"]}
            for q in random_questions
        ]

        return JsonResponse({"questions": questions_to_send})

    return JsonResponse({"error": "Invalid request method"}, status=405)





@csrf_exempt
def evaluate_answers(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=405)

    username = request.session.get('username')
    pdf_name = request.POST.get('pdf_name')

    if not username or not pdf_name:
        return JsonResponse({"error": "Missing username or pdf_name"}, status=400)

    # Fetch user answers document
    user_answer_doc = saved_useranswer.find_one({"username": username, "pdf_name": pdf_name})
    if not user_answer_doc:
        return JsonResponse({"error": "No submitted answers found"}, status=404)

    # Fetch correct questions + answers
    saved_doc = saved_collection.find_one({"username": username, "pdf_name": pdf_name}, sort=[('_id', -1)])
    if not saved_doc:
        return JsonResponse({"error": "No saved questions found"}, status=404)

    correct_questions = saved_doc.get("questions", [])
    user_answers = user_answer_doc.get("answers", [])

    # --- Change 1: Use 'answer' key here instead of 'correct_answer'
    correct_answer_map = {q['question_id']: q.get('answer', '') for q in correct_questions}

    # --- Change 2: Create a map for questions to get question text reliably
    question_map = {q['question_id']: q.get('question', '') for q in correct_questions}

    results = []
    total_score = 0
    count = 0

    for ans in user_answers:
        qid = ans.get("question_id")
        user_ans_text = ans.get("user_answer", "").strip()
        correct_ans_text = correct_answer_map.get(qid, "").strip()

        # --- Change 3: Accuracy calculation same as upper function
        accuracy_score = fuzz.ratio(user_ans_text.lower(), correct_ans_text.lower()) if correct_ans_text else 0

        # Keep readability and final score calculation as before
        readability_score = textstat.flesch_reading_ease(user_ans_text) if len(user_ans_text) > 20 else 100.0
        final_score = round((accuracy_score * 0.7) + (readability_score * 0.3), 2)

        results.append({
            "question_id": qid,
            # --- Change 4: Use question text from question_map instead of user answer document
            "question": question_map.get(qid, ""),
            "accuracy": accuracy_score,
            "readability": round(readability_score, 2),
            "final_score": final_score
        })

        total_score += final_score
        count += 1

    average_score = round(total_score / count, 2) if count > 0 else 0

    return JsonResponse({
        "detailed_scores": results,
        "average_score": average_score
    })


@csrf_exempt
def save_report(request):
    if request.method == "POST":
        try:
            username = request.session.get("username")
            pdf_name = request.POST.get("pdf_name")
            score = request.POST.get("score")  # Match JS field

            if not username or not pdf_name or not score:
                return JsonResponse({"error": "Missing data."}, status=400)

            report_data = {
                "username": username,
                "pdf_name": pdf_name,
                "type": "pdf",
                "total_score": float(score),
                "report_saved": True,
                "created_at": timezone.now()
            }

            # Save the report to MongoDB
            report_collection.insert_one(report_data)

            return JsonResponse({"success": True, "message": "✅ Report saved successfully!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)






def view_answers(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method."}, status=405)

    username = request.session.get("username")
    pdf_name = request.GET.get("pdf_name")

    if not username or not pdf_name:
        return JsonResponse({"error": "Missing username or pdf_name"}, status=400)

    # Fetch user's submitted answers
    user_answer_doc = saved_useranswer.find_one({
        "username": username,
        "pdf_name": pdf_name
    })

    if not user_answer_doc or "answers" not in user_answer_doc:
        return JsonResponse({"error": "No answers found for this user and PDF."}, status=404)

    # Fetch correct questions from the latest saved_collection
    saved_doc = saved_collection.find_one(
        {"username": username, "pdf_name": pdf_name},
        sort=[('_id', -1)]  # Get latest document
    )

    if not saved_doc or "questions" not in saved_doc:
        return JsonResponse({"error": "No questions found for this user and PDF."}, status=404)

    correct_questions = saved_doc["questions"]
    user_answers = user_answer_doc["answers"]

    # Map question_id -> {question, correct_answer}
    correct_map = {
        q["question_id"]: {
            "question": q.get("question", ""),
            "correct_answer": q.get("answer", "")  # Correct key here
        }
        for q in correct_questions
    }

    # Compare user answers to correct ones
    answers_data = []
    for ans in user_answers:
        qid = ans.get("question_id")
        user_ans = ans.get("user_answer", "")

        if qid in correct_map:
            correct_q = correct_map[qid]
            accuracy = fuzz.ratio(user_ans.lower(), correct_q["correct_answer"].lower()) if correct_q["correct_answer"] else 0

            answers_data.append({
                "question_id": qid,
                "question": correct_q["question"],
                "user_answer": user_ans,
                "correct_answer": correct_q["correct_answer"],
                "accuracy": accuracy
            })

    return JsonResponse({"answers": answers_data})