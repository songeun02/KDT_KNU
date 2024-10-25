# ----------------------------------------------------------------
# Flask Framework에서 WebServer 구동 파일 
# - 파일명 : app.py
# ----------------------------------------------------------------

# 모듈 로딩 
from flask import Flask

# DB 관련 설정 
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DB = SQLAlchemy() # DB 관련 
MIGRATE = Migrate() # DB 컨트롤러 (DB 생성 및 업데이트)

# ----------------------------------------------------------------
# Application 생성 함수
# - 함수명 : create_app <== 이름 변경 불가
# -- 자동으로 create_app을 호출해서 정상동작 
# ----------------------------------------------------------------

# 사용자 정의 함수
def create_app():

    # 전역 변수 
    # Flask Web Server 인스턴스 생성 - 서버 생성 
    APP = Flask(__name__) 

    # DB 관련 초기화 
    APP.config.from_object(config)

    # DB 초기화 및 연동 
    DB.init_app(APP)
    MIGRATE.init_app(APP, DB)

    # DB 클래스 정의 모듈 로딩 
    from .models import models
    
    # # URL 즉, client 요청 페이지 주소를 보여줄 기능 함수 
    # def print_page():
    #     return "<h1>HELLO ~ </h1>"
    
    # # URL 처리 함수 연결 
    # APP.add_url_rule('/',view_func=print_page, endpoint='INDEX')

    # ## 위의 내용 합침 -> @ 후 def 정의 => decorator 사용 
    # @APP.route('/', endpoint='INDEX')
    # def print_page():
    #     return "<h1>HELLO ~ </h1>"


    # URL 처리 모듈 등록 
    from .views import main_view
    APP.register_blueprint(main_view.main_bp)
    APP.register_blueprint(main_view.a_bp)
    


    return APP

