import pandas as pd
import os
import glob
from config import DATA_DIR

def load_words_from_csv():
    words_file = os.path.join(DATA_DIR, 'game_words.csv')
    try:
        df = pd.read_csv(words_file)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"Words file not found: {words_file}")
        return []
    except Exception as e:
        print(f"Error loading words: {e}")
        return []

def update_game_words(selected_files=None):
    default_file = os.path.join(DATA_DIR, 'default_words.csv')
    game_file = os.path.join(DATA_DIR, 'game_words.csv')
    word_files = glob.glob(os.path.join(DATA_DIR, 'words*.csv')) if selected_files is None else selected_files

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
                {'english': 'dog', 'chinese': '狗', 'difficulty': 'L2'},
                {'english': 'elephant', 'chinese': '大象', 'difficulty': 'L3'}
            ]
            pd.DataFrame(default_data).to_csv(default_file, index=False, encoding='utf-8')
        try:
            df = pd.read_csv(default_file)
            all_words = df.to_dict(orient='records')
        except Exception as e:
            print(f"Error reading default file: {e}")
            all_words = []

    if all_words:
        df = pd.DataFrame(all_words)
        df.to_csv(game_file, index=False, encoding='utf-8')
        print(f"Updated {game_file} with {len(all_words)} words")
    else:
        print("No words available to update game_words.csv")

def save_wrong_words(wrong_words):
    wrong_file = os.path.join(DATA_DIR, 'wrong_words.csv')
    existing_words = load_wrong_words()
    # 去重：基于 english 和 chinese
    unique_words = { (w['english'], w['chinese']) : w for w in existing_words + wrong_words }
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