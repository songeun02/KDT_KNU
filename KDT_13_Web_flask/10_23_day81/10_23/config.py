import os 

# SQLITE3 RDBMS
BASE_DIR = os.path.dirname(__file__)
DB_NAME = 'myweb.db'

# DB관련 기능 구현 시 사용할 변수 
## DB 변경하면 SQLALCHEMY_DATABASE_URI만 수정해서 다른 DB 사용 ㅇ 
## - sqlite 이외의 다른 DB 사용 ㅇ 
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, DB_NAME))
SQLALCHEMY_TRACK_MODIFICATIONS = False