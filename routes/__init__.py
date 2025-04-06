from flask import Blueprint

# 创建主蓝图
main = Blueprint('main', __name__)

# 导入所有路由
from . import main_routes
from . import file_analyze