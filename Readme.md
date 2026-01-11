# Intelligent Customer Support Ticket Classification System

> An end-to-end Machine Learning system that automatically classifies customer support tickets, detects urgency, assigns priority, and routes them to the correct department.

Built using classical NLP + ML (no deep learning) and deployed as a Flask web application with a clean frontend.

## 1. Project Overview

Customer support teams receive a large volume of unstructured text tickets every day. Manually triaging these tickets is slow, inconsistent, and error-prone.

This project solves that problem by:
- Classifying tickets into meaningful categories
- Detecting urgency signals from text
- Assigning business priority
- Routing tickets to the appropriate department
- Providing both an API and a web interface

The system is designed to be interpretable, efficient, and production-ready.

## 2. Features

- **Text Classification**: Categorizes tickets into Payment, Refund, Account, Technical, or Other.
- **Urgency Detection**: Uses rule-based NLP signals to identify urgent requests.
- **Priority Assignment**: Automatically assigns business priority based on urgency and category.
- **Department Routing**: Routes tickets to Finance, Technical Support, or Customer Support.
- **Robustness**: Handles noisy and obfuscated text (e.g., typos, "p@ym3nt").
- **Interface**: Includes a Flask REST API and a simple HTML/CSS frontend.
- **Deployment**: Ready for deployment on platforms like Render.

## 3. Tech Stack

### Language & ML
- **Python**
- **Scikit-learn**: Logistic Regression, Linear SVM, Multinomial Naive Bayes
- **NLP**: TF-IDF (word n-grams), TF-IDF (character n-grams), Sparse feature stacking

### Backend & Frontend
- **Flask**: Web framework
- **Gunicorn**: Production server
- **HTML/CSS**: Frontend interface (no frameworks)

### Deployment
- **Render**: Cloud hosting platform

## 4. Dataset

- **Source**: Custom synthetic dataset (500+ samples) generated from realistic ticket templates.
- **Noise Injection**: Includes urgent phrases, obfuscated characters (e.g., `p@ym3nt`, `0rd3r`), and mixed casing.
- **Balance**: Balanced across categories to simulate real-world behavior and avoid data leakage.

## 5. Feature Engineering

- **Word-level TF-IDF**: Unigrams + bigrams to capture semantic meaning.
- **Character-level TF-IDF**: 3–5 character n-grams to handle spelling mistakes, obfuscation, and typos.

> **Why no stemming or stopword removal?**
> Character n-grams naturally handle noise. Removing stopwords was found to reduce signal quality, so raw text is kept for improved robustness.

## 6. Model Training & Evaluation

Multiple classical ML models were evaluated:

| Model | Macro F1 Score | Status |
|-------|----------------|--------|
| Logistic Regression | ~0.79 | |
| **Linear SVM** | **~0.83** | **Selected** |
| Multinomial Naive Bayes | ~0.64 | |

**Additional Checks:**
- Stratified train-test split
- Label shuffling test to detect leakage
- Error analysis on misclassified samples

*Final model selection was based on generalization, not just accuracy.*

## 7. Business Logic Layer

This logic is intentionally kept outside the ML model for transparency and maintainability.

- **Urgency Detection**: Rule-based detection using phrases like "urgent", "asap", "immediately", "need this resolved today".
- **Priority Assignment**:
    - Urgent tickets → **High**
    - Payment / Account issues → **Medium**
    - Others → **Low**
- **Department Routing**:
    - Payment / Refund → **Finance**
    - Technical → **Technical Support**
    - Account / Other → **Customer Support**

## 8. Application Architecture

```mermaid
graph TD
    A[User Input] --> B[Text Cleaning]
    B --> C[TF-IDF (word + char)]
    C --> D[ML Category Prediction]
    D --> E[Urgency Detection]
    E --> F[Priority Assignment]
    F --> G[Department Routing]
    G --> H[JSON / UI Response]
```

## 9. API Usage

### Endpoint
`POST /predict`

### Request Body
```json
{
  "ticket": "Payment was deducted but the app crashed urgently"
}
```

### Response
```json
{
  "category": "Payment",
  "urgency": "urgent",
  "priority": "High",
  "department": "Finance"
}
```

## 10. Web Interface

- Simple form-based UI for manual ticket entry.
- Displays classification results instantly.
- Built using Flask `render_template`, HTML, and CSS.

## 11. Deployment

The application is deployed on Render.

- **Live URL**: [click here](https://intelligent-customer-support-ticket.onrender.com/)
- **Server**: Gunicorn

## 12. Project Structure

```
customer_support_classification/
│
├── app.py
├── utils.py
├── requirements.txt
│
├── models/
│   ├── lr.pkl
│   ├── svm.pkl
│   ├── tfidf_word.pkl
│   ├── tfidf_char.pkl
│   └── label_encoder.pkl
│
├── templates/
│   └── index.html
│
└── static/
    └── styles.css
```

## 13. How to Run Locally

```bash
# Clone the repository
git clone https://github.com/chinmai-sd-123/Intelligent-Customer-Support-Ticket-Classification.git
cd customer_support_classification

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open your browser and navigate to: `http://127.0.0.1:5000`

## 14. Key Learnings

- Classical ML can outperform deep learning on small, noisy datasets.
- Character-level features are powerful for real-world text.
- Separating ML and business logic improves system design.
- Data leakage detection is critical.
- End-to-end deployment matters more than model complexity.

## 15. Future Improvements

- [ ] Confidence score output
- [ ] Database integration for ticket storage
- [ ] Authentication and role-based access
- [ ] Dockerization
- [ ] Monitoring and logging