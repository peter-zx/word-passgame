import random

def generate_game(words, rows):
    pair_count = min(rows, len(words))
    available_words = words * (rows // len(words) + 1) if len(words) < rows else words
    selected_words = random.sample(available_words, pair_count)
    game_items = []
    for word in selected_words:
        game_items.append({'type': 'english', 'value': word['english'], 'pair': word['chinese']})
        game_items.append({'type': 'chinese', 'value': word['chinese'], 'pair': word['english']})
    random.shuffle(game_items)
    game_grid = []
    word_ids = {}
    for i, item in enumerate(game_items):
        word_ids[i] = item
        game_grid.append({'id': i, 'value': item['value']})
    return game_grid, word_ids