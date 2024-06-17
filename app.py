from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import summarizer
import image_generator

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    blog_url = request.form['blog_url']
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        summarized_text = summarizer.summarize_blog(blog_url)
        return render_template('review.html', summarized_text=summarized_text, image_url=file_path)
    return redirect(request.url)

@app.route('/generate', methods=['POST'])
def generate_image():
    image_url = request.form['image_url']
    texts = request.form.getlist('texts')
    images = image_generator.generate_images(image_url, texts)
    return render_template('result.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
