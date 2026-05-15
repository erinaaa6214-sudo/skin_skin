# utils.py

CATEGORIES = {
    "洗顔料": ["洗顔石鹸", "洗顔フォーム", "洗顔パウダー", "その他洗顔料"],
    "乳液・美容液・フェイスクリームなど": ["美容液", "乳液", "フェイスクリーム", "フェイスオイル・バーム", "オールインワン化粧品"],
    "クレンジング": ["オイルクレンジング", "ミルククレンジング", "クレンジングジェル", "リキッドクレンジング", "クレンジングクリーム", "ポイントメイクリムーバー", "クレンジングバーム", "クレンジングシート", "その他クレンジング"],
    "化粧水": ["化粧水", "ミスト状化粧水", "ブースター・導入液"],
    "パック・フェイスマスク": ["洗い流すパック・マスク", "シートマスク・パック", "ゴマージュ・ピーリング", "マッサージ料", "スリーピングマスク・パック"],
    "目元・口元ケア": ["アイケア・アイクリーム", "まつげ美容液", "リップケア・リップクリーム"],
    "その他スキンケア": ["その他スキンケア"],
}

TIME_OPTIONS = ["朝", "夜", "両方"]

# カテゴリアイコン
CATEGORY_ICONS = {
    "洗顔料": "🫧",
    "乳液・美容液・フェイスクリームなど": "💎",
    "クレンジング": "✨",
    "化粧水": "💧",
    "パック・フェイスマスク": "🌿",
    "目元・口元ケア": "👁️",
    "その他スキンケア": "☀️",
}

# ─────────────────────────────────────────────────────────────────────────────
# 相性診断ルール
# ─────────────────────────────────────────────────────────────────────────────
CONFLICT_RULES = [
    {
        "name": "レチノール ＋ AHA/BHA",
        "keywords_a": ["レチノール", "レチノイン酸", "retinol", "retinoid"],
        "keywords_b": ["AHA", "BHA", "グリコール酸", "サリチル酸", "乳酸", "マンデル酸", "glycolic acid", "salicylic acid", "lactic acid"],
        "severity": "danger",
        "reason": "両者とも肌のターンオーバーを強く促進します。同時使用は過剰な刺激・赤み・皮剥けの原因に。使用するなら時間帯を分けて（AHAは朝、レチノールは夜）。",
    },
    {
        "name": "高濃度ビタミンC ＋ ナイアシンアミド",
        "keywords_a": ["ビタミンC", "アスコルビン酸", "L-アスコルビン酸", "ascorbic acid", "vitamin c"],
        "keywords_b": ["ナイアシンアミド", "niacinamide", "nicotinamide"],
        "severity": "caution",
        "reason": "高濃度（20%以上）のビタミンCとナイアシンアミドを同時使用すると、ニコチン酸（肌荒れ成分）に変化する可能性があります。低濃度なら問題ない場合も多いです。",
    },
    {
        "name": "レチノール ＋ ビタミンC",
        "keywords_a": ["レチノール", "レチノイン酸", "retinol"],
        "keywords_b": ["ビタミンC", "アスコルビン酸", "L-アスコルビン酸", "ascorbic acid", "vitamin c"],
        "severity": "caution",
        "reason": "pH域が異なるため互いの効果を打ち消し合う可能性があります。ビタミンCは朝、レチノールは夜の使用が推奨されます。",
    },
    {
        "name": "ピーリング ＋ レチノール",
        "keywords_a": ["ピーリング", "ゴマージュ", "AHA", "BHA", "グリコール酸", "サリチル酸"],
        "keywords_b": ["レチノール", "レチノイン酸", "retinol"],
        "severity": "danger",
        "reason": "ピーリング成分とレチノールの組み合わせは肌バリアを過度に破壊します。別日に使用することを強く推奨します。",
    },
    {
        "name": "ベンゾイルパーオキサイド ＋ レチノール",
        "keywords_a": ["ベンゾイルパーオキサイド", "過酸化ベンゾイル", "benzoyl peroxide"],
        "keywords_b": ["レチノール", "レチノイン酸", "retinol"],
        "severity": "danger",
        "reason": "ベンゾイルパーオキサイドはレチノールを酸化・分解します。効果が失われるだけでなく、肌への刺激も増加します。",
    },
    {
        "name": "複数のピーリング成分の重複",
        "keywords_a": ["AHA", "グリコール酸", "乳酸", "マンデル酸"],
        "keywords_b": ["BHA", "サリチル酸", "ゴマージュ", "ピーリング"],
        "severity": "caution",
        "reason": "複数のピーリング成分を重ねると過剰な剥離でバリア機能が低下するリスクがあります。使用頻度に注意しましょう。",
    },
]


def normalize(text):
    return text.lower().replace("　", " ").strip()


def check_compatibility(items):
    conflicts = []
    all_items = [(item["product_name"], [normalize(i) for i in item["ingredients"]]) for item in items]

    for rule in CONFLICT_RULES:
        kw_a = [normalize(k) for k in rule["keywords_a"]]
        kw_b = [normalize(k) for k in rule["keywords_b"]]
        items_with_a, items_with_b = [], []
        for name, ings in all_items:
            if any(any(kw in ing for ing in ings) for kw in kw_a):
                items_with_a.append(name)
            if any(any(kw in ing for ing in ings) for kw in kw_b):
                items_with_b.append(name)
        if items_with_a and items_with_b:
            for a in items_with_a:
                for b in items_with_b:
                    if a != b:
                        conflicts.append({
                            "name": rule["name"],
                            "severity": rule["severity"],
                            "reason": rule["reason"],
                            "item_a": a,
                            "item_b": b,
                        })

    seen, deduped = set(), []
    for c in conflicts:
        key = (c["name"], frozenset([c["item_a"], c["item_b"]]))
        if key not in seen:
            seen.add(key)
            deduped.append(c)
    return deduped


# ─────────────────────────────────────────────────────────────────────────────
# レコメンド
# ─────────────────────────────────────────────────────────────────────────────
def generate_recommendations(items):
    recs = []
    all_ings = []
    for item in items:
        all_ings.extend([normalize(i) for i in item["ingredients"]])

    has_morning   = any(item["time_of_use"] in ["朝", "両方"] for item in items)
    has_evening   = any(item["time_of_use"] in ["夜", "両方"] for item in items)
    has_spf       = any("spf" in i or "日焼け止め" in i or "uvカット" in i or "紫外線" in i for i in all_ings)
    has_retinol   = any("レチノール" in i or "retinol" in i for i in all_ings)
    has_vit_c     = any("ビタミンc" in i or "アスコルビン酸" in i for i in all_ings)
    has_hyaluron  = any("ヒアルロン酸" in i or "hyaluronic" in i for i in all_ings)
    has_niacin    = any("ナイアシンアミド" in i or "niacinamide" in i for i in all_ings)
    has_ceramide  = any("セラミド" in i or "ceramide" in i for i in all_ings)

    if not has_spf:
        recs.append({"icon": "☀️", "title": "SPF（日焼け止め）の導入を", "detail": "紫外線は肌老化の最大の原因。朝のルーティンにSPF30以上の日焼け止めを追加するとシミ・シワ予防に大きな効果があります。", "suggestions": ["アネッサ パーフェクトUV", "ビオレUV アクアリッチ", "ラロッシュポゼ アンテリオス"]})
    if not has_retinol:
        recs.append({"icon": "✨", "title": "レチノールでエイジングケアを", "detail": "レチノール（ビタミンA誘導体）はシワ・ハリ改善に最もエビデンスのある成分。夜のルーティンに少量から導入しましょう。", "suggestions": ["The Ordinary レチノール 0.5%", "エリクシール リンクルクリームS", "ラロッシュポゼ レチノB3 アイセラム"]})
    if not has_vit_c:
        recs.append({"icon": "🍋", "title": "ビタミンCでくすみ・美白ケアを", "detail": "ビタミンCは抗酸化・美白・コラーゲン合成促進に優れた成分。朝に使うと紫外線ダメージの軽減にも役立ちます。", "suggestions": ["メラノCC 薬用しみ集中対策美容液", "ONE BY KOSÉ ザ ローション", "Kiehl's パワー ストレングス コンセントレート"]})
    if not has_hyaluron:
        recs.append({"icon": "💧", "title": "ヒアルロン酸で保湿力をアップ", "detail": "優れた保湿成分で肌のふっくら感・水分保持に役立ちます。化粧水や美容液に含まれることが多いです。", "suggestions": ["肌ラボ 極潤ヒアルロン液", "ナチュリエ ハトムギ化粧水", "The Ordinary ナイアシンアミド トナー"]})
    if not has_ceramide:
        recs.append({"icon": "🛡️", "title": "セラミドでバリア機能を強化", "detail": "肌のバリア機能を構成する脂質。肌荒れ・乾燥・敏感肌に悩む方に特におすすめです。", "suggestions": ["CeraVe モイスチャライジングクリーム", "キュレル 潤浸保湿 化粧水", "dプログラム バランスケア ローション"]})
    if not has_niacin:
        recs.append({"icon": "🌸", "title": "ナイアシンアミドで毛穴・トーンアップ", "detail": "毛穴の目立ちを抑え、肌色を均一にし、皮脂コントロールに効果的なビタミンB3の一種です。", "suggestions": ["The Ordinary ナイアシンアミド 10%", "CeraVe モイスチャライジングクリーム", "dプログラム バランスケア ローション"]})
    if items and not has_morning:
        recs.append({"icon": "🌅", "title": "朝ルーティンを始めましょう", "detail": "朝用または両用アイテムが登録されていません。洗顔→化粧水→美容液→日焼け止めの4ステップがおすすめです。", "suggestions": []})
    if items and not has_evening:
        recs.append({"icon": "🌙", "title": "夜ルーティンを充実させましょう", "detail": "夜は肌の修復・再生が活発な時間帯。クレンジング→洗顔→美容液→クリームの流れを意識しましょう。", "suggestions": []})
    if not items:
        recs.append({"icon": "📝", "title": "まずはアイテムを登録しましょう", "detail": "「アイテム登録」からスキンケアアイテムを追加すると、パーソナライズされたアドバイスが表示されます。", "suggestions": []})
    return recs
