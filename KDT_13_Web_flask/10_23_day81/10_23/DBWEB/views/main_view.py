# ----------------------------------------------------------------
# Flask Framework에서 모듈단위 URL 처리 파일 
# - 파일명 : main_view.py
# ----------------------------------------------------------------

# 모듈 로딩 
from flask import Blueprint, render_template
from DBWEB.models.models import Question

# Blueprint 인스턴스 생성 
main_bp = Blueprint('main', import_name=__name__, url_prefix='/', template_folder='templates')

# http://localhost:8080/ URL 처리 라우팅 함수 정의 
@main_bp.route('/')
def index():
    return render_template("index.html", name='이송은')

q_bp = Blueprint('question',__name__, url_prefix='/question')

# http://localhost:8080/ URL 처리 라우팅 함수 정의 
@main_bp.route("/qlist")
def print_list():

    # DB에서 조회한 결과를 HTML 파일로 전달
    q_list = Question.query.all()
    return render_template('question_list.html', question_list=q_list)

# http://localhost:5000/qdetail/<int:id> URL 처리 라우팅 함수 정의 
@main_bp.route("/qdetail/<int:question_id>")
def question_item(question_id):

    # DB에서 조회한 1개의 question 인스턴스 전달 
    q = Question.query.get(question_id)
    return render_template('question_detail.html', question=q)


# -------------------------------------------------------------------------

from flask import url_for,  request
from werkzeug.utils import redirect

from DBWEB import DB 

from DBWEB.models.models import Answer

from datetime import datetime

a_bp = Blueprint('answer', __name__, url_prefix='/answer')

@a_bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    question = Question.query.get_or_404(question_id)
    content = request.form['content']
    answer = Answer(content=content, create_date = datetime.now())
    question.answer_set.append(answer) # answer_set : 질문에 달린 답변들 
    DB.session.commit()
    return redirect(url_for('main.question_item', question_id=question_id))
