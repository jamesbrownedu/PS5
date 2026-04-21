from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import PyPDF2
from bs4 import BeautifulSoup
import zipfile
import random

class MarkovChain:
    def __init__(self):
        self.chain = {}

    def train(self, text):
        words = text.lower().split()
        for i in range(len(words) - 1):
            word = words[i]
            next_word = words[i + 1]
            if word not in self.chain:
                self.chain[word] = []
            self.chain[word].append(next_word)

    def generate(self, start_word, length=50):
        start_word = start_word.lower()
        if start_word not in self.chain:
            return "Sorry, I don't have enough data to answer that."
        result = [start_word]
        current = start_word
        for _ in range(length - 1):
            if current in self.chain and self.chain[current]:
                next_word = random.choice(self.chain[current])
                result.append(next_word)
                current = next_word
            else:
                break
        return ' '.join(result)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = MarkovChain()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            text = process_file(filepath)
            if text.strip():
                model.train(text)
                message = "File processed and AI trained on the content."
            else:
                message = "No text extracted from the file."
            return render_template('index.html', message=message)
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question', '').strip()
    if not question:
        response = "Please ask a question."
    else:
        start_word = question.split()[0] if question.split() else "the"
        response = model.generate(start_word)
    return render_template('index.html', response=response)

def process_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    text = ""
    try:
        if ext == '.pdf':
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + " "
        elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
        elif ext == '.html':
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text()
        elif ext == '.zip':
            with zipfile.ZipFile(filepath, 'r') as z:
                for name in z.namelist():
                    if not name.endswith('/') and os.path.splitext(name)[1].lower() in ['.txt', '.py', '.js', '.html', '.md']:
                        with z.open(name) as f:
                            content = f.read().decode('utf-8', errors='ignore')
                            text += content + " "
        else:
            # Assume text file
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
    except Exception as e:
        text = f"Error processing file: {str(e)}"
    return text

if __name__ == '__main__':
    app.run(debug=True)