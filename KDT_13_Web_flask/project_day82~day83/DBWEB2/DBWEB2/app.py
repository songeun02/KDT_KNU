from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import torch
from PIL import Image
from torchvision import transforms, models
import torch.nn as nn

app = Flask(__name__)

# 모델 인스턴스 생성 및 가중치 로드
model1=torch.load(r'C:\dlrj_rlaudwn\kdt\KDT-2\DBWEB2\models\top_model_all.pth', map_location='cpu')
model1.eval()

model2=torch.load(r'C:\dlrj_rlaudwn\kdt\KDT-2\DBWEB2\models\bottom_model_all.pth', map_location='cpu')
model2.eval()

model3=torch.load(r'C:\dlrj_rlaudwn\kdt\KDT-2\DBWEB2\models\shoes_model_all.pth', map_location='cpu')
model3.eval()

model4=torch.load(r'C:\dlrj_rlaudwn\kdt\KDT-2\DBWEB2\models\acc_model_all.pth', map_location='cpu')
model4.eval()

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            image = Image.open(filepath)
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
            ])
            input_tensor = transform(image).unsqueeze(0)

            with torch.no_grad():
                result1 = model1(input_tensor)

            probabilities = nn.Softmax(dim=1)(result1)
            predicted_label_index = probabilities.argmax().item()
            class_labels = ["상의", "하의", "신발", "액세서리"]
            predicted_label = class_labels[predicted_label_index]

            return render_template('index.html', title='패션 제품 분류하기', result=predicted_label)

    return render_template('index.html', title="패션 제품 분류하기")




@app.route('/personal/<username>', methods=['GET', 'POST'])
def personal_page(username):
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # 각 사용자에 따라 다른 모델 사용
            model = None
            if username == '상의 분류':  
                model = model1
                class_labels = ["상의", "하의", "신발", "액세서리"]

            elif username == '하의 분류':  
                model = model2
                class_labels = ["하의", "상의", "신발", "액세서리"]


            elif username == '신발 분류':  
                model = model3
                class_labels = ["신발", "하의", "상의", "액세서리"]


            elif username == '액세서리 분류':  
                model = model4
                class_labels = ["액세서리", "하의", "신발", "상의"]


            

            if model:
                with torch.no_grad():
                    image = Image.open(filepath)
                    transform = transforms.Compose([
                        transforms.Resize((224, 224)),
                        transforms.ToTensor(),
                    ])
                    input_tensor = transform(image).unsqueeze(0)

                    result = model(input_tensor)  # 해당 사용자 모델 사용
                    probabilities = nn.Softmax(dim=1)(result)
                    print(probabilities)
                    predicted_label_index = probabilities.argmax().item()
                    predicted_label = class_labels[predicted_label_index]

                
                # 결과 값을 사용자에 맞게 수정
                if username == '상의 분류':
                    result_text = f'{predicted_label} O' if predicted_label == "상의" else f' {predicted_label} X'
                elif username == '하의 분류':
                    result_text = f'{predicted_label} O' if predicted_label == "하의" else f' {predicted_label} X'
                elif username == '신발 분류':
                    result_text = f'{predicted_label} O' if predicted_label == "신발" else f' {predicted_label} X'
                elif username == '액세서리 분류':
                    result_text = f'{predicted_label} O' if predicted_label == "액세서리" else f' {predicted_label} X'


                return render_template('index_personal.html', result=result_text, title=username)
            else:
                return "Model not found for user", 404

    return render_template('index_personal.html', title=username)



if __name__ == '__main__':
    app.run(debug=True)
