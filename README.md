<div align="center">

  <img src="assets/character-py-logo.png" alt="Character.pyロゴ" width="600">

  <h1>Character.py</h1>

  <span>
    <a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&style=for-the-badge" alt="Python"></a>
    <a href="https://streamlit.io"><img src="https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B?logo=streamlit&style=for-the-badge" alt="Streamlit"></a>
    <a href="https://matplotlib.org"><img src="https://img.shields.io/badge/Matplotlib-3.9.2-blue?logo=matplotlib&style=for-the-badge" alt="Matplotlib"></a>
    <a href="https://github.com/hemlok-ai/character-py/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License"></a>
  </span>

</div>

  

## 概要

  

- **Character.py**は、キャラクターステータス作成ツールです。
- [Streamlit](https://streamlit.io)と[Python](https://www.python.org)で構築されており、職業ごとの絵文字アイコン、レーダーチャートによるステータス可視化を特徴とします。
- 勇者、賢者、錬金術師などの職業でキャラクターを作成、保存、比較できます。

  

主な機能：

- **動的ステータス生成**：職業ごとのボーナス（+2/-2）付きで自動生成。

- **カスタマイズ可能なUI**：ダークブルーUI、白単色のタイトル、単色の金ボタン、絵文字アイコン。

- **インタラクティブな可視化**：キャラクターのステータス比較用レーダーチャート。

- **データ管理**：JSON/Markdown形式でのキャラクターのエクスポート/インポート。
  

## インストール

  

### 前提条件

- Python 3.8以上（[ダウンロード](https://www.python.org/downloads/)）

- Git（[ダウンロード](https://git-scm.com/downloads/)）

  

### 手順

1. リポジトリをクローン：

   ```bash

   git clone https://github.com/hemlok-ai/character-py.git

   cd character-py

   ```

  

2. 仮想環境を作成・有効化：

   ```bash

   python -m venv venv

   source venv/bin/activate  # Windows: venv\Scripts\activate

   ```

  

3. 依存関係をインストール：

   ```bash

   pip install -r requirements.txt

   ```

  

4. （オプション）Linux用の日本語フォントをインストール：

   ```bash

   sudo apt install fonts-noto-cjk

   ```

  

5. Matplotlibのフォントキャッシュをクリア：

   ```bash

   rm -rf ~/.cache/matplotlib  # Windows: del /S %USERPROFILE%\.cache\matplotlib

   ```

  

## 使用方法

  

1. アプリケーションを起動：

   ```bash

   streamlit run app.py

   ```

  

2. ブラウザで`http://localhost:8501`を開く。

  

3. キャラクター作成：

   - 名前を入力（例：「テスト・テストス」）。

   - 職業を選択（例：🪄賢者）。

   - ステータスを自動生成または手動で設定（SS～F）。

   - キャラクターを保存、コピー、削除。

   - レーダーチャートでステータスを比較。

  

## カスタマイズ

  

- **タイトル**：`app.py`を編集：

  ```python

  st.title("異世界ステータス作成ツール")  # 日本語タイトルに変更

  ```

- **テーマ**：`.streamlit/config.toml`を変更：

  ```toml

  primaryColor = "#8B0000"  # 赤いアクセントに変更

  ```

- **ボタン**：`static/styles.css`を調整：

  ```css

  .stButton > button { background: #8B0000; }  # 赤いボタン

  .stButton > button:hover { transform: scale(1.05); }  # ホバー時の拡大を微調整

  ```

- **職業アイコン**：`data/classes.json`を更新：

  ```json

  "賢者": {"icon": "🔮", "bonuses": {"魔力適性": 2, "技術理解": 2, "物理攻撃": -2}}

  ```

- **フォント**：`static/styles.css`を変更：

  ```css

  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');

  h1 { font-family: 'Roboto', serif; }

  ```
  

## プロジェクト構造

  

```

├── app.py                    # メインのStreamlitアプリ

├── models/

│   └── character.py          # キャラクタークラスとロジック

├── utils/

│   ├── data_manager.py       # キャラクターデータ管理

│   └── plot_utils.py         # レーダーチャート描画

├── data/

│   ├── classes.json          # 職業データ（アイコン、ボーナス）

│   └── ranks.json            # ステータスランク（SS～F）

├── .streamlit/

│   └── config.toml           # テーマ設定

├── static/

│   └── styles.css            # カスタムCSS

├── assets/

│   └── character-py-logo.png # README用ロゴ

├── requirements.txt          # 依存関係

├── README.md                 # プロジェクトドキュメント

```

  

## ライセンス

  

このプロジェクトはMITライセンスの下で公開されています。詳細は[ライセンス](https://github.com/hemlok-ai/character-py/blob/main/LICENSE)を参照。

  

## リンク

  

- **リポジトリ**: [https://github.com/hemlok-ai/character-py](https://github.com/hemlok-ai/character-py)

- **Python**: [https://www.python.org](https://www.python.org)

- **Streamlit**: [https://streamlit.io](https://streamlit.io)
  

---