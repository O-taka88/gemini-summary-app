from flask import Flask

# Flaskアプリのインスタンスを作成
app = Flask(__name__)

# ルートURL ("/") にアクセスがあったときの処理
@app.route("/")
def hello_world():
    return "Hello, World! Flaskサーバーが動いています。"

# このファイルが直接実行された場合にサーバーを起動
if __name__ == "__main__":
    app.run(debug=True)