import requests
from io import BytesIO
from PIL import Image
import time
import pymysql


connect = pymysql.connect(
    host="155.230.153.151",
    user="songeun",
    password="1234",
    db="songeun",
    charset="utf8mb4",
)
cur = connect.cursor()


query = "select * from fashiondf where subcategory = 'Topwear'"
cur.execute(query)
connect.commit()


datas = cur.fetchall()


for index, data in enumerate(datas):
    for attempt in range(3):
        try:
            response = requests.get(data[0], timeout=10)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content))

            img.save(
                rf"C:\Users\Administrator\Desktop\이송은\web_flask_project\image\top\{data[1]}_{index}.jpg"
            )
            break

        except (requests.exceptions.RequestException, OSError) as e:
            print(f"Attempt {attempt + 1} failed for {data[0]}: {e}")
            time.sleep(1)


cur.close()
connect.close()
