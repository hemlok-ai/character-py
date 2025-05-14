import streamlit as st
import json
import sys
from models.character import Character, STATS, CLASSES, RANKS
from utils.data_manager import load_characters, save_characters
from utils.plot_utils import plot_radar_chart
import logging

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定数
MAX_NAME_LENGTH = 50

def validate_name(name: str) -> bool:
    """キャラクター名のバリデーション"""
    if not name or len(name) > MAX_NAME_LENGTH:
        st.error(f"キャラクター名は1～{MAX_NAME_LENGTH}文字で入力してください")
        return False
    return True

def main():
    """メインのStreamlitアプリ"""
    st.set_page_config(page_title="Chronicles of Otherworld: Status Forge", layout="wide")

    # CSS読み込み
    with open("static/styles.css", "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    st.title("Character.py")

    # 初期化
    if "characters" not in st.session_state:
        st.session_state.characters = load_characters()
    if "form_stats" not in st.session_state:
        st.session_state.form_stats = {stat: "C" for stat in STATS}
    if "rerun_trigger" not in st.session_state:
        st.session_state.rerun_trigger = False

    # キャラクター新規作成
    with st.expander("キャラクター新規作成", expanded=True):
        with st.form("character_form"):
            name = st.text_input("キャラクター名", "Kaito Chronos")
            # 職業選択にアイコン（<span>を削除）
            job_options = [(f"{CLASSES[job]['icon']} {job}", job) for job in CLASSES]
            job_display = st.selectbox("職業", job_options, format_func=lambda x: x[0], help="職業を選択")
            job = job_display[1] if job_display else list(CLASSES.keys())[0]
            stats = {}
            cols = st.columns(4)
            for i, stat in enumerate(STATS):
                stats[stat] = cols[i % 4].selectbox(
                    stat,
                    RANKS,
                    index=RANKS.index(st.session_state.form_stats.get(stat, "C")),
                    key=f"stat_{stat}"
                )
            auto_generate = st.form_submit_button("自動生成")
            save = st.form_submit_button("保存")

            if auto_generate:
                if validate_name(name):
                    char = Character(name, job)
                    char.auto_generate()
                    st.session_state.form_stats = char.stats
                    st.success("ステータスを自動生成しました！")
            if save:
                if validate_name(name):
                    char = Character(name, job)
                    char.stats = stats
                    st.session_state.characters.append(char)
                    save_characters(st.session_state.characters)
                    st.session_state.form_stats = {stat: "C" for stat in STATS}
                    st.success(f"{char.name} を保存しました！")

    # 保存されたキャラクター
    selected_indices = []
    with st.expander("保存されたキャラクター", expanded=True):
        if not st.session_state.characters:
            st.info("保存されたキャラクターがありません")
        else:
            cols = st.columns(3)
            for i, char in enumerate(st.session_state.characters):
                with cols[i % 3]:
                    with st.container(border=False):
                        st.markdown(
                            f"""
                            <div class="character-card">
                                <h4><span class='job-icon'>{CLASSES[char.job]['icon']}</span>{char.name} ({char.job})</h4>
                                <p style='color: #D9E4EC; font-size: 12px;'>作成: {char.created_at}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        if st.checkbox("比較対象", key=f"compare_{i}"):
                            selected_indices.append(i)
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("コピー", key=f"copy_{i}"):
                                new_char = Character(f"{char.name}のコピー", char.job)
                                new_char.stats = char.stats.copy()
                                st.session_state.characters.append(new_char)
                                save_characters(st.session_state.characters)
                                if not st.session_state.rerun_trigger:
                                    st.session_state.rerun_trigger = True
                                    st.rerun()
                        with col2:
                            if st.button("削除", key=f"delete_{i}"):
                                st.session_state.characters.pop(i)
                                save_characters(st.session_state.characters)
                                if not st.session_state.rerun_trigger:
                                    st.session_state.rerun_trigger = True
                                    st.rerun()

    # キャラクター比較
    if selected_indices:
        st.divider()
        st.subheader("キャラクター比較")
        compare_data = [
            {
                "名前": char.name,
                "職業": char.job,
                **{stat: char.stats[stat] for stat in STATS},
                "合計": sum(RANKS.index(v) for v in char.stats.values())
            }
            for idx, char in enumerate(st.session_state.characters) if idx in selected_indices
        ]
        st.dataframe(compare_data, hide_index=True)
        fig = plot_radar_chart(st.session_state.characters, selected_indices)
        st.pyplot(fig)

    # データ管理
    with st.expander("データ管理"):
        tab1, tab2 = st.tabs(["エクスポート", "インポート"])
        with tab1:
            data = [{"name": c.name, "stats": c.stats, "job": c.job, "created_at": c.created_at} for c in st.session_state.characters]
            st.download_button(
                label="JSON形式でエクスポート",
                data=json.dumps(data, ensure_ascii=False, indent=2),
                file_name="characters.json",
                mime="application/json"
            )
            markdown = "\n".join([
                f"## {char.name} ({char.job})\n\n" +
                "| " + " | ".join(["ステータス"] + STATS) + " |\n" +
                "|-" + "-|-" * len(STATS) + "|\n" +
                "| " + " | ".join(["ランク"] + [char.stats[stat] for stat in STATS]) + " |"
                for char in st.session_state.characters
            ])
            st.download_button(
                label="Markdown形式でエクスポート",
                data=markdown,
                file_name="characters.md",
                mime="text/markdown"
            )
        with tab2:
            uploaded_file = st.file_uploader("JSONファイルをアップロード", type="json")
            if uploaded_file:
                try:
                    imported_data = json.load(uploaded_file)
                    st.session_state.characters = [
                        Character(data["name"], data.get("job", "村人"), data.get("created_at")) for data in imported_data
                    ]
                    save_characters(st.session_state.characters)
                    st.success(f"{len(imported_data)} 件のキャラクターをインポートしました！")
                except json.JSONDecodeError as e:
                    st.error(f"JSONファイルが壊れています: {e}")
                except Exception as e:
                    st.error(f"インポートエラー: {e}")

    # リセット rerun_trigger
    st.session_state.rerun_trigger = False

if __name__ == "__main__":
    main()