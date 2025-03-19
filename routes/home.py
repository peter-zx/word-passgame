from flask import Blueprint, send_from_directory
import os  # 新增导入
from config import BASE_DIR

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def index():
    return send_from_directory(os.path.join(BASE_DIR, 'static'), 'index.html')