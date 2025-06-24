# feedback_loop/test_feedback.py

from feedback_collector import collect_feedback
from trainer import print_diff_summary

resume = """
John Smith
Python Developer
Experience with Django, Flask
"""

corrected_resume = """
John Smith
Senior Python Developer
Experience with Django, Flask, FastAPI
"""

# Step 1: Collect correction
collect_feedback(resume, corrected_resume, "resume")

# Step 2: View summary
print_diff_summary()
