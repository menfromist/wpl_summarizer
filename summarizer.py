import requests
from bs4 import BeautifulSoup
from google.cloud import language_v1
from google.oauth2 import service_account
import os
import json

def get_credentials_from_env():
    # 환경 변수에서 JSON 문자열을 읽어와서 사전으로 변환
    json_credentials = os.getenv('GOOGLE_CLOUD_CREDENTIALS')
    if json_credentials is None:
        raise ValueError("환경 변수 'GOOGLE_CLOUD_CREDENTIALS'가 설정되지 않았습니다.")
    
    credentials_info = json.loads(json_credentials)
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    return credentials

def fetch_blog_text(blog_url):
    response = requests.get(blog_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    blog_text = ' '.join([para.text for para in paragraphs])
    return blog_text

def summarize_text_with_gemini(text, num_sentences=9):
    credentials = get_credentials_from_env()
    client = language_v1.LanguageServiceClient(credentials=credentials)

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_syntax(document=document)

    sentences = [sentence.text.content for sentence in response.sentences]
    summarized = sentences[:num_sentences]
    return summarized

def summarize_blog(blog_url, num_sentences=9):
    blog_text = fetch_blog_text(blog_url)
    summary = summarize_text_with_gemini(blog_text, num_sentences)
    return summary

if __name__ == '__main__':
    blog_url = input("Enter the blog URL: ")
    summary = summarize_blog(blog_url)
    for sentence in summary:
        print(sentence)
