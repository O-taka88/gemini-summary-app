# app.py をこの内容に書き換える

import os
import google.generativeai as genai
from flask import Flask, render_template, request
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# --- Gemini APIの初期設定 ---
# 環境変数からAPIキーを取得
api_key = os.environ.get("GEMINI_API_KEY")
# APIキーが設定されていない場合はエラーを出して終了
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# APIキーを設定
genai.configure(api_key=api_key)
# 使用するモデルを準備
model = genai.GenerativeModel('gemini-2.0-flash')
# -----------------------------

# Flaskアプリのインスタンスを作成
app = Flask(__name__)

# ルートURL ("/") にアクセスがあったときの処理 (GETリクエスト)
@app.route("/")
def index():
    # index.html を表示する
    return render_template("index.html", result="")

# "/summarize" URLに対する処理 (POSTリクエスト)
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        # HTMLフォームから"original_text"という名前のデータを取得
        original_text = request.form["original_text"]
        
        # テキストが空の場合はエラーメッセージを返す
        if not original_text:
            return render_template("index.html", result="文章が入力されていません。")

        # Gemini APIへの指示文（プロンプト）を作成
        prompt = f"以下の文章を、重要なポイントを3つに絞って箇条書きで要約してください。\n\n---\n{original_text}"
        
        # AIにリクエストを送信し、結果を取得
        response = model.generate_content(prompt)
        
        # 結果をindex.htmlに埋め込んで表示
        return render_template("index.html", result=response.text, original_text=original_text)

    except Exception as e:
        # 何かエラーが起きた場合
        print(f"An error occurred: {e}")
        return render_template("index.html", result="エラーが発生しました。しばらくしてから再度お試しください。")

# このファイルが直接実行された場合にサーバーを起動
if __name__ == "__main__":
    app.run(debug=True)