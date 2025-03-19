from flask import Blueprint, jsonify, request
from utils.words_util import load_words_from_csv
from utils.game_util import generate_game

game_bp = Blueprint('game_bp', __name__)

@game_bp.route('/game/<level>', methods=['GET'])
def get_game(level):
    words = load_words_from_csv()
    if not words:
        return jsonify({'error': 'No words found'}), 404

    level_map = {'lv1': 4, 'lv2': 5, 'lv3': 6, 'lv4': 7, 'lv5': 8, 'lv6': 9}
    rows = level_map.get(level.lower(), 4)
    groups = []
    group_count = 1 if level == 'endless' else 6
    for _ in range(group_count):
        grid, word_ids = generate_game(words, rows)
        groups.append({'grid': grid, 'word_ids': word_ids})
    return jsonify({'groups': groups, 'rows': rows})

@game_bp.route('/next_group/<level>', methods=['GET'])
def next_group(level):
    words = load_words_from_csv()
    if not words:
        return jsonify({'error': 'No words found'}), 404
    level_map = {'lv1': 4, 'lv2': 5, 'lv3': 6, 'lv4': 7, 'lv5': 8, 'lv6': 9}
    rows = level_map.get(level.lower(), 4)
    grid, word_ids = generate_game(words, rows)
    return jsonify({'grid': grid, 'word_ids': word_ids})

@game_bp.route('/check', methods=['POST'])
def check_pair():
    data = request.get_json()
    word1_id = data.get('word1_id')
    word2_id = data.get('word2_id')
    word_ids = data.get('word_ids')

    if word1_id is None or word2_id is None or word_ids is None:
        return jsonify({'error': 'Invalid request'}), 400

    word1 = word_ids.get(str(word1_id))
    word2 = word_ids.get(str(word2_id))

    if word1 is None or word2 is None:
        return jsonify({'error': 'Invalid word IDs'}), 400

    if word1['value'] == word2['pair'] and word2['value'] == word1['pair']:
        return jsonify({'result': True})
    return jsonify({'result': False})