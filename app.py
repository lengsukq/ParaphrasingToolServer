from flask import Flask
from routes import main

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
