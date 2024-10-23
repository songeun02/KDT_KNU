# ----------------------------------------------------------------
# Flask Framework에서 WebServer 구동 파일 
# - 파일명 : app.py
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# # 연결 확인 
# # 모듈 로딩 
# import flask
# import pandas as pd 

# print(f'Pandas v.{pd.__version__}')

# ----------------------------------------------------------------

# 모듈 로딩 
from flask import Flask, render_template

# 사용자 정의 함수
def create_app():

    # 전역 변수 
    # Flask Web Server 인스턴스 생성 
    APP = Flask(__name__) 

    # 라우팅 기능 함수 
    # Flask Web Server 인스턴스 변수명.route("URL")
    @APP.route("/") # 이 url(root)가 들어왔을 때 동작
    def index():
        # return """<body style = 'background-color:skyblue;'>
        #             <h1>HELLO</h1>
        #             </body>"""

        # html 연결 
        return render_template('index.html')

    # http://127.0.0.1:5000/info
    @APP.route("/info")
    @APP.route("/info/")
    def info():
        return """<body style='background-color:yellow; text-align:center'>
                    <h1>흐아아암</h1>
                    </body>"""


    # http://127.0.0.1:5000/info/문자열변수
    @APP.route("/info/<name>")
    def print_info(name):
        # return f"""
        #     <body style='background-color:skyblue; text-align:center'>
        #         <h1>{name}'s Information</h1>
        #         어...? 
        #     </body> """

        return render_template('info.html', name=name)

    # http://127.0.0.1:5000/info/정수
    # age라는 변수에 정수 저장 
    @APP.route("/info/<int:age>")
    def check_age(age):
        return f"""
        <body style='background-color:pink; text-align:center'>
        나이:{age}
        </body>
    """

    # http://127.0.0.1:5000/info/go
    @APP.route("/go")
    def go_home():
        return APP.redirect("/")

    return APP


# 조건부 실행 
if __name__ == '__main__':
    # Flask Web Server 구동 
    create_app.run()
    # create_app 함수명 변경 금지