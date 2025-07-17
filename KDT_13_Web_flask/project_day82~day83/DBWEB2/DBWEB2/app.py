from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import torch
from PIL import Image
from torchvision import transforms, models
import torch.nn as nn

app = Flask(__name__)

# 모델 인스턴스 생성 및 가중치 로드
model1=torch.load(r'C:\Users\sh321\Desktop\KDT_KNU\KDT_13_Web_flask\project_day82~day83\DBWEB2\DBWEB2\models\top_model_all.pth', map_location='cpu',weights_only=False )
model1.eval()

model2=torch.load(r'C:\Users\sh321\Desktop\KDT_KNU\KDT_13_Web_flask\project_day82~day83\DBWEB2\DBWEB2\models\bottom_model_all.pth', map_location='cpu',weights_only=False)
model2.eval()

model3=torch.load(r'C:\Users\sh321\Desktop\KDT_KNU\KDT_13_Web_flask\project_day82~day83\DBWEB2\DBWEB2\models\shoes_model_all.pth', map_location='cpu',weights_only=False)
model3.eval()

model4=torch.load(r'C:\Users\sh321\Desktop\KDT_KNU\KDT_13_Web_flask\project_day82~day83\DBWEB2\DBWEB2\models\acc_model_all.pth', map_location='cpu',weights_only=False)
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
                transforms.Normalize([0.485, 0.456, 0.406],
                                     [0.229, 0.224, 0.225])
            ])
            input_tensor = transform(image).unsqueeze(0)

            with torch.no_grad():
                prob1 = torch.sigmoid(model1(input_tensor))[0].item()
                prob2 = torch.sigmoid(model2(input_tensor))[0].item()
                prob3 = torch.sigmoid(model3(input_tensor))[0].item()
                prob4 = torch.sigmoid(model4(input_tensor))[0].item()

                probs = [prob1, prob2, prob3, prob4]
                print(probs)
                class_labels = ["상의", "하의", "신발", "액세서리"]
                predicted_label = class_labels[probs.index(max(probs))]

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
            
            elif username == '하의 분류':  
                model = model2

            elif username == '신발 분류':  
                model = model3

            elif username == '액세서리 분류':  
                model = model4
              
            if model:
                with torch.no_grad():
                    image = Image.open(filepath)
                    transform = transforms.Compose([
                        transforms.Resize((224, 224)),
                        transforms.ToTensor(),
                        transforms.Normalize([0.485, 0.456, 0.406],
                                             [0.229, 0.224, 0.225])
                    ])
                    input_tensor = transform(image).unsqueeze(0)

                    probabilities = torch.sigmoid(model(input_tensor))[0].item()
                    print(probabilities)

                threshold = 0.7
                
                # 결과 값을 사용자에 맞게 수정
                if username == '상의 분류':
                    result_text = '상의 O' if probabilities >= threshold else '상의 X'
                elif username == '하의 분류':
                    result_text = '하의 O' if probabilities >= threshold else '하의 X'
                elif username == '신발 분류':
                    result_text = '신발 O' if probabilities >= threshold else '신발 X'
                elif username == '액세서리 분류':
                    result_text = '액세서리 O' if probabilities >= threshold else '액세서리 X'

                return render_template('index_personal.html', result=result_text, title=username)
            else:
                return "Model not found for user", 404

    return render_template('index_personal.html', title=username)



if __name__ == '__main__':
    app.run(debug=True)
