import os
import cgi, cgitb  # cgi 프로그래밍 관련
import sys, codecs # 인코딩 관련
import string
from konlpy.tag import Okt
import torch
import torch.nn as nn
import numpy as np 
import joblib      # AI 모델 관련
import pickle  # 단어 사전 저장/불러오기 관련
from sklearn.feature_extraction.text import TfidfVectorizer  # TF-IDF 사용
from sklearn.metrics.pairwise import cosine_similarity  # 코사인 유사도 계산
import torch.nn.functional as F

SCRIPT_MODE = True    # Jupyter Mode : False, WEB Mode : True
cgitb.enable()         # Web상에서 진행상태 메시지를 콘솔에서 확인할수 있도록 하는 기능

def show_html(result):
    print("Content-Type: text/html; charset=utf-8")
    print(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Model Project</title>
    """)
    print("""
        <style>
            html {height: 100px;}
            body {height: 100vh; width:100vw;}
            body {background-color: rgb(252, 211, 211);}
            header {background-color: rgb(255,170,170);}
            #section_ml {display: inline-block; background-color: rgb(252, 211, 211); height: 85vh; width: 90vw; margin-left: 4%;}
            #title {text-align: center;}
            #content { text-align : center; margin-left: 26%; height: 60vh; width: 45vw;}
        </style>
    """)
    print(f"""
    </head>
    <body id = "body">
        <header id = "title">
            <h1>My Project Model</h1>
        </header>

        <div id = "section_ml" style="border:5px solid rgb(255,170,170)">
            
            <h2 id = "title">자연어 처리</h2>
            <h3 id = "title"> [ 낚시성 뉴스 기사 탐지 ] </h3>
            <img src="../image/nnews.png" style="width: 60px; height: 50px; margin-left: 48%;" >
            <hr>
            
            
            <br>
            <form id ="content">
                뉴스 기사
                <br>
                <textarea name = "news_article" rows = "30" cols="80"></textarea>

                <input type = "submit" value = "전송">
          
                <h3>{result}</h3>
                
            </form>
          
            
            
        </div>
          
        
        
    
    </body>
    </html>
    """)

# SentenceClassifier 모델 클래스 정의
class SentenceClassifier(nn.Module):
    def __init__(self, n_vocab, hidden_dim, embedding_dim, n_layers, dropout=0.5, bidirectional=True, model_type="lstm", pretrained_embedding=None):
        super(SentenceClassifier, self).__init__()
        if pretrained_embedding is not None:
            self.embedding = nn.Embedding.from_pretrained(
                torch.tensor(pretrained_embedding, dtype=torch.float32),
                padding_idx=0
            )
        else:
            self.embedding = nn.Embedding(
                num_embeddings=n_vocab,
                embedding_dim=embedding_dim,
                padding_idx=0
            )
        
        # LSTM 모델 사용
        self.model = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=n_layers,
            bidirectional=bidirectional,
            dropout=dropout,
            batch_first=True
        )

        if bidirectional:
            self.classifier = nn.Linear(hidden_dim * 2, 1)
        else:
            self.classifier = nn.Linear(hidden_dim, 1)
        
        self.dropout = nn.Dropout(dropout)

    def forward(self, inputs):
        embeddings = self.embedding(inputs)
        output, _ = self.model(embeddings)
        last_output = output[:, -1, :]
        last_output = self.dropout(last_output)
        logits = self.classifier(last_output)
        return logits

# 단어 사전 불러오기----------------------------------
def load_vocab(vocab_path):
    with open(vocab_path, 'rb') as f:
        token_to_id = pickle.load(f)
    return token_to_id

# 코사인 유사도를 계산하는 함수-----------------------------------------
def calculate_cosine_similarity(article_text, vocab_tokens):
    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer().fit(vocab_tokens + [article_text])
    
    # 기사와 단어 사전을 벡터로 변환
    article_vec = vectorizer.transform([article_text])
    vocab_vec = vectorizer.transform(vocab_tokens)

    # 코사인 유사도 계산
    similarity = cosine_similarity(article_vec, vocab_vec)
    
    # 유사도의 평균값 반환
    return np.mean(similarity)

# 사용자 입력 데이터를 예측하는 함수-----------------------------------------
def classify_article(article_text, vocab_tokens):
    
    # 기사와 단어 사전의 코사인 유사도 계산
    similarity = calculate_cosine_similarity(article_text, vocab_tokens)

    # 유사도가 60% 이상일 때 해당 주제와 관련 있다고 판단
    if similarity >= 0.6:
        return f"위에 작성한 기사는 IT & 과학 관련 뉴스가 맞습니다."
    else:
        return f"위에 작성한 기사는 IT & 과학 관련 뉴스가 아닙니다."

# 주제별 모델과 단어 사전 로딩 함수---------------------------------------
def load_model_and_vocab_for_category():

    if SCRIPT_MODE:
        model_path = os.path.dirname(__file__)+ '/model_nlp_news.pth' # 웹상에서는 절대경로만
        vocab_path = os.path.dirname(__file__)+ '/vocab.pkl'
    else:
        model_path = '../model_nlp_news.pth'
        vocab_path = '../vocab.pkl'
    

    if model_path and os.path.exists(model_path) and vocab_path and os.path.exists(vocab_path):
        # 모델 및 단어 사전 불러오기
        model = torch.load(model_path, map_location=torch.device('cpu'))
        token_to_id = load_vocab(vocab_path)
        return model, token_to_id
    else:
        raise FileNotFoundError(f"모델 또는 단어 사전을 찾을 수 없습니다.")

def calculate_cosine_similarity(article_text, vocab_tokens):
    # vocab_tokens가 사전일 경우, 값들만 리스트로 변환
    if isinstance(vocab_tokens, dict):
        vocab_tokens = list(vocab_tokens.values())  # 사전 값을 리스트로 변환

    # vocab_tokens 안에 정수형 값이 있을 경우, 문자열로 변환하거나 필터링
    vocab_tokens = [str(token) for token in vocab_tokens if isinstance(token, (str, int))]  # 문자열로 변환
    
    # article_text가 문자열인지 확인 (보통은 문자열이어야 함)
    if not isinstance(article_text, str):
        raise ValueError("article_text는 문자열이어야 합니다.")

    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer().fit(vocab_tokens + [article_text])
    
    # 기사와 단어 사전을 벡터로 변환
    article_vec = vectorizer.transform([article_text])
    vocab_vec = vectorizer.transform(vocab_tokens)

    # 코사인 유사도 계산
    similarity = cosine_similarity(article_vec, vocab_vec)
    
    # 유사도의 평균값 반환
    return np.mean(similarity)


# (1) WEB 인코딩 설정---------------------------------
if SCRIPT_MODE:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())  # 웹에서 utf-8 인코딩 설정

# (2) WEB 사용자 입력 데이터 처리------------------------
form = cgi.FieldStorage()
article_text = form.getvalue("news_article", "").strip()  # 뉴스 기사 텍스트 입력받기

try:

    model, vocab_tokens = load_model_and_vocab_for_category()
    
    # (4) 예측 및 결과 출력
    if len(article_text)>1:
        result = classify_article(article_text, vocab_tokens)
    else:
        result = "기사를 입력해주세요."

except Exception as e:
    result = f"오류가 발생했습니다: {str(e)}"

# (5) 사용자에게 WEB 화면 제공
show_html(result)
