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
    if request.is_json:
        data = request.get_json()
        if 'selected_files' in data:
            selected_files = data['selected_files']
            update_game_words(selected_files)
            return jsonify({'message': '词库已更新'})
    
    # 处理上传新词库
    existing_files = glob.glob(os.path.join(DATA_DIR, 'words*.csv'))
    new_file_num = len(existing_files) + 1
    new_file = os.path.join(DATA_DIR, f'words{new_file_num}.csv')

    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.csv'):
                content = file.read().decode('utf-8').strip()
                lines = content.split('\n')
                words = [line.replace('，', ',').split(',') for line in lines if line.strip()]  # 替换中文逗号
                df = pd.DataFrame(words, columns=['english', 'chinese', 'difficulty'])
                df.to_csv(new_file, index=False, encoding='utf-8')
            else:
                return jsonify({'error': '仅支持 CSV 文件'}), 400
        elif 'text' in request.form:
            text = request.form['text'].strip()
            if not text:
                return jsonify({'error': '文本内容为空'}), 400
            lines = text.split('\n')
            words = [line.replace('，', ',').split(',') for line in lines if line.strip()]  # 替换中文逗号
            if not all(len(word) == 3 for word in words):
                return jsonify({'error': '每行必须包含 3 列：英文,中文,难度'}), 400
            df = pd.DataFrame(words, columns=['english', 'chinese', 'difficulty'])
            df.to_csv(new_file, index=False, encoding='utf-8')
        else:
            return jsonify({'error': '无效输入'}), 400

        update_game_words([new_file])
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

@words_bp.route('/get_wordbanks', methods=['GET'])
def get_wordbanks():
    wordbank_files = glob.glob(os.path.join(DATA_DIR, 'words*.csv'))
    wrong_words_file = os.path.join(DATA_DIR, 'wrong_words.csv')
    if os.path.exists(wrong_words_file):
        wordbank_files.append(wrong_words_file)
    wordbanks = [os.path.basename(f) for f in wordbank_files]
    return jsonify({'wordbanks': wordbanks})