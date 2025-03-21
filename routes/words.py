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
    if 'selected_files' in request.get_json():
        selected_files = request.get_json()['selected_files']
        update_game_words(selected_files)
        return jsonify({'message': 'Wordbank updated'})
    
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