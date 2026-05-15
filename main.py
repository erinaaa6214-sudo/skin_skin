import streamlit as st
import hashlib
from collections import defaultdict, Counter

from database import (
    init_db, insert_item, get_all_items, get_items_by_time,
    delete_item, update_item, get_item_by_id, update_sort_order,
    search_master_products, get_master_product_by_id,
)
from utils import CATEGORIES, CATEGORY_ICONS, TIME_OPTIONS, check_compatibility, generate_recommendations

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="My Skin Routine",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# ─────────────────────────────────────────────────────────────────────────────
# Global CSS — Luxury Editorial Aesthetic
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── App Background ──────────────────────────────── */
.stApp {
    background: #FAF7F5;
    min-height: 100vh;
}
.block-container {
    padding: 2rem 2.5rem 4rem 2.5rem !important;
    max-width: 1200px;
}

/* ── Sidebar ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #1C1412 !important;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #EDE8E3 !important; }
[data-testid="stSidebar"] .block-container { padding: 0 !important; }

/* ── Sidebar Nav Buttons ─────────────────────────── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #C8A99A !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 1.8rem !important;
    width: 100% !important;
    text-align: left !important;
    border-radius: 0 !important;
    transition: all 0.2s ease !important;
    border-left: 2px solid transparent !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(200,169,154,0.1) !important;
    color: #EDE8E3 !important;
    border-left: 2px solid #C8A99A !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(200,169,154,0.15) !important;
    color: #EDE8E3 !important;
    border-left: 2px solid #C8A99A !important;
}

/* ── Page Title ──────────────────────────────────── */
.page-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #B08070;
    margin-bottom: 0.35rem;
}
.page-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 300;
    color: #1C1412;
    line-height: 1.05;
    margin-bottom: 0.1rem;
}
.page-title em {
    font-style: italic;
    color: #8B5E52;
}
.page-divider {
    width: 48px;
    height: 1px;
    background: linear-gradient(90deg, #C8A99A, transparent);
    margin: 1rem 0 2rem 0;
}

/* ── Cards ───────────────────────────────────────── */
.skin-card {
    background: #FFFFFF;
    border-radius: 4px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1rem;
    border: 1px solid #EDE8E3;
    box-shadow: 0 1px 3px rgba(28,20,18,0.04), 0 8px 24px rgba(28,20,18,0.05);
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    position: relative;
}
.skin-card:hover {
    box-shadow: 0 2px 6px rgba(28,20,18,0.06), 0 16px 40px rgba(28,20,18,0.09);
    transform: translateY(-1px);
}
.skin-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #C8A99A, #8B5E52);
    border-radius: 4px 0 0 4px;
}
.card-brand {
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #B08070;
    margin-bottom: 0.25rem;
}
.card-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #1C1412;
    line-height: 1.2;
    margin-bottom: 0.6rem;
}
.card-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0.6rem;
    align-items: center;
}
.tag {
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.7rem;
    border-radius: 2px;
    display: inline-block;
}
.tag-cat   { background: #FAF7F5; color: #8B5E52; border: 1px solid #EDE8E3; }
.tag-morn  { background: #FFF8F0; color: #C86400; border: 1px solid #FFE4C4; }
.tag-eve   { background: #F0F0F8; color: #3A3A7A; border: 1px solid #D4D4F0; }
.tag-both  { background: #F0F8F4; color: #1A6648; border: 1px solid #C4E8D4; }
.card-ingredients {
    font-size: 0.75rem;
    color: #9E8880;
    margin-top: 0.4rem;
    line-height: 1.5;
}
.card-memo {
    font-size: 0.78rem;
    color: #7A6860;
    margin-top: 0.5rem;
    font-style: italic;
    padding-top: 0.5rem;
    border-top: 1px solid #F0EBE8;
}
.card-step {
    position: absolute;
    top: 1.2rem;
    right: 1.4rem;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    font-weight: 300;
    color: #EDE8E3;
    line-height: 1;
    user-select: none;
}

/* ── Stat Boxes ──────────────────────────────────── */
.stat-row {
    display: flex;
    gap: 1px;
    margin-bottom: 2.5rem;
    background: #EDE8E3;
    border-radius: 4px;
    overflow: hidden;
}
.stat-box {
    flex: 1;
    background: #FFFFFF;
    padding: 1.4rem 1rem;
    text-align: center;
}
.stat-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.8rem;
    font-weight: 300;
    color: #1C1412;
    line-height: 1;
}
.stat-label {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #B08070;
    margin-top: 0.35rem;
}

/* ── Section Header ──────────────────────────────── */
.section-hd {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 300;
    color: #1C1412;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #EDE8E3;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Conflict Cards ──────────────────────────────── */
.conflict-card {
    border-radius: 4px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    border-left: 4px solid;
}
.conflict-danger {
    background: #FFF5F5;
    border-color: #C84040;
    border: 1px solid #F8D0D0;
    border-left: 4px solid #C84040;
}
.conflict-caution {
    background: #FFFBF0;
    border-color: #C88000;
    border: 1px solid #F8E4A0;
    border-left: 4px solid #C88000;
}
.conflict-title { font-weight: 500; font-size: 0.9rem; margin-bottom: 0.35rem; }
.conflict-danger .conflict-title  { color: #8B2020; }
.conflict-caution .conflict-title { color: #7A5000; }
.conflict-items  { font-size: 0.78rem; color: #666; margin-bottom: 0.4rem; }
.conflict-reason { font-size: 0.82rem; color: #444; line-height: 1.5; }

/* ── Rec Cards ───────────────────────────────────── */
.rec-card {
    background: #FFFFFF;
    border: 1px solid #EDE8E3;
    border-radius: 4px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 2px 12px rgba(28,20,18,0.04);
}
.rec-icon  { font-size: 1.4rem; margin-bottom: 0.4rem; }
.rec-title { font-family: 'Cormorant Garamond', serif; font-size: 1.05rem; font-weight: 600; color: #1C1412; margin-bottom: 0.35rem; }
.rec-detail { font-size: 0.82rem; color: #6A5A54; line-height: 1.6; margin-bottom: 0.4rem; }
.rec-sugg  { font-size: 0.75rem; color: #B08070; font-style: italic; }

/* ── Login ───────────────────────────────────────── */
.login-outer {
    min-height: 85vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
.login-box {
    width: 380px;
    background: #FFFFFF;
    border-radius: 4px;
    padding: 3rem 2.5rem;
    box-shadow: 0 4px 40px rgba(28,20,18,0.10);
    text-align: center;
}
.login-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 300;
    color: #1C1412;
    letter-spacing: 0.05em;
}
.login-logo em { font-style: italic; color: #8B5E52; }
.login-sub {
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #B08070;
    margin: 0.4rem 0 2rem 0;
}

/* ── Product DB card ─────────────────────────────── */
.prod-card {
    background: #FDFAF8;
    border: 1px solid #EDE8E3;
    border-radius: 4px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
}
.prod-card:hover { background: #FFF0EB; border-color: #C8A99A; }
.prod-card-brand { font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; color: #B08070; }
.prod-card-name  { font-family: 'Cormorant Garamond', serif; font-size: 1rem; font-weight: 600; color: #1C1412; }
.prod-card-ing   { font-size: 0.72rem; color: #9E8880; margin-top: 0.2rem; }

/* ── Empty state ─────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #C8A99A;
}
.empty-icon  { font-size: 2.5rem; margin-bottom: 0.8rem; }
.empty-label { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; font-weight: 300; }

/* ── Streamlit widget overrides ──────────────────── */
.stTextInput > div > input,
.stTextArea > div > textarea,
.stSelectbox > div > div {
    border-color: #EDE8E3 !important;
    border-radius: 4px !important;
    background: #FFFFFF !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextInput > div > input:focus,
.stTextArea > div > textarea:focus {
    border-color: #C8A99A !important;
    box-shadow: 0 0 0 2px rgba(200,169,154,0.15) !important;
}
.stButton > button {
    border-radius: 2px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
    background: #1C1412 !important;
    color: #EDE8E3 !important;
    border: 1px solid #1C1412 !important;
}
.stButton > button[kind="primary"]:hover {
    background: #3A2A24 !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #8B5E52 !important;
    border: 1px solid #C8A99A !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #FAF0EB !important;
}
.stRadio > div { gap: 0.8rem !important; }
div[data-baseweb="tab-list"] {
    border-bottom: 1px solid #EDE8E3 !important;
    gap: 0 !important;
    background: transparent !important;
}
div[data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #B08070 !important;
    padding: 0.6rem 1.4rem !important;
    border-radius: 0 !important;
}
div[aria-selected="true"][data-baseweb="tab"] {
    color: #1C1412 !important;
    border-bottom: 2px solid #1C1412 !important;
}
.stAlert { border-radius: 4px !important; }
.stExpander { border: 1px solid #EDE8E3 !important; border-radius: 4px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────────────────────────────────────
PASSWORD_HASH = hashlib.sha256("skincare2024".encode()).hexdigest()

def check_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest() == PASSWORD_HASH

def login_page():
    st.markdown('<div class="login-outer">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="login-box">
            <div class="login-logo">My Skin <em>Routine</em></div>
            <div class="login-sub">あなただけのスキンケア記録帳</div>
        </div>
        """, unsafe_allow_html=True)
        pw = st.text_input("", type="password", placeholder="パスワードを入力してください", key="login_pw", label_visibility="collapsed")
        if st.button("ログイン", use_container_width=True, type="primary"):
            if check_password(pw):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("パスワードが違います")
        st.caption("初期パスワード：skincare2024")
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "ホーム"
if "edit_id" not in st.session_state:
    st.session_state["edit_id"] = None
if "prefill" not in st.session_state:
    st.session_state["prefill"] = None

if not st.session_state["authenticated"]:
    login_page()
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 2.5rem 1.8rem 1.5rem 1.8rem; border-bottom: 1px solid #2E2018;">
        <div style="font-family:'Cormorant Garamond',serif; font-size:1.6rem; font-weight:300; color:#EDE8E3; letter-spacing:0.05em; line-height:1.1;">
            My Skin<br><em style="font-style:italic; color:#C8A99A;">Routine</em>
        </div>
        <div style="font-size:0.6rem; letter-spacing:0.2em; text-transform:uppercase; color:#6A5040; margin-top:0.5rem;">
            Skincare Journal
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

    nav_items = [
        ("ホーム", "Home"),
        ("登録", "Register"),
        ("朝", "Morning"),
        ("夜", "Evening"),
        ("診断", "Analysis"),
        ("レコメンド", "Recommend"),
    ]
    labels_jp = {"ホーム": "🏠  ホーム", "登録": "＋  アイテム登録", "朝": "☀  朝ルーティン", "夜": "🌙  夜ルーティン", "診断": "⬡  相性診断", "レコメンド": "✦  レコメンド"}
    for key, _ in nav_items:
        active = st.session_state["page"] == key
        if st.button(labels_jp[key], use_container_width=True, type="primary" if active else "secondary", key=f"nav_{key}"):
            st.session_state["page"] = key
            st.session_state["edit_id"] = None
            st.session_state["prefill"] = None
            st.rerun()

    st.markdown('<div style="position:absolute;bottom:2rem;width:calc(100% - 0px);padding:0 1.8rem;">', unsafe_allow_html=True)
    st.markdown('<div style="height:60vh;"></div>', unsafe_allow_html=True)
    if st.button("⏏  ログアウト", use_container_width=True, type="secondary"):
        st.session_state["authenticated"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Helper: page header
# ─────────────────────────────────────────────────────────────────────────────
def page_header(eyebrow, title_plain, title_italic=""):
    st.markdown(f"""
    <div class="page-eyebrow">{eyebrow}</div>
    <div class="page-title">{title_plain}{"<em>" + title_italic + "</em>" if title_italic else ""}</div>
    <div class="page-divider"></div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Helper: render item card
# ─────────────────────────────────────────────────────────────────────────────
def time_tag(tou):
    cls = {"朝": "tag-morn", "夜": "tag-eve", "両方": "tag-both"}.get(tou, "tag-both")
    label = {"朝": "☀ 朝", "夜": "🌙 夜", "両方": "☀ 朝 ＋ 🌙 夜"}.get(tou, tou)
    return f'<span class="tag {cls}">{label}</span>'


def render_card(item, show_actions=True, step_num=None):
    ing_str = "　".join(item["ingredients"]) if item["ingredients"] else "—"
    step_html = f'<div class="card-step">{step_num:02d}</div>' if step_num else ""
    cat_icon = CATEGORY_ICONS.get(item["category"], "✦")
    memo_html = f'<div class="card-memo">📝 {item["memo"]}</div>' if item.get("memo") else ""

    st.markdown(f"""
    <div class="skin-card">
        {step_html}
        <div class="card-brand">{item['brand']}</div>
        <div class="card-name">{item['product_name']}</div>
        <div class="card-meta">
            <span class="tag tag-cat">{cat_icon} {item['subcategory']}</span>
            {time_tag(item['time_of_use'])}
        </div>
        <div class="card-ingredients">🧪 {ing_str}</div>
        {memo_html}
    </div>
    """, unsafe_allow_html=True)

    if show_actions:
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            if st.button("編集", key=f"edit_{item['id']}", type="secondary"):
                st.session_state["edit_id"] = item["id"]
                st.session_state["page"] = "登録"
                st.rerun()
        with c2:
            if st.button("削除", key=f"del_{item['id']}", type="secondary"):
                delete_item(item["id"])
                st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ホーム
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state["page"] == "ホーム":
    page_header("Skincare Journal", "My Skin ", "Routine")

    items   = get_all_items()
    morning = [i for i in items if i["time_of_use"] in ["朝", "両方"]]
    evening = [i for i in items if i["time_of_use"] in ["夜", "両方"]]
    danger_count = sum(1 for c in check_compatibility(items) if c["severity"] == "danger")

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-box"><div class="stat-number">{len(items)}</div><div class="stat-label">Total Items</div></div>
        <div class="stat-box"><div class="stat-number">{len(morning)}</div><div class="stat-label">Morning</div></div>
        <div class="stat-box"><div class="stat-number">{len(evening)}</div><div class="stat-label">Evening</div></div>
        <div class="stat-box"><div class="stat-number">{danger_count}</div><div class="stat-label">Alerts</div></div>
    </div>
    """, unsafe_allow_html=True)

    col_m, col_e = st.columns(2, gap="large")

    with col_m:
        st.markdown('<div class="section-hd">☀ 朝のルーティン</div>', unsafe_allow_html=True)
        if morning:
            for i, item in enumerate(morning[:5]):
                st.markdown(f"""
                <div class="skin-card" style="padding:1rem 1.3rem;">
                    <div class="card-step" style="font-size:1.4rem;">{i+1:02d}</div>
                    <div class="card-brand">{item['brand']}</div>
                    <div class="card-name" style="font-size:1.05rem;">{item['product_name']}</div>
                    <div class="card-meta" style="margin-bottom:0;">{time_tag(item['time_of_use'])}</div>
                </div>
                """, unsafe_allow_html=True)
            if len(morning) > 5:
                st.caption(f"他 {len(morning)-5} アイテム")
        else:
            st.markdown('<div class="empty-state"><div class="empty-icon">🌅</div><div class="empty-label">朝用アイテムがありません</div></div>', unsafe_allow_html=True)

    with col_e:
        st.markdown('<div class="section-hd">🌙 夜のルーティン</div>', unsafe_allow_html=True)
        if evening:
            for i, item in enumerate(evening[:5]):
                st.markdown(f"""
                <div class="skin-card" style="padding:1rem 1.3rem;">
                    <div class="card-step" style="font-size:1.4rem;">{i+1:02d}</div>
                    <div class="card-brand">{item['brand']}</div>
                    <div class="card-name" style="font-size:1.05rem;">{item['product_name']}</div>
                    <div class="card-meta" style="margin-bottom:0;">{time_tag(item['time_of_use'])}</div>
                </div>
                """, unsafe_allow_html=True)
            if len(evening) > 5:
                st.caption(f"他 {len(evening)-5} アイテム")
        else:
            st.markdown('<div class="empty-state"><div class="empty-icon">🌙</div><div class="empty-label">夜用アイテムがありません</div></div>', unsafe_allow_html=True)

    if danger_count > 0:
        st.markdown('<div class="section-hd">⚠ アラート</div>', unsafe_allow_html=True)
        conflicts = check_compatibility(items)
        for c in [x for x in conflicts if x["severity"] == "danger"][:3]:
            st.warning(f"🔴 **{c['name']}**｜{c['item_a']} × {c['item_b']} — 相性診断で詳細を確認してください")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: アイテム登録
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "登録":
    edit_id   = st.session_state.get("edit_id")
    item_data = get_item_by_id(edit_id) if edit_id else None
    prefill   = st.session_state.get("prefill")

    if edit_id:
        page_header("Edit Item", "アイテムを", "編集")
    else:
        page_header("Register Item", "アイテムを", "登録")

    # ── 人気商品から選ぶ ────────────────────────────────────────────────────
    if not edit_id:
        with st.expander("✦ 人気商品データベースから選ぶ（推奨）", expanded=not bool(prefill)):
            st.markdown('<div style="font-size:0.8rem;color:#9E8880;margin-bottom:1rem;">ブランド名・商品名・成分名で検索できます。選択すると自動入力されます。</div>', unsafe_allow_html=True)

            db_col1, db_col2, db_col3 = st.columns([2, 2, 1])
            with db_col1:
                db_search = st.text_input("🔍 キーワード検索", placeholder="例：キュレル、ヒアルロン酸", key="db_search")
            with db_col2:
                db_cat_opts = ["すべて"] + list(CATEGORIES.keys())
                db_cat = st.selectbox("カテゴリ絞り込み", db_cat_opts, key="db_cat")
            with db_col3:
                if db_cat != "すべて":
                    db_sub_opts = ["すべて"] + CATEGORIES[db_cat]
                    db_sub = st.selectbox("サブカテゴリ", db_sub_opts, key="db_sub")
                else:
                    db_sub = "すべて"
                    st.selectbox("サブカテゴリ", ["すべて"], disabled=True, key="db_sub_dis")

            results = search_master_products(
                query=db_search,
                category="" if db_cat == "すべて" else db_cat,
                subcategory="" if db_sub == "すべて" else db_sub,
            )

            if results:
                st.caption(f"{len(results)} 件見つかりました")
                for prod in results:
                    col_info, col_btn = st.columns([5, 1])
                    with col_info:
                        st.markdown(f"""
                        <div class="prod-card">
                            <div class="prod-card-brand">{prod['brand']} · {prod['subcategory']}</div>
                            <div class="prod-card-name">{prod['product_name']}</div>
                            <div class="prod-card-ing">🧪 {prod['key_ingredients']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_btn:
                        st.markdown('<div style="padding-top:0.6rem;"></div>', unsafe_allow_html=True)
                        if st.button("選択", key=f"pick_{prod['id']}", type="primary"):
                            st.session_state["prefill"] = {
                                "category":    prod["category"],
                                "subcategory": prod["subcategory"],
                                "brand":       prod["brand"],
                                "product_name": prod["product_name"],
                                "ingredients": prod["key_ingredients"],
                            }
                            st.rerun()
            else:
                st.markdown('<div style="color:#C8A99A;font-size:0.85rem;padding:1rem 0;">検索結果がありません。下のフォームから手動で入力してください。</div>', unsafe_allow_html=True)

    if prefill:
        st.success(f"✦ 「{prefill['product_name']}」を選択しました。内容を確認・編集してから保存してください。")

    st.markdown('<div class="section-hd">✦ アイテム詳細</div>', unsafe_allow_html=True)

    # ── 登録フォーム ────────────────────────────────────────────────────────
    # Default values from prefill / edit
    def_cat  = (prefill or item_data or {}).get("category", list(CATEGORIES.keys())[0])
    def_sub  = (prefill or item_data or {}).get("subcategory", "")
    def_brand = (prefill or item_data or {}).get("brand", "")
    def_name  = (prefill or item_data or {}).get("product_name", "")
    def_ings  = ""
    if prefill:
        def_ings = prefill.get("ingredients", "")
    elif item_data:
        def_ings = "、".join(item_data.get("ingredients", []))
    def_time  = (item_data or {}).get("time_of_use", "両方")
    def_memo  = (item_data or {}).get("memo", "")

    with st.form("item_form", clear_on_submit=False):
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            cat_list = list(CATEGORIES.keys())
            cat_idx  = cat_list.index(def_cat) if def_cat in cat_list else 0
            category = st.selectbox("カテゴリ ＊", cat_list, index=cat_idx, key="form_cat")
        with r1c2:
            sub_list = CATEGORIES[category]
            sub_idx  = sub_list.index(def_sub) if def_sub in sub_list else 0
            subcategory = st.selectbox("サブカテゴリ ＊", sub_list, index=sub_idx, key="form_sub")

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            brand = st.text_input("ブランド名 ＊", value=def_brand, placeholder="例：資生堂、SK-II、COSRX")
        with r2c2:
            product_name = st.text_input("商品名 ＊", value=def_name, placeholder="例：フェイシャル トリートメント エッセンス")

        ingredients_raw = st.text_area(
            "主な成分（カンマ or 読点区切り）",
            value=def_ings,
            placeholder="例：ヒアルロン酸、ナイアシンアミド、グリセリン",
            height=90,
        )

        time_opts_idx = TIME_OPTIONS.index(def_time) if def_time in TIME_OPTIONS else 2
        time_of_use = st.radio("使用タイミング ＊", TIME_OPTIONS, index=time_opts_idx, horizontal=True)

        memo = st.text_area("メモ（任意）", value=def_memo, placeholder="使用感・購入場所・リピート回数など", height=70)

        save_btn = st.form_submit_button("✦ 保存する", use_container_width=True, type="primary")

        if save_btn:
            if not brand.strip() or not product_name.strip():
                st.error("ブランド名と商品名は必須です")
            else:
                ings = [i.strip() for i in ingredients_raw.replace("、", ",").replace("　", ",").split(",") if i.strip()]
                if edit_id:
                    update_item(edit_id, category, subcategory, brand.strip(), product_name.strip(), ings, time_of_use, memo.strip())
                    st.session_state["edit_id"] = None
                    st.success("✦ アイテムを更新しました")
                else:
                    insert_item(category, subcategory, brand.strip(), product_name.strip(), ings, time_of_use, memo.strip())
                    st.success("✦ アイテムを登録しました")
                st.session_state["prefill"] = None
                st.rerun()

    if edit_id:
        if st.button("← 編集をキャンセル", type="secondary"):
            st.session_state["edit_id"] = None
            st.rerun()

    if prefill and not edit_id:
        if st.button("✕ 選択をクリア", type="secondary"):
            st.session_state["prefill"] = None
            st.rerun()

    # ── 登録済み一覧 ────────────────────────────────────────────────────────
    st.markdown('<div class="section-hd">✦ 登録済みアイテム一覧</div>', unsafe_allow_html=True)
    all_items = get_all_items()
    if all_items:
        fc1, fc2 = st.columns([3, 1])
        with fc1:
            q = st.text_input("🔍 絞り込み", placeholder="商品名・ブランドで検索", label_visibility="collapsed")
        with fc2:
            ft = st.selectbox("タイミング", ["すべて"] + TIME_OPTIONS, label_visibility="collapsed")

        filtered = all_items
        if q:
            ql = q.lower()
            filtered = [i for i in filtered if ql in i["product_name"].lower() or ql in i["brand"].lower()]
        if ft != "すべて":
            filtered = [i for i in filtered if i["time_of_use"] == ft]

        for item in filtered:
            render_card(item, show_actions=True)
    else:
        st.markdown('<div class="empty-state"><div class="empty-icon">📦</div><div class="empty-label">まだアイテムが登録されていません</div></div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: 朝 / 夜 ルーティン
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state["page"] in ["朝", "夜"]:
    is_morning = st.session_state["page"] == "朝"
    if is_morning:
        page_header("Morning Routine", "朝の ", "スキンケア")
        items = get_items_by_time("朝")
        icon  = "☀"
    else:
        page_header("Evening Routine", "夜の ", "スキンケア")
        items = get_items_by_time("夜")
        icon  = "🌙"

    tab_list, tab_cat = st.tabs([f"{icon}  ルーティン一覧", "📂  カテゴリ別"])

    with tab_list:
        if items:
            st.caption(f"全 {len(items)} ステップ　｜　⬆⬇ で順番を変更できます")
            for idx, item in enumerate(items):
                col_card, col_ctrl = st.columns([11, 1])
                with col_card:
                    render_card(item, show_actions=False, step_num=idx + 1)
                with col_ctrl:
                    st.markdown('<div style="padding-top:1.1rem;display:flex;flex-direction:column;gap:0.3rem;">', unsafe_allow_html=True)
                    if idx > 0 and st.button("▲", key=f"up_{item['id']}"):
                        prev = items[idx - 1]
                        update_sort_order(item["id"], prev["sort_order"])
                        update_sort_order(prev["id"], item["sort_order"])
                        st.rerun()
                    if idx < len(items) - 1 and st.button("▼", key=f"dn_{item['id']}"):
                        nxt = items[idx + 1]
                        update_sort_order(item["id"], nxt["sort_order"])
                        update_sort_order(nxt["id"], item["sort_order"])
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="empty-state"><div class="empty-icon">{icon}</div><div class="empty-label">{"朝" if is_morning else "夜"}用のアイテムがありません</div></div>', unsafe_allow_html=True)
            if st.button("✦ アイテムを登録する", type="primary"):
                st.session_state["page"] = "登録"
                st.rerun()

    with tab_cat:
        if items:
            by_cat = defaultdict(list)
            for item in items:
                by_cat[item["category"]].append(item)
            for cat, cat_items in by_cat.items():
                st.markdown(f'<div class="section-hd">{CATEGORY_ICONS.get(cat,"✦")} {cat}</div>', unsafe_allow_html=True)
                cols = st.columns(min(len(cat_items), 3), gap="medium")
                for ci, item in enumerate(cat_items):
                    with cols[ci % 3]:
                        ing_str = "　".join(item["ingredients"][:3]) + ("…" if len(item["ingredients"]) > 3 else "") if item["ingredients"] else "—"
                        st.markdown(f"""
                        <div class="skin-card" style="padding:1.1rem 1.3rem;">
                            <div class="card-brand">{item['brand']}</div>
                            <div class="card-name" style="font-size:1rem;">{item['product_name']}</div>
                            <div class="card-meta">{time_tag(item['time_of_use'])}</div>
                            <div class="card-ingredients" style="font-size:0.7rem;">🧪 {ing_str}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("アイテムがありません")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: 相性診断
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "診断":
    page_header("Compatibility Check", "成分 ", "相性診断")

    items = get_all_items()
    if not items:
        st.markdown('<div class="empty-state"><div class="empty-icon">🧪</div><div class="empty-label">アイテムを登録してから診断してください</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="font-size:0.85rem;color:#9E8880;margin-bottom:1.5rem;">現在 <strong>{len(items)}</strong> 件のアイテムの成分を解析中…</div>', unsafe_allow_html=True)

        conflicts = check_compatibility(items)
        danger  = [c for c in conflicts if c["severity"] == "danger"]
        caution = [c for c in conflicts if c["severity"] == "caution"]

        if not conflicts:
            st.success("✅ 危険な成分の組み合わせは検出されませんでした。現在のルーティンは安全です。")
            st.balloons()
        else:
            if danger:
                st.markdown('<div class="section-hd">🔴 要注意：使用を避けるべき組み合わせ</div>', unsafe_allow_html=True)
                for c in danger:
                    st.markdown(f"""
                    <div class="conflict-card conflict-danger">
                        <div class="conflict-title">🔴 {c['name']}</div>
                        <div class="conflict-items">対象：<strong>{c['item_a']}</strong> × <strong>{c['item_b']}</strong></div>
                        <div class="conflict-reason">{c['reason']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            if caution:
                st.markdown('<div class="section-hd">🟡 注意：使い方を工夫して</div>', unsafe_allow_html=True)
                for c in caution:
                    st.markdown(f"""
                    <div class="conflict-card conflict-caution">
                        <div class="conflict-title">🟡 {c['name']}</div>
                        <div class="conflict-items">対象：<strong>{c['item_a']}</strong> × <strong>{c['item_b']}</strong></div>
                        <div class="conflict-reason">{c['reason']}</div>
                    </div>
                    """, unsafe_allow_html=True)

        with st.expander("🧪 登録アイテムの全成分一覧"):
            for item in items:
                if item["ingredients"]:
                    st.markdown(f"**{item['product_name']}**（{item['brand']}）")
                    st.caption("　" + "　/　".join(item["ingredients"]))
                else:
                    st.markdown(f"**{item['product_name']}**（{item['brand']}）— *成分未登録*")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: レコメンド
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "レコメンド":
    page_header("Personalized Advice", "スキンケア ", "レコメンド")

    items = get_all_items()
    recs  = generate_recommendations(items)

    st.markdown(f'<div style="font-size:0.85rem;color:#9E8880;margin-bottom:1.5rem;">{len(items)} 件のアイテムをもとに、パーソナライズされたアドバイスをお届けします。</div>', unsafe_allow_html=True)

    if not recs:
        st.success("🎉 素晴らしいルーティンです！追加のアドバイスはありません。")
    else:
        cols = st.columns(2, gap="medium")
        for i, rec in enumerate(recs):
            sugg = ("💬 例：" + "　/　".join(rec["suggestions"])) if rec.get("suggestions") else ""
            with cols[i % 2]:
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-icon">{rec['icon']}</div>
                    <div class="rec-title">{rec['title']}</div>
                    <div class="rec-detail">{rec['detail']}</div>
                    {"<div class='rec-sugg'>" + sugg + "</div>" if sugg else ""}
                </div>
                """, unsafe_allow_html=True)

    if items:
        st.markdown('<div class="section-hd">📊 ルーティン成分マップ</div>', unsafe_allow_html=True)
        all_ings = []
        for item in items:
            all_ings.extend(item["ingredients"])
        if all_ings:
            counts = Counter(all_ings).most_common(18)
            cols3  = st.columns(3)
            for i, (ing, cnt) in enumerate(counts):
                with cols3[i % 3]:
                    bar_w = int(cnt / counts[0][1] * 100)
                    st.markdown(f"""
                    <div style="background:#FFFFFF;border:1px solid #EDE8E3;border-radius:4px;padding:0.65rem 1rem;margin-bottom:0.5rem;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="font-size:0.8rem;color:#1C1412;font-weight:500;">{ing}</span>
                            <span style="font-size:0.7rem;color:#B08070;">{cnt}件</span>
                        </div>
                        <div style="height:2px;background:#EDE8E3;border-radius:1px;margin-top:0.4rem;">
                            <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,#C8A99A,#8B5E52);border-radius:1px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("成分を登録するとここに分析が表示されます。")
