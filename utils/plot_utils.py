import matplotlib.pyplot as plt
import numpy as np
from typing import List
from models.character import Character, STATS, RANKS
import streamlit as st
import logging
import matplotlib.font_manager as fm

logger = logging.getLogger(__name__)

def plot_radar_chart(characters: List[Character], selected_indices: List[int]) -> plt.Figure:
    """レーダーチャートを描画する"""
    # フォント設定
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    japanese_fonts = ["MS Gothic", "Yu Gothic", "Noto Sans CJK JP"]
    selected_font = None
    for font in japanese_fonts:
        if font in available_fonts:
            selected_font = font
            break
    
    if selected_font:
        plt.rcParams["font.family"] = selected_font
        logger.info(f"Using font: {selected_font}")
    else:
        logger.warning(
            "日本語フォントが見つかりません。以下のフォントをインストールしてください: "
            f"{', '.join(japanese_fonts)}. フォールバックフォントを使用。"
        )
        plt.rcParams["font.family"] = "sans-serif"

    # ダークテーマ設定
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})
    ax.set_facecolor('#1B263B')
    fig.patch.set_facecolor('#1B263B')
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    angles = np.linspace(0, 2 * np.pi, len(STATS), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    for idx in selected_indices:
        char = characters[idx]
        values = [RANKS.index(char.stats[stat]) for stat in STATS]
        values += values[:1]
        ax.plot(angles, values, label=f"{char.name} ({char.job})", color='#FFD700', linewidth=2)
        ax.fill(angles, values, alpha=0.2, facecolor='#FFD700')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(STATS, color='#D9E4EC', size=12)
    ax.set_yticks(range(len(RANKS)))
    ax.set_yticklabels(RANKS, color='#D9E4EC')
    ax.grid(color='#C0C0C0', linestyle='--', alpha=0.5)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), facecolor='#0D1B2A', edgecolor='#C0C0C0', labelcolor='#D9E4EC')
    return fig