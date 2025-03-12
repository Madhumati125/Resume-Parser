from flask import Flask, request, render_template, jsonify
import os
from main import extract_text_from_pdf, extract_skills, count_skills, extract_experience_and_education, matcher

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Extract text and skills
        text = extract_text_from_pdf(filepath)
        extracted_skills = extract_skills(text, matcher)
        skill_counts = count_skills(extracted_skills)
        experience, education = extract_experience_and_education(text)

        result = {
            'resume': file.filename,
            'extracted_skills': extracted_skills,
            'skill_counts': skill_counts,
            'experience': experience,
            'education': education
        }

        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
