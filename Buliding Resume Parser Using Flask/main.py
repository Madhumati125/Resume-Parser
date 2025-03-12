import os
import json
import pdfplumber
import spacy
from spacy.matcher import PhraseMatcher
from fuzzywuzzy import process
import re

# Load Spacy NLP model
nlp = spacy.load("en_core_web_sm")

# Load skills from skills.json
with open('skills.json', 'r') as f:
    skills_data = json.load(f)


# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text


# Function to create PhraseMatcher patterns
def create_matcher(skills_data):
    matcher = PhraseMatcher(nlp.vocab)
    for category, skills in skills_data.items():
        patterns = [nlp(skill.lower()) for skill in skills]
        matcher.add(category, patterns)
    return matcher


# Function to extract skills using PhraseMatcher and Fuzzy Matching
def extract_skills(text, matcher):
    doc = nlp(text.lower())
    matches = matcher(doc)
    extracted_skills = {category: [] for category in skills_data.keys()}

    # Exact matching using PhraseMatcher
    for match_id, start, end in matches:
        category = nlp.vocab.strings[match_id]
        skill = doc[start:end].text
        if skill not in extracted_skills[category]:
            extracted_skills[category].append(skill)

    # Fuzzy matching
    for category, skills in skills_data.items():
        for token in doc:
            matched_skill, score = process.extractOne(token.text, skills)
            if score > 85 and matched_skill not in extracted_skills[category]:
                extracted_skills[category].append(matched_skill)

    return extracted_skills


# Function to count occurrences of skills
def count_skills(extracted_skills):
    skill_counts = {category: len(skills) for category, skills in extracted_skills.items()}
    return skill_counts


# Function to extract experience and education
def extract_experience_and_education(text):
    experience_pattern = r'(\d+)\s+(years|months)\s+(of experience|experience)'
    education_pattern = r'(B\.?Sc|M\.?Sc|Bachelor|Master|PhD|Diploma|Degree)'

    experience = re.findall(experience_pattern, text)
    education = re.findall(education_pattern, text)

    total_experience = sum(int(exp[0]) for exp in experience) if experience else 0
    degrees = list(set(edu for edu in education))

    return total_experience, degrees


# Load job description
with open('job_description.txt', 'r') as f:
    job_description = f.read()

# Create PhraseMatcher
matcher = create_matcher(skills_data)

# Path to resumes
resume_dir = 'data'
resumes = [os.path.join(resume_dir, f) for f in os.listdir(resume_dir) if f.endswith('.pdf')]

results = []
for resume in resumes:
    print(f"\n🔍 Parsing resume: {resume}")

    # Extract text from resume
    text = extract_text_from_pdf(resume)

    # Extract skills
    extracted_skills = extract_skills(text, matcher)

    # Count skills
    skill_counts = count_skills(extracted_skills)

    # Extract experience and education
    experience, education = extract_experience_and_education(text)

    # Store results
    results.append({
        'resume': os.path.basename(resume),
        'extracted_skills': extracted_skills,
        'skill_counts': skill_counts,
        'experience': experience,
        'education': education
    })

# Output results as JSON
with open('results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("\n✅ Results saved to 'results.json'")
