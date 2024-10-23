# ----------------------------------------------------------------
# Flask Framework에서  '/'URL에 대한 라우팅 처리 파일 
# - 파일명 : main_views.py
# ----------------------------------------------------------------

# 모듈 로딩 
from flask import Blueprint,render_template

# Blueprint 인스턴스 생성
main_bp = Blueprint('root', __name__, url_prefix='/') # main -> root 이후 flask routes 실행하면 main.index -> root.index 
# __name__ : 실행하면 파일명...? 변수명..? 

# 라우팅 기능 함수 정의 
@main_bp.route('/', endpoint = 'hello') # endpoint = 'hello' 지정 후 flask routes 실행하면 root.index -> root.hello
# 원래 endpoint의 의미는 사용자가 요청한 url 주소
# flask에서는 endpoint가 함수의 별칭 -> 함수 이름을 외부에 노출시키지 않음 -> 함수명 변경해도 ㅇ 
def kiki():
    return render_template('index.html')