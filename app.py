import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 디렉토리 존재 여부 확인 및 생성
def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    blog_url = request.form['url']
    file = request.files['file']

    # 파일 저장 경로 확인 및 디렉토리 생성
    ensure_directory_exists(app.config['UPLOAD_FOLDER'])

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # 블로그 내용 요약 (summarizer.py를 통해 호출)
    summarized_text = summarize_blog(blog_url)

    return render_template('review.html', text=summarized_text, image_path=file_path)

# summarizer.py의 summarize_blog 함수 호출 코드 (필요 시 수정)

if __name__ == '__main__':
    app.run(debug=True)
