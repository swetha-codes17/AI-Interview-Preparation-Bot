from flask import Flask, render_template, request,session
import random
from groq import Groq
import re
app = Flask(__name__)
client = Groq(api_key="GROQ_API_KEY")
app.secret_key = "interviewbot123"
python_questions = {
    "Easy": [
        "What is Python?",
        "What are variables in Python?",
        "What is a list?",
        "What is a tuple?",
        "What is a dictionary?",
        "What is a function?",
        "What is an if statement?"
    ],

    "Intermediate": [
        "Difference between list and tuple?",
        "What is list comprehension?",
        "What is exception handling?",
        "What is a lambda function?",
        "What are modules in Python?",
        "What is OOP?",
        "Explain inheritance."
    ],

    "Advanced": [
        "What is multithreading?",
        "Difference between process and thread?",
        "What are decorators?",
        "What are generators?",
        "Explain GIL in Python.",
        "What is method resolution order?",
        "Explain context managers."
    ]
}


sql_questions = {
    "Easy": [
        "What is SQL?",
        "What is a database?",
        "What is a table?",
        "What is a primary key?",
        "What is a foreign key?",
        "What is SELECT statement?",
        "What is WHERE clause?"
    ],

    "Intermediate": [
        "Difference between DELETE and TRUNCATE?",
        "What is JOIN?",
        "Types of JOINs?",
        "What is GROUP BY?",
        "What is HAVING clause?",
        "What is normalization?",
        "Difference between WHERE and HAVING?"
    ],

    "Advanced": [
        "What are stored procedures?",
        "What are triggers?",
        "What is indexing?",
        "What is a view?",
        "What is transaction management?",
        "Explain ACID properties.",
        "What is query optimization?"
    ]
}

web_questions = {
    "Easy": [
        "What is HTML?",
        "What is CSS?",
        "What is JavaScript?",
        "What is a hyperlink?",
        "What is a form?",
        "What is responsive design?",
        "What is Bootstrap?"
    ],

    "Intermediate": [
        "Difference between id and class?",
        "What is Flexbox?",
        "What is Grid?",
        "What is DOM?",
        "What is event handling?",
        "Difference between inline and block elements?",
        "What is localStorage?"
    ],

    "Advanced": [
        "What is REST API?",
        "What is JWT authentication?",
        "What is CORS?",
        "What is asynchronous JavaScript?",
        "What is event bubbling?",
        "Difference between session and cookies?",
        "What is virtual DOM?"
    ]
}
datascience_questions = {
    "Easy": [
        "What is Data Science?",
        "What is Machine Learning?",
        "What is AI?",
        "What is a dataset?",
        "What is data cleaning?",
        "What is supervised learning?",
        "What is unsupervised learning?"
    ],

    "Intermediate": [
        "Difference between AI and ML?",
        "What is feature engineering?",
        "What is overfitting?",
        "What is underfitting?",
        "What is train-test split?",
        "What is regression?",
        "What is classification?"
    ],

    "Advanced": [
        "What is cross validation?",
        "What is gradient descent?",
        "What is deep learning?",
        "What is a neural network?",
        "What is precision and recall?",
        "What is confusion matrix?",
        "What is hyperparameter tuning?"
    ]
}
@app.route("/", methods=["GET", "POST"])
def home():

    question = ""

    if request.method == "POST":
        domain = request.form["domain"]
        level = request.form["level"]
        session["question_no"] = 1
        session["total_score"] = 0
        session["asked_questions"] = []
        session["current_question"] = ""
        session["domain"] = domain
        session["level"] = level
        domain = request.form["domain"]
        level = request.form["level"]

        if domain == "Python":
            available_questions = [
              q for q in python_questions[level]
              if q not in session["asked_questions"]
    ]
            question = random.choice(available_questions)
            session["asked_questions"].append(question)
            session["current_question"] = question

        elif domain == "SQL":
            available_questions = [
               q for q in sql_questions[level]
               if q not in session["asked_questions"]
    ]
            question = random.choice(available_questions)
            session["asked_questions"].append(question)
            session["current_question"] = question

        elif domain == "Web Development":
            available_questions = [
               q for q in web_questions[level]
               if q not in session["asked_questions"]
    ]
            question = random.choice(available_questions)
            session["asked_questions"].append(question)
            session["current_question"] = question
        elif domain == "Data Science":
            available_questions = [
               q for q in datascience_questions[level]
               if q not in session["asked_questions"]
    ]
            question = random.choice(available_questions)
            session["asked_questions"].append(question)
            session["current_question"] = question

        return render_template("question.html", question=question,domain=domain,level=level,question_no=session["question_no"])
    return render_template("index.html")
@app.route("/submit_answer", methods=["POST"])
def submit_answer():

    answer = request.form["answer"]
    score = 0
    prompt = f"""
You are a strict technical interviewer.
Question:
{session["current_question"]}
Candidate Answer:
{answer}
Rules:
-Completely wrong answer = 0-2
-Partially correct answer = 3-5
Mostly correct answer = 6-8
Perfect answer = 9-10
Be very strict.
Give output in exactly this format:
Score: <number out of 10>
Feedback: <maximum 1 sentence only>
"""

    response = client.chat.completions.create(
      model="llama-3.1-8b-instant",
      messages=[
        {"role": "user", "content": prompt}
    ]
)

    ai_result = response.choices[0].message.content
    print(ai_result)

    match = re.search(r"Score:\s*(\d+)", ai_result)

    if match:
        score = int(match.group(1))
    else:
        score = 5
    feedback = ai_result
    session["total_score"] += score
    session["question_no"] += 1
    if session["question_no"] <= 5:
       domain = session["domain"]
       level = session["level"]
       if domain == "Python":
          available_questions = [
              q for q in python_questions[level]
              if q not in session["asked_questions"]
    ]
          question = random.choice(available_questions)
          session["asked_questions"].append(question)
          session["current_question"] = question

       elif domain == "SQL":
          available_questions = [
               q for q in sql_questions[level]
               if q not in session["asked_questions"]
    ]
          question = random.choice(available_questions)
          session["asked_questions"].append(question)
          session["current_question"] = question

       elif domain == "Web Development":
           available_questions = [
               q for q in web_questions[level]
               if q not in session["asked_questions"]
    ]
           question = random.choice(available_questions)
           session["asked_questions"].append(question)
           session["current_question"] = question
       elif domain == "Data Science":
          available_questions = [
               q for q in datascience_questions[level]
               if q not in session["asked_questions"]
    ]
          question = random.choice(available_questions)
          session["asked_questions"].append(question)
          session["current_question"] = question
       #QUESTION PAGE
       print("Asked Questions:",session["asked_questions"])
       print("Next Question:",question)
       return render_template(
            "question.html",question=question,domain=domain,level=level,question_no = session["question_no"]
          )
    total_score = session["total_score"] 
    readiness =   (total_score / 50) * 100
    
    strengths = []
    weaknesses = []

    if readiness >= 80:
        badge = "🏆 Interview Master"
    elif readiness >= 60:
        badge = "🥈 Rising Talent"
    else:
        badge = "📚 Learner"
    if readiness >= 80:
       strengths = [
        "Strong Python fundamentals",
        "Good problem solving",
        "Confident interview performance"
    ]

       weaknesses = [
        "Practice advanced concepts"
    ]

    elif readiness >= 60:
       strengths = [
        "Good understanding of basics",
        "Can answer common questions"
    ]

       weaknesses = [
        "Need more coding practice",
        "Improve confidence"
    ]

    else:
       strengths = [
        "Attempted all questions"
    ]

       weaknesses = [
        "Need stronger Python basics",
        "Improve interview answers",
        "Practice coding regularly"
    ]
    
    return render_template(
      "result.html",
       total_score = total_score,
       readiness=round(readiness,2),
       strengths=strengths,
       weaknesses=weaknesses,
       feedback=feedback,
       badge=badge,
       domain = session["domain"],
       level = session["level"]
       )
if __name__ == "__main__":
    app.run(debug=True)
