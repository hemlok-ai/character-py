import json
from typing import List
from models.character import Character
import streamlit as st
import logging

logger = logging.getLogger(__name__)

def load_characters() -> List[Character]:
    """キャラクターをJSONファイルから読み込む"""
    try:
        with open("characters.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Character(data["name"], data.get("job", "村人"), data.get("created_at")) for data in data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        st.error(f"JSONファイルが壊れています: {e}")
        return []
    except Exception as e:
        logger.error(f"キャラクター読み込みエラー: {e}")
        st.error(f"読み込みエラー: {e}")
        return []

def save_characters(characters: List[Character]) -> None:
    """キャラクターをJSONファイルに保存する"""
    try:
        data = [{"name": c.name, "stats": c.stats, "job": c.job, "created_at": c.created_at} for c in characters]
        with open("characters.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(characters)} characters")
    except Exception as e:
        logger.error(f"キャラクター保存エラー: {e}")
        st.error(f"保存エラー: {e}")
        raise