import os
import json
import pdfplumber
import spacy
from spacy.matcher import PhraseMatcher

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


# Function to extract skills from resume text
def extract_skills(text, matcher):
    doc = nlp(text.lower())
    matches = matcher(doc)
    extracted_skills = {category: [] for category in skills_data.keys()}

    for match_id, start, end in matches:
        category = nlp.vocab.strings[match_id]
        skill = doc[start:end].text
        if skill not in extracted_skills[category]:
            extracted_skills[category].append(skill)

    return extracted_skills


# Function to count occurrences of skills
def count_skills(extracted_skills):
    skill_counts = {category: len(skills) for category, skills in extracted_skills.items()}
    return skill_counts


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

    # Store results
    results.append({
        'resume': os.path.basename(resume),
        'extracted_skills': extracted_skills,
        'skill_counts': skill_counts
    })

# Display final results
print("\n📊 Final Results:")
for result in results:
    print(f"\nResume: {result['resume']}")
    print(f"Skills Found: {result['extracted_skills']}")
    print(f"Skill Counts: {result['skill_counts']}")

# Output results as JSON
with open('results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("\n✅ Results saved to 'results.json'")
