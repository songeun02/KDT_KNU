import os
import cgi, cgitb  # cgi 프로그래밍 관련
import sys, codecs # 인코딩 관련
import torch
import torch.nn as nn
import numpy as np 
import pickle  # 단어 사전 저장/불러오기 관련
import torch.nn.functional as F

# 동작관련 전역 변수----------------------------------
SCRIPT_MODE = True    # Jupyter Mode : False, WEB Mode : True
cgitb.enable()         # Web상에서 진행상태 메시지를 콘솔에서 확인할수 있도록 하는 기능

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# HTML 출력 함수----------------------------------------
def showHTML(msg):
    print("Content-Type: text/html; charset=utf-8")
    print(f"""
    <!DOCTYPE html>
    <html lang="en">
     <head>
      <meta charset="UTF-8">
      <title>뉴스 기사 주제 분류</title>
      <style>
        .container {{
            margin-top: 20px;
        }}
        textarea {{
            width: 100%;
            height: 200px;
        }}
        select {{
            margin-top: 10px;
        }}
      </style>
     </head>
     <body>
      <div class="container">
        <h2>뉴스 기사 주제 분류</h2>
        <form enctype="multipart/form-data" method="post">
          <p>뉴스 기사 입력:</p>
          <textarea name="article" placeholder="여기에 뉴스 기사를 붙여넣으세요"></textarea>
          <p>주제 선택:</p>
          <select name="category">
            <option value="경제">경제</option>
            <option value="생활&문화">생활&문화</option>
            <option value="IT&과학">IT&과학</option>
            <option value="정치">정치</option>
          </select>
          <p><input type="submit" value="분류하기"></p>
          <p>{msg}</p>
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
def classify_article(article_text, selected_category, model, vocab_tokens):
    if not article_text.strip():
        return "기사를 입력해주세요."

    prob = predict_article_category(article_text, model, vocab_tokens)

    if prob >= 0.4:
        return f"'{selected_category}' 주제의 낚시성 기사일 확률이 {prob * 100:.2f}%입니다."
    else:
        return f"'{selected_category}' 주제의 낚시성 기사가 아닐 확률이 {100 - prob * 100:.2f}%입니다."



# 주제별 모델과 단어 사전 로딩 함수---------------------------------------
def load_model_and_vocab_for_category(category):
    model_paths = {
        "경제": "/absolute/path/to/economy_model.pth",
        "생활&문화": "/absolute/path/to/life_model.pth",
        "IT&과학": r"C:\Users\sh321\Desktop\KDT\NLP\cgi-bin\models\loss_0.548_score0.760.pth",
        "정치": "/absolute/path/to/politics_model.pth"
    }

    vocab_paths = {
        "경제": "/absolute/path/to/economy_vocab.pkl",
        "생활&문화": "/absolute/path/to/life_vocab.pth",
        "IT&과학": r"C:\Users\sh321\Desktop\KDT\NLP\cgi-bin\wordDict\vocab.pkl",
        "정치": "/absolute/path/to/politics_vocab.pkl"
    }
    
    model_path = model_paths.get(category)
    vocab_path = vocab_paths.get(category)

    if model_path and os.path.exists(model_path) and vocab_path and os.path.exists(vocab_path):
        # 모델 및 단어 사전 불러오기
        model = torch.load(model_path, map_location=device, weights_only=False) 
        model.to(device) 
        token_to_id = load_vocab(vocab_path)
        return model, token_to_id
    else:
        raise FileNotFoundError(f"{category} 모델 또는 단어 사전을 찾을 수 없습니다. \n{model_path}, \n{vocab_path}, \n{os.path.exists(model_path)} \n{os.path.exists(vocab_path)}" )


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
article_text = form.getfirst("article", "").strip()  # 뉴스 기사 텍스트 입력받기
selected_category = form.getfirst("category", "")  # 선택된 주제

try:
    # (3) 선택된 주제에 맞는 모델과 단어 사전 로딩
    if selected_category:
        model, vocab_tokens = load_model_and_vocab_for_category(selected_category)
    else:
        model, vocab_tokens = None, None

    # (4) 예측 및 결과 출력
    if article_text and selected_category and model:
        result = classify_article(article_text, selected_category, model, vocab_tokens)
    else:
        result = "기사를 입력하고 주제를 선택해주세요."

except Exception as e:
    result = f"오류가 발생했습니다: {str(e)}"

# (5) 사용자에게 WEB 화면 제공
showHTML(result)
