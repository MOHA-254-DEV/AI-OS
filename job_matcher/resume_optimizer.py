# job_matcher/resume_optimizer.py
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text.lower())
    return [word for word in tokens if word not in stop_words]

def optimize_resume(resume_text, job_description):
    resume_words = set(clean_text(resume_text))
    job_keywords = set(clean_text(job_description))

    missing_keywords = job_keywords - resume_words
    enriched_resume = resume_text + "\n\nKEYWORDS: " + ", ".join(missing_keywords)

    return {
        "original_resume": resume_text,
        "optimized_resume": enriched_resume,
        "missing_keywords": list(missing_keywords)
    }
