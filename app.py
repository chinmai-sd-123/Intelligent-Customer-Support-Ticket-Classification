from flask import Flask, render_template, request,jsonify

import joblib
from scipy.sparse import hstack
from utils import clean_text,detect_urgency,route_department,assign_priority

app = Flask(__name__)

# loading model

svm = joblib.load("models/svm.pkl")
tfidf_word = joblib.load("models/tfidf_word.pkl")
tfidf_char=joblib.load("models/tfidf_char.pkl")
label_encoder=joblib.load("models/label_encoder.pkl")

@app.route('/',methods=['GET','POST'])
def home():
    result=None
    ticket_text=""
    if request.method=='POST':
        ticket_text=request.form['ticket']
        cleaned=clean_text(ticket_text)
        X_word=tfidf_word.transform([cleaned])
        X_char=tfidf_char.transform([cleaned])
        X=hstack((X_word,X_char))

        cat_idx=svm.predict(X)
        category=label_encoder.inverse_transform(cat_idx)[0]

        urgency_value=detect_urgency(ticket_text)
        urgency="urgent" if urgency_value == 1 else "normal"

        priority=assign_priority(category,urgency_value)
        department=route_department(category)

        result={
            'category':category,
            'urgency':urgency,
            'priority':priority,
            'department':department
        }
    return render_template(
        "index.html",
        result=result,
        ticket=ticket_text,
    )

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "ticket" not in data:
        return jsonify({
            'error': 'ticket text missing'
        }),400
    ticket=data["ticket"].strip()

    if ticket =="":
        return jsonify({
            'error': 'ticket text missing'}), 400

    # 1. clean text
    cleaned=clean_text(ticket)
     # 2. vectorize
    X_word=tfidf_word.transform([cleaned])
    X_char=tfidf_char.transform([cleaned])
    X=hstack([X_word,X_char])

    # 3.Predict category
    cat_idx=svm.predict(X)
    category=label_encoder.inverse_transform(cat_idx)[0]


    #4.urgency
    urgency_value=detect_urgency(ticket)
    urgency="urgent" if urgency_value==1 else "normal"

    #5. priority
    priority=assign_priority(category,urgency)

    # 6.Department
    department=route_department(category)

    return jsonify({
        "category": category,
        "urgency": urgency,
        "priority": priority,
        "department": department,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




