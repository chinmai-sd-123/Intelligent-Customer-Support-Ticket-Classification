import re

URGENT_KEYWORDS = [
    "urgent", "asap", "immediately",
    "need this resolved today",
    "really frustrated",
    "not a scam",
    "this is unacceptable"
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text

def detect_urgency(text):
    text = text.lower()
    for k in URGENT_KEYWORDS:
        if k in text:
            return 1
    return 0

def assign_priority(category, urgency):
    if urgency == 1:
        return "High"
    if category in ["Payment", "Account"]:
        return "Medium"
    return "Low"

def route_department(category):
    routing = {
        "Payment": "Finance",
        "Refund": "Finance",
        "Technical": "Technical Support",
        "Account": "Customer Support",
        "Other": "Customer Support"
    }
    return routing.get(category, "Customer Support")


