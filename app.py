from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv('.env.local')

from routes import main

app = Flask(__name__)

# 配置CORS
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": "*"}})

# 注册蓝图
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
