import sqlite3
import json
from datetime import datetime

DB_PATH = "skincare.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────────────────────────────────────────
# 初期商品データ（80品）
# (category, subcategory, brand, product_name, key_ingredients)
# ─────────────────────────────────────────────────────────────────────────────
INITIAL_PRODUCTS = [
    # ── 洗顔料 ───────────────────────────────────────────────────────────────
    ("洗顔料", "洗顔フォーム", "キュレル", "キュレル 泡洗顔料", "セラミド,グリセリン,ラウリン酸アミドプロピルベタイン"),
    ("洗顔料", "洗顔フォーム", "肌ラボ", "肌ラボ 白潤プレミアム 薬用美白泡洗顔", "トラネキサム酸,ヒアルロン酸,グリセリン"),
    ("洗顔料", "洗顔フォーム", "ビオレ", "ビオレ モイスチャーマイルド洗顔フォーム", "ヒアルロン酸,セリシン,グリセリン"),
    ("洗顔料", "洗顔フォーム", "イハダ", "イハダ 薬用洗顔フォーム", "グリチルリチン酸2K,ユーカリ葉エキス,グリセリン"),
    ("洗顔料", "洗顔フォーム", "Kiehl's", "キールズ アルティモイスチャー フェイシャル ソープ", "セサミオイル,グリセリン,水添ポリイソブテン"),
    ("洗顔料", "洗顔石鹸", "ドクターシーラボ", "ドクターシーラボ エンリッチリフト洗顔料", "コラーゲン,ヒアルロン酸,プラセンタエキス"),
    ("洗顔料", "洗顔フォーム", "CeraVe", "CeraVe ハイドレーティング クレンザー", "セラミド,ヒアルロン酸,ナイアシンアミド"),
    ("洗顔料", "洗顔フォーム", "FANCL", "ファンケル マイルドクレンジングオイル＆洗顔セット", "酵素,グリセリン,海藻エキス"),
    ("洗顔料", "洗顔パウダー", "資生堂", "エリクシール ルフレ バランシング おしろいミルク", "酵素,グリセリン,スクワラン"),

    # ── クレンジング ─────────────────────────────────────────────────────────
    ("クレンジング", "オイルクレンジング", "ファンケル", "ファンケル マイルドクレンジングオイル", "ホホバオイル,オリーブオイル,グリセリン"),
    ("クレンジング", "オイルクレンジング", "DHC", "DHC 薬用ディープクレンジングオイル", "オリーブオイル,グリセリン,ローズマリー葉エキス"),
    ("クレンジング", "ミルククレンジング", "DECORTÉ", "コスメデコルテ AQ ミレニアム クレンジングミルク", "シア脂,ヒアルロン酸,コラーゲン,ゴールデンロータスエキス"),
    ("クレンジング", "クレンジングバーム", "Clé de Peau", "クレ・ド・ポー ボーテ ユイル デマキヤント リッシュ n", "ミネラルオイル,ミツロウ,サクラ葉エキス"),
    ("クレンジング", "クレンジングジェル", "ルナソル", "ルナソル スムーシングクレンジングオイル", "ラベンダー油,ヒマワリ種子油,グリセリン"),
    ("クレンジング", "クレンジングバーム", "Banila co.", "バニラコ クリーン イット ゼロ クレンジングバーム", "シア脂,セテアリルアルコール,ミネラルオイル"),
    ("クレンジング", "ミルククレンジング", "HABA", "ハーバー スクワランクレンジングミルク", "スクワラン,シア脂,グリセリン"),
    ("クレンジング", "リキッドクレンジング", "ビオデルマ", "ビオデルマ サンシビオ エイチツーオー D", "キュウリ果実エキス,マンニトール,グルコシド"),
    ("クレンジング", "クレンジングシート", "キュレル", "キュレル 泡クレンジングシート", "セラミド,グリセリン,グリチルリチン酸2K"),

    # ── 化粧水 ───────────────────────────────────────────────────────────────
    ("化粧水", "化粧水", "肌ラボ", "肌ラボ 極潤ヒアルロン液", "ヒアルロン酸,アセチルヒアルロン酸,グリセリン"),
    ("化粧水", "化粧水", "キュレル", "キュレル 潤浸保湿 化粧水 III とてもしっとり", "セラミド,グリセリン,グリチルリチン酸2K"),
    ("化粧水", "化粧水", "ナチュリエ", "ナチュリエ ハトムギ化粧水", "ハトムギエキス,グリセリン,BG"),
    ("化粧水", "化粧水", "SK-II", "SK-II フェイシャル トリートメント エッセンス", "ピテラ,ナイアシンアミド,パントテニルエチルエーテル"),
    ("化粧水", "化粧水", "雪肌精", "雪肌精 化粧水 しっとり", "コメエキス,甘草エキス,ヨクイニンエキス"),
    ("化粧水", "化粧水", "エリクシール", "エリクシール シュペリエル バランシング 化粧水 I", "トレハロース,ヒアルロン酸,コラーゲン"),
    ("化粧水", "化粧水", "DECORTÉ", "コスメデコルテ モイスチュアリスタ ローション", "ヒアルロン酸,コラーゲン,スクワラン"),
    ("化粧水", "ブースター・導入液", "DECORTÉ", "コスメデコルテ AQ ブースター セラム", "ヒアルロン酸,コラーゲン,セラミド"),
    ("化粧水", "ミスト状化粧水", "ラロッシュポゼ", "ラロッシュポゼ ターマルウォーター", "温泉水,ミネラル,セレン"),
    ("化粧水", "化粧水", "ALBION", "アルビオン スキンコンディショナー エッセンシャル N", "甘草エキス,ソウハクヒエキス,ヒアルロン酸"),
    ("化粧水", "化粧水", "dプログラム", "dプログラム バランスケア ローション MB", "グリチルリチン酸2K,セラミド,ナイアシンアミド"),
    ("化粧水", "化粧水", "ONE BY KOSÉ", "ONE BY KOSÉ ザ ローション", "コウジ酸誘導体,ナイアシンアミド,ヒアルロン酸"),
    ("化粧水", "化粧水", "The Ordinary", "The Ordinary ナイアシンアミド トナー", "ナイアシンアミド,亜鉛PCA,グリセリン"),
    ("化粧水", "化粧水", "ソフィーナ", "ソフィーナiP ベースケア セラム 土台美容液", "AHA,ナイアシンアミド,ヒアルロン酸"),

    # ── 乳液・美容液・フェイスクリームなど ─────────────────────────────────
    ("乳液・美容液・フェイスクリームなど", "美容液", "SK-II", "SK-II スキンパワー エッセンス", "ピテラ,ナイアシンアミド,コウジ酸"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "資生堂", "アルティミューン パワライジング コンセントレートIII", "イリス根エキス,ヒアルロン酸,レチノール"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "エリクシール", "エリクシール シュペリエル エンリッチドセラム CB", "ヒアルロン酸,スーパーリフトEX,コラーゲン"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "The Ordinary", "The Ordinary レチノール 0.5% in スクワラン", "レチノール,スクワラン,ローズヒップオイル"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "The Ordinary", "The Ordinary ナイアシンアミド 10% + 亜鉛 1%", "ナイアシンアミド,亜鉛PCA,グリセリン"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "HABA", "ハーバー スクワランオイル", "スクワラン"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "メラノCC", "メラノCC 薬用しみ集中対策美容液", "ビタミンC誘導体,ビタミンE誘導体,グリコシルルチン"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "DECORTÉ", "コスメデコルテ AQ セラム", "レチノール,コラーゲン,ヒアルロン酸"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "ポーラ", "ポーラ B.A セラム", "アルガンエキス,コメ発酵エキス,ヒアルロン酸"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "Kiehl's", "キールズ パワー ストレングス マルチパーパス コンセントレート", "ビタミンC,グリセリン,ヒアルロン酸"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "Sulwhasoo", "雪花秀 ファーストケア アクティベーティング セラム", "高麗人参根エキス,白樺エキス,アデノシン"),
    ("乳液・美容液・フェイスクリームなど", "美容液", "The Inkey List", "The Inkey List レチノール セラム", "レチノール,スクワラン,グリセリン"),
    ("乳液・美容液・フェイスクリームなど", "乳液", "キュレル", "キュレル 潤浸保湿 乳液", "セラミド,グリセリン,グリチルリチン酸2K"),
    ("乳液・美容液・フェイスクリームなど", "乳液", "エリクシール", "エリクシール シュペリエル バランシング 乳液 I", "コラーゲン,ヒアルロン酸,スーパーモイスチャーミルクEX"),
    ("乳液・美容液・フェイスクリームなど", "乳液", "肌ラボ", "肌ラボ 極潤ヒアルロン乳液", "ヒアルロン酸,アセチルヒアルロン酸,グリセリン"),
    ("乳液・美容液・フェイスクリームなど", "乳液", "dプログラム", "dプログラム バランスケア エマルジョン MB", "グリチルリチン酸2K,セラミド,ヒアルロン酸"),
    ("乳液・美容液・フェイスクリームなど", "フェイスクリーム", "CeraVe", "CeraVe モイスチャライジングクリーム", "セラミド,ヒアルロン酸,ナイアシンアミド"),
    ("乳液・美容液・フェイスクリームなど", "フェイスクリーム", "キュレル", "キュレル 潤浸保湿 フェイスクリーム", "セラミド,グリセリン,グリチルリチン酸2K"),
    ("乳液・美容液・フェイスクリームなど", "フェイスクリーム", "DECORTÉ", "コスメデコルテ AQ ミレニアム クリーム", "コラーゲン,ヒアルロン酸,レチノール誘導体"),
    ("乳液・美容液・フェイスクリームなど", "フェイスクリーム", "ラ メール", "ラ メール クレーム ドゥ・ラ・メール", "ミラクルブロス,ケルプ,シトラスオイル"),
    ("乳液・美容液・フェイスクリームなど", "フェイスクリーム", "ポーラ", "ポーラ B.A クリーム", "アルガンエキス,レチノール,コラーゲン"),
    ("乳液・美容液・フェイスクリームなど", "フェイスクリーム", "エリクシール", "エリクシール リンクルクリームS", "レチノール,グリセリン,スクワラン"),
    ("乳液・美容液・フェイスクリームなど", "フェイスクリーム", "ニベア", "ニベア クリーム", "グリセリン,ミツロウ,ラノリン"),
    ("乳液・美容液・フェイスクリームなど", "フェイスオイル・バーム", "HABA", "ハーバー スクワランフェイスオイル", "スクワラン,アルガンオイル"),
    ("乳液・美容液・フェイスクリームなど", "フェイスオイル・バーム", "Clarins", "クラランス フェイス トリートメント オイル", "ローズヒップオイル,ハチミツ,ビタミンE"),
    ("乳液・美容液・フェイスクリームなど", "オールインワン化粧品", "肌ラボ", "肌ラボ 白潤プレミアム 薬用浸透美白オールインワンゲル", "トラネキサム酸,ヒアルロン酸,コラーゲン"),
    ("乳液・美容液・フェイスクリームなど", "オールインワン化粧品", "ドクターシーラボ", "ドクターシーラボ アクアコラーゲンゲル エンリッチリフト", "コラーゲン,ヒアルロン酸,プラセンタエキス"),

    # ── パック・フェイスマスク ──────────────────────────────────────────────
    ("パック・フェイスマスク", "シートマスク・パック", "LuLuLun", "ルルルン フェイスマスク ピュア モイスト", "ヒアルロン酸,グリセリン,BG"),
    ("パック・フェイスマスク", "シートマスク・パック", "SK-II", "SK-II フェイシャル トリートメント マスク", "ピテラ,ナイアシンアミド,グリセリン"),
    ("パック・フェイスマスク", "シートマスク・パック", "メディヒール", "メディヒール TEAトゥリー エッセンシャル マスク", "ティーツリーエキス,ヒアルロン酸,アラントイン"),
    ("パック・フェイスマスク", "シートマスク・パック", "My Beauty Diary", "マイビューティーダイアリー ホワイトトリュフ マスク", "白トリュフエキス,ヒアルロン酸,コラーゲン"),
    ("パック・フェイスマスク", "スリーピングマスク・パック", "LANEIGE", "ラネージュ ウォーター スリーピング マスク", "ヒアルロン酸,プロバイオティクス,ハーブエキス"),
    ("パック・フェイスマスク", "洗い流すパック・マスク", "ポーラ", "ポーラ ホワイトショット クリアスキンラボ", "ビタミンC誘導体,グリチルリチン酸2K,グリセリン"),
    ("パック・フェイスマスク", "ゴマージュ・ピーリング", "The Ordinary", "The Ordinary AHA 30% + BHA 2% ピーリングソリューション", "グリコール酸,サリチル酸,ヒアルロン酸"),
    ("パック・フェイスマスク", "ゴマージュ・ピーリング", "ソフィーナ", "ソフィーナ iP インターリンク セラム", "AHA,ヒアルロン酸,コラーゲン"),
    ("パック・フェイスマスク", "マッサージ料", "シセイドウ", "資生堂 エリクシール リフティングマッサージクリーム", "コラーゲン,ヒアルロン酸,グリセリン"),

    # ── その他スキンケア（日焼け止め） ─────────────────────────────────────
    ("その他スキンケア", "その他スキンケア", "アネッサ", "アネッサ パーフェクトUV スキンケアミルク A SPF50+", "酸化チタン,グリセリン,ヒアルロン酸"),
    ("その他スキンケア", "その他スキンケア", "ビオレ", "ビオレUV アクアリッチ ウォータリーエッセンス SPF50+", "ヒアルロン酸,グリセリン,ポリグルタミン酸"),
    ("その他スキンケア", "その他スキンケア", "ラロッシュポゼ", "ラロッシュポゼ アンテリオス UVイデア XL プロテクション SPF50+", "酸化チタン,グリセリン,ビタミンEP"),
    ("その他スキンケア", "その他スキンケア", "isntree", "イズントゥリー ヒアルロニック サンセラム SPF50+", "ヒアルロン酸,ナイアシンアミド,アロエベラ"),
    ("その他スキンケア", "その他スキンケア", "AHC", "AHC ナチュラルパーフェクション フレッシュサンスクリーン SPF50+", "ナイアシンアミド,グリセリン,セラミド"),

    # ── 目元・口元ケア ───────────────────────────────────────────────────────
    ("目元・口元ケア", "アイケア・アイクリーム", "DECORTÉ", "コスメデコルテ AQ アイクリーム", "コラーゲン,レチノール,ペプチド"),
    ("目元・口元ケア", "アイケア・アイクリーム", "Kiehl's", "キールズ クリーミー アイ トリートメント ウィズ アボカド", "アボカドオイル,βカロチン,グリセリン"),
    ("目元・口元ケア", "アイケア・アイクリーム", "ラロッシュポゼ", "ラロッシュポゼ レチノB3 アイセラム", "レチノール,ナイアシンアミド,ヒアルロン酸"),
    ("目元・口元ケア", "アイケア・アイクリーム", "The Inkey List", "The Inkey List カフェイン アイクリーム", "カフェイン,ペプチド,ヒアルロン酸"),
    ("目元・口元ケア", "まつげ美容液", "資生堂", "資生堂 アドバンスド ラッシュ ナリッシング セラム", "パンテノール,ケラチン,ビオチン"),
    ("目元・口元ケア", "リップケア・リップクリーム", "LANEIGE", "ラネージュ リップ グロウィング セラム", "ヒアルロン酸,セラミド,ビタミンE"),
    ("目元・口元ケア", "リップケア・リップクリーム", "ロート製薬", "メンソレータム リップ UVモイスト", "ヒアルロン酸,ミツロウ,アロエエキス"),
]


def init_db():
    conn = get_connection()
    c = conn.cursor()

    # ── User items ────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            brand TEXT NOT NULL,
            product_name TEXT NOT NULL,
            ingredients TEXT DEFAULT '[]',
            time_of_use TEXT NOT NULL DEFAULT '両方',
            memo TEXT DEFAULT '',
            sort_order INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    try:
        c.execute("ALTER TABLE items ADD COLUMN sort_order INTEGER DEFAULT 0")
    except Exception:
        pass

    # ── Master products ───────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS master_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            brand TEXT NOT NULL,
            product_name TEXT NOT NULL,
            key_ingredients TEXT DEFAULT ''
        )
    """)

    # Seed only once
    c.execute("SELECT COUNT(*) FROM master_products")
    if c.fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO master_products (category, subcategory, brand, product_name, key_ingredients) VALUES (?,?,?,?,?)",
            INITIAL_PRODUCTS,
        )

    conn.commit()
    conn.close()


# ─── User Items CRUD ──────────────────────────────────────────────────────────

def insert_item(category, subcategory, brand, product_name, ingredients, time_of_use, memo):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COALESCE(MAX(sort_order),0)+1 FROM items")
    next_order = c.fetchone()[0]
    ing_json = json.dumps(ingredients, ensure_ascii=False)
    c.execute(
        "INSERT INTO items (category,subcategory,brand,product_name,ingredients,time_of_use,memo,sort_order,created_at) VALUES (?,?,?,?,?,?,?,?,?)",
        (category, subcategory, brand, product_name, ing_json, time_of_use, memo, next_order, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_all_items():
    conn = get_connection()
    rows = [dict(r) for r in conn.execute("SELECT * FROM items ORDER BY sort_order ASC, created_at ASC")]
    conn.close()
    for r in rows:
        try:
            r["ingredients"] = json.loads(r["ingredients"])
        except Exception:
            r["ingredients"] = []
    return rows


def get_items_by_time(time_of_use):
    conn = get_connection()
    rows = [dict(r) for r in conn.execute(
        "SELECT * FROM items WHERE time_of_use=? OR time_of_use='両方' ORDER BY sort_order ASC, created_at ASC",
        (time_of_use,),
    )]
    conn.close()
    for r in rows:
        try:
            r["ingredients"] = json.loads(r["ingredients"])
        except Exception:
            r["ingredients"] = []
    return rows


def delete_item(item_id):
    conn = get_connection()
    conn.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()


def update_item(item_id, category, subcategory, brand, product_name, ingredients, time_of_use, memo):
    conn = get_connection()
    ing_json = json.dumps(ingredients, ensure_ascii=False)
    conn.execute(
        "UPDATE items SET category=?,subcategory=?,brand=?,product_name=?,ingredients=?,time_of_use=?,memo=? WHERE id=?",
        (category, subcategory, brand, product_name, ing_json, time_of_use, memo, item_id),
    )
    conn.commit()
    conn.close()


def update_sort_order(item_id, new_order):
    conn = get_connection()
    conn.execute("UPDATE items SET sort_order=? WHERE id=?", (new_order, item_id))
    conn.commit()
    conn.close()


def get_item_by_id(item_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
    conn.close()
    if not row:
        return None
    row = dict(row)
    try:
        row["ingredients"] = json.loads(row["ingredients"])
    except Exception:
        row["ingredients"] = []
    return row


# ─── Master Products ──────────────────────────────────────────────────────────

def search_master_products(query="", category="", subcategory=""):
    conn = get_connection()
    sql = "SELECT * FROM master_products WHERE 1=1"
    params = []
    if query:
        q = f"%{query}%"
        sql += " AND (product_name LIKE ? OR brand LIKE ? OR key_ingredients LIKE ?)"
        params += [q, q, q]
    if category:
        sql += " AND category=?"
        params.append(category)
    if subcategory:
        sql += " AND subcategory=?"
        params.append(subcategory)
    sql += " ORDER BY brand, product_name LIMIT 60"
    rows = [dict(r) for r in conn.execute(sql, params)]
    conn.close()
    return rows


def get_master_product_by_id(pid):
    conn = get_connection()
    row = conn.execute("SELECT * FROM master_products WHERE id=?", (pid,)).fetchone()
    conn.close()
    return dict(row) if row else None
