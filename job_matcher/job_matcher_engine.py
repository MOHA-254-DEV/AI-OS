# job_matcher/job_matcher_engine.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs_to_resume(resume, job_listings):
    documents = [resume] + [job['description'] for job in job_listings]
    tfidf = TfidfVectorizer().fit_transform(documents)

    similarity_matrix = cosine_similarity(tfidf[0:1], tfidf[1:])
    ranked_jobs = sorted(zip(job_listings, similarity_matrix[0]), key=lambda x: x[1], reverse=True)

    return [
        {
            "title": job["title"],
            "description": job["description"],
            "url": job.get("url", "N/A"),
            "match_score": float(score)
        } for job, score in ranked_jobs
    ]
