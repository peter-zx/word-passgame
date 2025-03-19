# 假设之前的 scores.py 内容，这里仅示例
from flask import Blueprint, jsonify, request
from config import DATA_DIR
import os
import json

scores_bp = Blueprint('scores_bp', __name__)

@scores_bp.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    score_file = os.path.join(DATA_DIR, 'scores.json')
    scores = []
    if os.path.exists(score_file):
        with open(score_file, 'r', encoding='utf-8') as f:
            scores = json.load(f)
    scores.append(data)
    with open(score_file, 'w', encoding='utf-8') as f:
        json.dump(scores[-5:], f)  # 保留最近 5 次
    return jsonify({'message': 'Score saved'})

@scores_bp.route('/get_scores', methods=['GET'])
def get_scores():
    score_file = os.path.join(DATA_DIR, 'scores.json')
    if os.path.exists(score_file):
        with open(score_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])