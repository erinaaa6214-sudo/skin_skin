# 🌸 My Skin Routine

スキンケアルーティンを管理する日本語対応Webアプリです。

## ファイル構成

```
MySkinRoutine/
├── main.py          # メインアプリ（Streamlit）
├── database.py      # SQLite DB操作
├── utils.py         # カテゴリ・診断・レコメンドロジック
├── requirements.txt
└── README.md
```

## ローカルで動かす

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Streamlit Community Cloudへのデプロイ手順

1. このフォルダの中身を **GitHubリポジトリ** にプッシュする
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/<あなたのユーザー名>/<リポジトリ名>.git
   git push -u origin main
   ```

2. [share.streamlit.io](https://share.streamlit.io) にアクセスしてGitHubでサインイン

3. 「New app」→ リポジトリ・ブランチ・`main.py` を選択してデプロイ

4. SQLiteファイル（`skincare.db`）はCloud上で自動生成されます

## 初期パスワード

```
skincare2024
```

> `main.py` の `PASSWORD_HASH` を変更することでパスワードを変更できます。
> `hashlib.sha256("新パスワード".encode()).hexdigest()` をPythonで実行して置き換えてください。

## 機能一覧

| 機能 | 説明 |
|------|------|
| 🔐 ログイン | 簡易パスワード認証 |
| ➕ アイテム登録 | カテゴリ・成分・使用タイミングを登録・編集・削除 |
| ☀️ 朝ルーティン | 朝用アイテムをステップ順に表示・並び替え |
| 🌙 夜ルーティン | 夜用アイテムをステップ順に表示・並び替え |
| 🔬 相性診断 | 成分の危険な組み合わせを自動検出 |
| 💡 レコメンド | ルーティンのギャップを分析してアドバイス |

## 相性診断でチェックしている成分の組み合わせ

- 🔴 レチノール ＋ AHA/BHA
- 🟡 高濃度ビタミンC ＋ ナイアシンアミド
- 🟡 レチノール ＋ ビタミンC
- 🔴 ピーリング ＋ レチノール
- 🔴 ベンゾイルパーオキサイド ＋ レチノール
- 🟡 複数のピーリング成分の重複
