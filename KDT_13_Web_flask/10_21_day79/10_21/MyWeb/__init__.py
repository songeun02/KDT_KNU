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

    # 라우팅 기능 모듈 
    from .views import main_views
    
    ## views/main_views.py에 있는 main_bp인 blueprint 객체 가져오기
    APP.register_blueprint(main_views.main_bp) 
    

    return APP


# 조건부 실행 
if __name__ == '__main__':
    # Flask Web Server 구동 
    create_app.run()
    # create_app 함수명 변경 금지