from flask import Blueprint, send_from_directory
import os
from config import BASE_DIR

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def index():
    # 直接返回 index.html，让 Flask 处理静态文件
    return send_from_directory('static', 'index.html')