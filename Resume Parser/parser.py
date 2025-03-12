import os
import shutil
import spacy
from spacy.matcher import PhraseMatcher
from docx import Document
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define file paths
RESUME_DIR = './data/resumes'
JOB_DESCRIPTION_FILE = './data/job_description.txt'
OUTPUT_DIR = './output'

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Load job description and extract skills
with open(JOB_DESCRIPTION_FILE, 'r') as file:
    job_description = file.read()

skills = [line.strip() for line in job_description.split('\n') if line.strip().startswith('-')]
skills = [skill.replace('-', '').strip() for skill in skills]

# Initialize PhraseMatcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp(skill) for skill in skills]
for pattern in patterns:
    matcher.add("SKILL", [pattern])


# Function to read resume text
def read_resume(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


# Process resumes
results = []
for filename in os.listdir(RESUME_DIR):
    if filename.endswith('.docx'):
        file_path = os.path.join(RESUME_DIR, filename)
        text = read_resume(file_path)
        doc = nlp(text)

        # Match skills using PhraseMatcher
        matched_skills = []
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            matched_skills.append(span.text)

        # Fuzzy matching
        for skill in skills:
            if any(fuzz.partial_ratio(skill.lower(), ms.lower()) > 80 for ms in matched_skills):
                if skill not in matched_skills:
                    matched_skills.append(skill)

        # TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = {feature_names[i]: tfidf_matrix[0, i] for i in range(len(feature_names))}

        # Filter scores for relevant skills
        skill_scores = {skill: tfidf_scores.get(skill.lower(), 0) for skill in matched_skills}

        # Save result
        result = {
            'file': filename,
            'matched_skills': matched_skills,
            'tfidf_scores': skill_scores
        }
        results.append(result)

        # Copy resume to output folder
        shutil.copy(file_path, os.path.join(OUTPUT_DIR, filename))

# Display Results
for result in results:
    print(f"File: {result['file']}")
    print(f"Matched Skills: {result['matched_skills']}")
    print(f"TF-IDF Scores: {result['tfidf_scores']}")
    print('-' * 40)
