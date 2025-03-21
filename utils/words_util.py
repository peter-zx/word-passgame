###Bug 分析：game_words.csv 未及时更新
import pandas as pd
import os
import glob
from config import DATA_DIR

def load_words_from_csv():
    words_file = os.path.join(DATA_DIR, 'game_words.csv')
    if not os.path.exists(words_file):
        update_game_words()
    try:
        df = pd.read_csv(words_file)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error loading words: {e}")
        return []

def update_game_words(selected_files=None):
    default_file = os.path.join(DATA_DIR, 'default_words.csv')
    game_file = os.path.join(DATA_DIR, 'game_words.csv')
    
    # 删除旧的 game_words.csv
    if os.path.exists(game_file):
        os.remove(game_file)
        print(f"Deleted old {game_file}")
    
    all_words = []
    # 如果提供了选择的文件
    if selected_files:
        for wf in selected_files:
            full_path = wf if os.path.isabs(wf) else os.path.join(DATA_DIR, wf)  # 支持相对路径和绝对路径
            if os.path.exists(full_path):
                try:
                    df = pd.read_csv(full_path)
                    all_words.extend(df.to_dict(orient='records'))
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")
            else:
                print(f"File not found: {full_path}")
    # 如果未提供选择文件，使用默认词库
    else:
        if not os.path.exists(default_file):
            default_data = [
                {'english': 'apple', 'chinese': '苹果', 'difficulty': 'L1'},
                {'english': 'banana', 'chinese': '香蕉', 'difficulty': 'L1'},
                {'english': 'cat', 'chinese': '猫', 'difficulty': 'L2'},
                {'english': 'dog', 'chinese': '狗', 'difficulty': 'L2'}
            ]
            pd.DataFrame(default_data).to_csv(default_file, index=False, encoding='utf-8')
        df = pd.read_csv(default_file)
        all_words = df.to_dict(orient='records')

    if all_words:
        df = pd.DataFrame(all_words)
        df.to_csv(game_file, index=False, encoding='utf-8')
        print(f"Created new {game_file} with {len(all_words)} words")
    else:
        print("No valid words to write to game_words.csv")

def save_wrong_words(wrong_words):
    wrong_file = os.path.join(DATA_DIR, 'wrong_words.csv')
    existing_words = load_wrong_words()
    unique_words = { (w['english'], w['chinese']): w for w in (existing_words + wrong_words) if 'english' in w and 'chinese' in w }
    df = pd.DataFrame(list(unique_words.values()))
    df.to_csv(wrong_file, index=False, encoding='utf-8')
    print(f"Saved {len(unique_words)} unique wrong words to {wrong_file}")

def load_wrong_words():
    wrong_file = os.path.join(DATA_DIR, 'wrong_words.csv')
    try:
        df = pd.read_csv(wrong_file)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading wrong words: {e}")
        return []