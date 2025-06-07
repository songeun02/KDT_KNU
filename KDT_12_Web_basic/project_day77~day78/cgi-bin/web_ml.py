import joblib      # AI 모델 관련
import os
import cgi, cgitb  # cgi 프로그래밍 관련
import sys, codecs # 인코딩 관련
from joblib import load
import numpy as np
from scipy.stats import boxcox

# 동작관련 전역 변수----------------------------------
SCRIPT_MODE = True    # Jupyter Mode : False, WEB Mode : True
cgitb.enable()         # Web상에서 진행상태 메시지를 콘솔에서 확인할 수 있도록 하는 기능

def show_html(predict_age):
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
            #content {display : flex; text-align: left; margin-left: 10%; width: 90%;}
            #input_data {flex:1;}
            #result_box {flex:1; margin-top : 13%;}
        </style>
    """)
    print(f"""
    </head>
    <body id = "body">
        <header id = "title">
            <h1>My Project Model</h1>
        </header>

        <div id = "section_ml" style="border:5px solid rgb(255,170,170)">
            
            <h2 id = "title">머신러닝</h2>
            <h3 id = "title"> [ 전복 나이 예측 ] </h3>
            <img src="../image/abalone_f.png" style="width: 70px; hegiht: 60px; margin-left: 48%;" >
                    
            <hr>
    
            <br>
            <form id ="content" action="/cgi-bin/web_ml.py" method="POST">
                <div id = "input_data">
                    <fieldset> 
                        <legend>전복 성별 (Sex)</legend>
                        <label>
                            <input type = "radio" name = "gender" value = "F"> F
                            <input type = "radio" name="gender" value="I"> I(infant)
                            <input type = "radio" name="gender" value="M"> M
                        </label>
            
                    </fieldset>

                    <br>
                    가장 긴 껍질 길이 (Length) <input type="text" name="length"><br><br>
                    껍질 길이에 수직 길이 (Diameter) <input type="text" name="diameter"><br><br>
                    살점 포함 껍질 길이 (Height) <input type="text" name="height"><br><br>
                    전체 전복 무게 (Whole Weight) <input type="text" name="whole_weight"><br><br>
                    살점 무게 (Shucked Weight) <input type="text" name="shucked_weight"><br><br>
                    내장 무게 (Viscera weight) <input type="text" name="viscera_weight"><br><br>
                    건조된 살점 무게 (Shell Weight) <input type="text" name="shell_weight"><br>

                    
                    <input type = "submit" value = "전송" style="margin-left : 90%;" margin-top:1%;>
                    
                </div>

                <div id = "result_box">
                    <h3 style="margin-left: 20%;">예측된 전복 나이 : {predict_age}</h3>
                </div>


            </form>

        </div>
        
    </body>
    </html>
    """)

def sex_num(sex):
    if sex == 'F':
        sex_list = [1,0,0]
    elif sex == 'I':
        sex_list = [0,1,0]
    else:
        sex_list = [0,0,1]

    return sex_list

def make_array(sex_array, length, diameter, height, whole_weight, shucked_weight, viscera_weight, shell_weight):

    # 입력 데이터 전처리 
    lambda_length, lambda_diameter = joblib.load(lambdafile)

    length_process = boxcox(float(length), lambda_length)
    diameter_process = boxcox(float(diameter), lambda_diameter)
    height_process = np.sqrt(float(height))
    whole_weight_process = np.sqrt(float(whole_weight))
    shucked_weight_process = np.sqrt(float(shucked_weight))
    viscera_weight_process = np.sqrt(float(viscera_weight))
    shell_weight_process = np.sqrt(float(shell_weight))

    # 입력 데이터를 배열로 변환
    input_data = np.array([[
        int(sex_array[0]),
        int(sex_array[1]),
        int(sex_array[2]),
        length_process,
        diameter_process,
        height_process,
        whole_weight_process,
        shucked_weight_process,
        viscera_weight_process,
        shell_weight_process
    ]])
    return input_data


# (1) WEB 인코딩 설정
if SCRIPT_MODE:
   sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach()) # 웹에서만 필요 : 표준출력을 utf-8로 

# (2) 모델 로딩
if SCRIPT_MODE:
    mlfile = os.path.dirname(__file__)+ '/model_run_file/model_ml_bagging.joblib' # 웹상에서는 절대경로만
else:
    mlfile = './model_run_file/model_ml_bagging.pkl'

# (3) 스케줄러 로딩 
if SCRIPT_MODE:
    scalerfile = os.path.dirname(__file__)+ '/model_run_file/scaler_ml_bagging.joblib' # 웹상에서는 절대경로만
else:
    scalerfile = './model_run_file/scaler_ml_bagging.pkl'

# (4) λ 로딩 
if SCRIPT_MODE:
    lambdafile = os.path.dirname(__file__)+ '/model_run_file/x_boxcox_lambdas.joblib' # 웹상에서는 절대경로만
else:
    lambdafile = './x_boxcox_lambdas.pkl'

    
# # (3) WEB 사용자 입력 데이터 처리
# # (3-1) HTML 코드에서 사용자 입력 받는 form 태크 영역 객체 가져오기
form = cgi.FieldStorage()

# 폼에서 입력된 데이터 가져오기
sex = form.getvalue('gender','')
length = form.getvalue('length','')
diameter = form.getvalue('diameter','')
height = form.getvalue('height','')
whole_weight = form.getvalue('whole_weight','')
shucked_weight = form.getvalue('shucked_weight','')
viscera_weight = form.getvalue('viscera_weight','')
shell_weight = form.getvalue('shell_weight','')

predicted_value=0


# 입력 데이터를 배열로 변환
if len(length):
    sex_array = sex_num(sex)

    input_data = make_array(sex_array, length, diameter, height, whole_weight, shucked_weight, viscera_weight, shell_weight)

    mlModel = joblib.load(mlfile)
    scaler = joblib.load(scalerfile)
    input_data_scaled = scaler.transform(input_data)

    # 예측하기
    predicted_value = mlModel.predict(input_data_scaled)
    predicted_value = predicted_value[0]

# (4) 사용자에게 WEB 화면 제공
show_html(predicted_value ** 2)
