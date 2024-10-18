import joblib      # AI 모델 관련
import os
import cgi, cgitb  # cgi 프로그래밍 관련
import sys, codecs # 인코딩 관련
from joblib import load
import pandas as pd
import numpy as np

# 동작관련 전역 변수----------------------------------
SCRIPT_MODE = True    # Jupyter Mode : False, WEB Mode : True
cgitb.enable()         # Web상에서 진행상태 메시지를 콘솔에서 확인할 수 있도록 하는 기능

def show_html():
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
                html{height: 100px;}
                body{height: 100vh; width:100vw;}
                body{background-color: rgb(252, 211, 211);}
                header{background-color: rgb(255,170,170);}
                #section_ml{display: inline-block; background-color: rgb(252, 211, 211); height: 85vh; width: 45vw; text-align:center; margin-left: 4%;}
                #section_nlp{display: inline-block; background-color: rgb(252, 211, 211); height: 85vh; width: 45vw; text-align:center;}
                #title{text-align: center;}
                #ml{margin-right: 10%;}
                #nlp{margin-right: 10%;}

            </style>
    """)
    print(f"""
        </head>
        <body id = "body">
            <header id = "title">
                <h1>My Project Model</h1>
            </header>

            <div id = "section_ml" style="border:5px solid rgb(255,170,170)">
                <nav>
                    <h2 id = "title">머신러닝</h2>
                    <h3 id = "title"> [ 전복 나이 예측 ] </h3>
                    <ul>
                        <a href="./web_ml.py" >
                            <img src="../image/abalone_f.png" style="width: 300px; height: 250px; margin-right: 10%;" >
                        </a>
                        <hr id = "ml">
                        <br>
                        <div id = "ml">
                            전복의 성별, 가장 긴 껍질 길이, 껍질 길이에 수직 길이, 살점 포함 껍질 길이, 전체 전복 무게, 살점 무게, 내장 무게, 건조된 살점 무게를 통해 전복의 나이를 예측하는 모델 생성

                        </div>
                    </ul>
                </nav>
            </div>

            <div id = "section_nlp" style="border:5px solid rgb(255,170,170)">
                <nav>
                    <h2 id = "title">자연어</h2>
                    <h3 id = "title"> [ 낚시성 기사 탐지 ] </h3>
                    <ul>
                        <a href="./web_nlp.py">
                            <img src="../image/nnews.png" style="width: 300px; height: 250px; margin-right: 7%;">
                        </a>
                        <br>
                        <hr id = "nlp">
                        <br>
                        <div id = "nlp">
                            기사의 본문을 통해 기사의 본문이 중간에 내용의 흐름을 벗어나서 다른 내용을 다루고 있는 낚시성 기사인지 아닌지 여부를 판단해주는 모델 생성
                        </div>
                    </ul>
                </nav> 
            </div>
            
        </body>
        </html>

    """)


# (1) WEB 인코딩 설정
if SCRIPT_MODE:
   sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach()) # 웹에서만 필요 : 표준출력을 utf-8로 


# (4) 사용자에게 WEB 화면 제공
show_html()
