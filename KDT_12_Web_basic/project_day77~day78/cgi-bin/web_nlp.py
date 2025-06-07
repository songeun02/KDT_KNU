import os
import cgi, cgitb  # cgi 프로그래밍 관련
import sys, codecs # 인코딩 관련
import torch
import torch.nn as nn
import numpy as np 
import pickle  # 단어 사전 저장/불러오기 관련
import torch.nn.functional as F

SCRIPT_MODE = True    # Jupyter Mode : False, WEB Mode : True
cgitb.enable()         # Web상에서 진행상태 메시지를 콘솔에서 확인할수 있도록 하는 기능

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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
            #section_nlp {display: inline-block; background-color: rgb(252, 211, 211); height: 85vh; width: 90vw; margin-left: 4%;}
            #title {text-align: center;}
            #content{ display : flex; align-items : flex-start; gap : 20px; margin-top : 7px; margin-left : 10%}
            #result_box{flex:1; margin-top:10px}
            #text_input{flex:1;}
        </style>
    """)
    print(f"""
    </head>
    <body id = "body">
        <header id = "title">
            <h1>My Project Model</h1>
        </header>

        <div id = "section_nlp" style="border:5px solid rgb(255,170,170)">
            
            <h2 id = "title">자연어 처리</h2>
            <h3 id = "title"> [ 낚시성 뉴스 기사 탐지 ] </h3>
            <img src="../image/nnews.png" style="width: 60px; height: 50px; margin-left: 48%;" >
            <hr>
            
            
            <br>
            <form id ="content">
                <div id = "text_input">
          
                    뉴스 기사
                    <br>
                    
                    <textarea name = "news_article" rows = "25" cols="80"></textarea>

                    <input type = "submit" value = "전송">
                </div>
          
                <div id = "result_box">
          
                    <h3>{result}</h3>

                </div>
                
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


# 사용자 입력 데이터를 예측하는 함수-----------------------------------------
def classify_article(article_text, model, vocab_tokens):
    if not article_text.strip():
        return "기사를 입력해주세요."

    prob = predict_article_category(article_text, model, vocab_tokens)

    if prob >= 0.4:
        return f"'IT & 과학'주제의 낚시성 기사일 확률이 {prob * 100:.2f}%입니다."
    else:
        return f"'IT & 과학' 주제의 낚시성 기사가 아닐 확률이 {100 - prob * 100:.2f}%입니다."

# 주제별 모델과 단어 사전 로딩 함수---------------------------------------
def load_model_and_vocab_for_category():

    if SCRIPT_MODE:
        model_path = os.path.dirname(__file__)+ '/model_run_file/model_nlp_news.pth' # 웹상에서는 절대경로만
        vocab_path = os.path.dirname(__file__)+ '/model_run_file/vocab.pkl'
    else:
        model_path = './model_run_file/model_nlp_news.pth'
        vocab_path = './model_run_file/vocab.pkl'
    

    if model_path and os.path.exists(model_path) and vocab_path and os.path.exists(vocab_path):
        # 모델 및 단어 사전 불러오기
        model = torch.load(model_path, map_location=device, weights_only=False)
        model.to(device)
        token_to_id = load_vocab(vocab_path)
        return model, token_to_id
    else:
        raise FileNotFoundError(f"모델 또는 단어 사전을 찾을 수 없습니다.")

def predict_article_category(article_text, model, token_to_id):
    model.eval()
    tokens = article_text.strip().split()
    indexed = [token_to_id.get(token, token_to_id.get('<unk>', 0)) for token in tokens]
    indexed_tensor = torch.tensor([indexed], dtype=torch.long).to(device)

    with torch.no_grad():
        logits = model(indexed_tensor)
        prob = torch.sigmoid(logits).item()  # 이진 분류일 경우 sigmoid 사용

    return prob

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
        result = classify_article(article_text, model, vocab_tokens)
    else:
        result = "기사를 입력해주세요."

except Exception as e:
    result = f"오류가 발생했습니다: {str(e)}"

# (5) 사용자에게 WEB 화면 제공
show_html(result)