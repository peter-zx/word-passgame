from flask import Blueprint, jsonify, request
from config import DATA_DIR
from utils.words_util import load_words_from_csv, update_game_words, save_wrong_words, load_wrong_words
import os
import glob
import pandas as pd

words_bp = Blueprint('words_bp', __name__)

@words_bp.route('/upload_words', methods=['POST'])
def upload_words():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 处理选择已有词库
    if request.get_json() and 'selected_files' in request.get_json():
        selected_files = request.get_json()['selected_files']
        update_game_words(selected_files)
        return jsonify({'message': '词库已更新'})

    # 生成新文件
    existing_files = glob.glob(os.path.join(DATA_DIR, 'words*.csv'))
    new_file_num = len(existing_files) + 1
    new_file = os.path.join(DATA_DIR, f'words{new_file_num}.csv')

    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.csv'):
                content = file.read().decode('utf-8').strip()
                # 确保 CSV 格式正确
                lines = content.split('\n')
                words = [line.split(',') for line in lines if line.strip()]
                df = pd.DataFrame(words, columns=['english', 'chinese', 'difficulty'])
                df.to_csv(new_file, index=False, encoding='utf-8')
            else:
                return jsonify({'error': '仅支持 CSV 文件'}), 400
        elif 'text' in request.form:
            text = request.form['text'].strip()
            if not text:
                return jsonify({'error': '文本内容为空'}), 400
            # 解析粘贴的文本
            lines = text.split('\n')
            words = [line.split(',') for line in lines if line.strip()]
            df = pd.DataFrame(words, columns=['english', 'chinese', 'difficulty'])
            df.to_csv(new_file, index=False, encoding='utf-8')
        else:
            return jsonify({'error': '无效输入'}), 400

        update_game_words([new_file])  # 使用新上传的文件更新 game_words.csv
        return jsonify({'message': f'已保存到 {os.path.basename(new_file)}'})
    except Exception as e:
        return jsonify({'error': f'保存失败: {str(e)}'}), 500

@words_bp.route('/words', methods=['GET'])
def get_words():
    words = load_words_from_csv()
    return jsonify(words)

@words_bp.route('/wrong_words', methods=['GET'])
def get_wrong_words():
    wrong_words = load_wrong_words()
    return jsonify(wrong_words)

@words_bp.route('/wrong_words', methods=['POST'])
def save_wrong_words_route():
    data = request.get_json()
    if not data or 'wrong_words' not in data:
        return jsonify({'error': '无效数据'}), 400
    save_wrong_words(data['wrong_words'])
    return jsonify({'message': '错词已保存'})