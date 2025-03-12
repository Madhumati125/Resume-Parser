# Resume-Parser
Output of Resume-Parser
🔍 Parsing resume: data\resume.pdf

🔍 Parsing resume: data\resume2.pdf

📊 Final Results:

Resume: resume.pdf
Skills Found: {'Programming': ['python'], 'Data Science': ['machine learning', 'tensorflow', 'pandas', 'nlp'], 'Database': [], 'DevOps': ['docker']}
Skill Counts: {'Programming': 1, 'Data Science': 4, 'Database': 0, 'DevOps': 1}

Resume: resume2.pdf
Skills Found: {'Programming': ['python'], 'Data Science': ['machine learning', 'tensorflow', 'pandas', 'nlp'], 'Database': ['sql'], 'DevOps': ['docker']}
Skill Counts: {'Programming': 1, 'Data Science': 4, 'Database': 1, 'DevOps': 1}

✅ Results saved to 'results.json'

Output of Resume-Parser Using Flask
![resume](https://github.com/user-attachments/assets/5ae7dad8-2ea4-4f08-affe-771b8c39cb0f)
![resume2](https://github.com/user-attachments/assets/7e560e27-b29a-4724-b9ac-18453b69426a)

Output from Resume-Parser
File: resume.docx
Matched Skills: ['Python', 'Python', 'Machine Learning']
TF-IDF Scores: {'Python': 0.3922322702763681, 'Machine Learning': 0}
----------------------------------------
File: resume2.docx
Matched Skills: ['Python', 'Python', 'Machine Learning']
TF-IDF Scores: {'Python': 0.32025630761017426, 'Machine Learning': 0}
----------------------------------------

Output using shutil
In resume_results.txt:
NLP: 2
Python: 5
Machine Learning: 3

In resume2_results.txt:
NLP: 2
Python: 6
Machine Learning: 3

And in console:
Job Skills: ['Python', 'Machine Learning', 'NLP', 'Flask', 'Django', 'SpaCy']

Processing: resume.pdf
Skills Found:
NLP: 2
Python: 5
Machine Learning: 3

Processing: resume2.pdf
Skills Found:
NLP: 2
Python: 6
Machine Learning: 3

✅ Resume Parsing Complete!
