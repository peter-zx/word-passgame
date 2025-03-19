from flask import Flask
from routes.home import home_bp
from routes.words import words_bp
from routes.game import game_bp
from routes.scores import scores_bp

app = Flask(__name__, static_folder='static')

# 注册蓝图
app.register_blueprint(home_bp)
app.register_blueprint(words_bp)
app.register_blueprint(game_bp)
app.register_blueprint(scores_bp)

if __name__ == '__main__':
    app.run(debug=True)