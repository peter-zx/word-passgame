from flask import Blueprint, jsonify, request
from config import DATA_DIR
from utils.words_util import load_words_from_csv, update_game_words, save_wrong_words, load_wrong_words
import os  # 确认存在
import glob
import pandas as pd

words_bp = Blueprint('words_bp', __name__)

@words_bp.route('/upload_words', methods=['POST'])
def upload_words():
    os.makedirs(DATA_DIR, exist_ok=True)
    existing_files = glob.glob(os.path.join(DATA_DIR, 'words*.csv'))
    new_file_num = len(existing_files) + 1
    new_file = os.path.join(DATA_DIR, f'words{new_file_num}.csv')

    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.csv'):
            content = file.read().decode('utf-8').strip()
            with open(new_file, 'w', encoding='utf-8') as f:
                f.write('english,chinese,difficulty\n' + content)
    elif 'text' in request.form:
        text = request.form['text'].strip()
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write('english,chinese,difficulty\n' + text)
    else:
        return jsonify({'error': 'Invalid input'}), 400

    update_game_words()
    return jsonify({'message': f'Words added to {new_file}'})

@words_bp.route('/words', methods=['GET'])
def get_words():
    words = load_words_from_csv()
    return jsonify(words)

@words_bp.route('/add_word', methods=['POST'])
def add_word():
    data = request.get_json()
    if not data or 'english' not in data or 'chinese' not in data or 'difficulty' not in data:
        return jsonify({'error': 'Invalid or missing data'}), 400

    words = load_words_from_csv()
    words.append({'english': data['english'], 'chinese': data['chinese'], 'difficulty': data['difficulty']})

    try:
        df = pd.DataFrame(words)
        df.to_csv(os.path.join(DATA_DIR, 'game_words.csv'), index=False, encoding='utf-8')
        return jsonify({'message': 'Word added successfully'})
    except Exception as e:
        return jsonify({'error': f'Error saving words: {e}'}), 500

@words_bp.route('/wrong_words', methods=['GET'])
def get_wrong_words():
    wrong_words = load_wrong_words()
    return jsonify(wrong_words)

@words_bp.route('/wrong_words', methods=['POST'])
def save_wrong_words_route():
    data = request.get_json()
    if not data or 'wrong_words' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    save_wrong_words(data['wrong_words'])
    return jsonify({'message': 'Wrong words saved'})

# 在 words_bp 下新增
@words_bp.route('/upload_words', methods=['POST'])
def upload_words():
    os.makedirs(DATA_DIR, exist_ok=True)
    if 'selected_files' in request.get_json():
        selected_files = request.get_json()['selected_files']
        update_game_words(selected_files)
        return jsonify({'message': 'Wordbank updated'})
    # 其余代码不变