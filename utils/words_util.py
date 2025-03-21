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
    word_files = selected_files if selected_files else glob.glob(os.path.join(DATA_DIR, 'words*.csv'))

    all_words = []
    if word_files:
        for wf in word_files:
            try:
                df = pd.read_csv(wf)
                all_words.extend(df.to_dict(orient='records'))
            except Exception as e:
                print(f"Error reading {wf}: {e}")
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
        print(f"Updated {game_file} with {len(all_words)} words")

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