import os
import shutil
import spacy
from spacy.matcher import PhraseMatcher
import pdfplumber
from fuzzywuzzy import fuzz, process

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# File paths
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
JOB_DESCRIPTION_FILE = 'job_description.txt'

# Load job description skills
with open(JOB_DESCRIPTION_FILE, 'r') as file:
    job_description = file.read()

# Extract skills from job description
job_skills = [line.strip('- ').strip() for line in job_description.split('\n') if line.startswith('-')]
print(f"Job Skills: {job_skills}")

# Initialize PhraseMatcher
matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp(skill) for skill in job_skills]
for pattern in patterns:
    matcher.add(pattern.text, [pattern])

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

# Function to parse and match skills
def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)
    doc = nlp(text)

    # Exact matches using PhraseMatcher
    matches = matcher(doc)
    extracted_skills = [doc[start:end].text for match_id, start, end in matches]

    # Fuzzy matches using fuzzywuzzy
    fuzzy_skills = []
    for word in text.split():
        match, score = process.extractOne(word, job_skills)
        if score > 80:
            fuzzy_skills.append(match)

    # Combine and count skills
    all_skills = extracted_skills + fuzzy_skills
    skills_count = {skill: all_skills.count(skill) for skill in set(all_skills)}

    return skills_count

# Create output folder if not exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Process each resume
for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith('.pdf'):
        file_path = os.path.join(INPUT_FOLDER, filename)
        print(f"\nProcessing: {filename}")

        # Parse resume and count skills
        skills_count = parse_resume(file_path)

        # Print output
        print("Skills Found:")
        for skill, count in skills_count.items():
            print(f"{skill}: {count}")

        # Save results
        output_file = os.path.join(OUTPUT_FOLDER, f"{filename.replace('.pdf', '')}_results.txt")
        with open(output_file, 'w') as f:
            for skill, count in skills_count.items():
                f.write(f"{skill}: {count}\n")

        # Move processed file to output
        shutil.move(file_path, os.path.join(OUTPUT_FOLDER, filename))

print("\n✅ Resume Parsing Complete!")
