from flask import Flask, request, jsonify
import mongoengine as me
from dotenv import load_dotenv
import os

# 加載 .env 文件中的環境變數
load_dotenv()

app = Flask(__name__)

# 從 .env 文件中讀取 MongoDB 連接字串
mongo_uri = os.getenv('MONGO_URI')

# 連接到 MongoDB
me.connect(host=mongo_uri)

# 定義 User 模型
class User(me.Document):
    name = me.StringField(required=True)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True)

    meta = {
        'collection': 'users'  # 手動指定集合名稱為 'users'
    }

# 創建新用戶的 API
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'], password=data['password'])
    user.save()
    return jsonify({"id": str(user.id), "message": "User created"}), 201

# 查詢所有用戶的 API
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.objects()
    return jsonify(users), 200

# 啟動 Flask 伺服器
if __name__ == '__main__':
    app.run(debug=True)
