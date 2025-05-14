import random
import json
from datetime import datetime
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

# 定数定義
STATS = ["魔力適性", "魔法制御", "物理攻撃", "技術理解", "耐久力", "敏捷性", "幸運"]
CONFIG = {
    "STAT_TOTAL_MIN": 18,
    "STAT_TOTAL_MAX": 22,
    "WEAK_STAT_THRESHOLD": "C"
}

def validate_ranks(ranks: List[str]) -> None:
    """ランクデータのバリデーション"""
    if not ranks:
        raise ValueError("ランクリストが空です")
    if len(ranks) < 2:
        raise ValueError("ランクは2つ以上必要です")
    if len(ranks) != len(set(ranks)):
        raise ValueError("ランクに重複があります")

def load_ranks() -> List[str]:
    """ランクデータをJSONファイルから読み込む"""
    try:
        with open("data/ranks.json", "r", encoding="utf-8") as f:
            ranks = json.load(f)
        validate_ranks(ranks)
        logger.info(f"Loaded ranks: {ranks}")
        return ranks
    except FileNotFoundError:
        logger.error("ranks.json が見つかりません")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"ranks.json の形式エラー: {e}")
        raise
    except Exception as e:
        logger.error(f"ランクデータ読み込みエラー: {e}")
        raise

def validate_classes(classes: Dict[str, Dict[str, any]]) -> None:
    """職業データのバリデーション"""
    for job, data in classes.items():
        # bonuses内のステータスを検証
        bonuses = data.get("bonuses", {})
        for stat in bonuses:
            if stat not in STATS:
                raise ValueError(f"職業 '{job}' のステータス '{stat}' は無効です")
        # ボーナス値の検証（警告のみ）
        for stat, bonus in bonuses.items():
            if bonus not in [2, -2]:
                logger.warning(f"職業 '{job}' のステータス '{stat}' のボーナス '{bonus}' は+2または-2を推奨")
        # iconの存在を確認（任意）
        if "icon" in data:
            logger.debug(f"職業 '{job}' のアイコン: {data['icon']}")

def load_classes() -> Dict[str, Dict[str, any]]:
    """職業データをJSONファイルから読み込む"""
    try:
        with open("data/classes.json", "r", encoding="utf-8") as f:
            classes = json.load(f)
        validate_classes(classes)
        logger.info(f"Loaded classes: {list(classes.keys())}")
        return classes
    except FileNotFoundError:
        logger.error("classes.json が見つかりません")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"classes.json の形式エラー: {e}")
        raise
    except Exception as e:
        logger.error(f"職業データ読み込みエラー: {e}")
        raise

RANKS = load_ranks()
CLASSES = load_classes()

class Character:
    """キャラクターのステータスと職業を管理するクラス"""
    def __init__(self, name: str, job: str = "村人", created_at: Optional[str] = None):
        """キャラクターを初期化する"""
        self.name = name
        self.job = job
        self.stats: Dict[str, str] = {stat: "C" for stat in STATS}
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.apply_job_bonus()

    def apply_job_bonus(self) -> None:
        """職業ボーナスをステータスに適用する（2段階変化）"""
        for stat, bonus in CLASSES.get(self.job, {}).get("bonuses", {}).items():
            current_idx = RANKS.index(self.stats[stat])
            new_idx = max(0, min(len(RANKS) - 1, current_idx + bonus))
            self.stats[stat] = RANKS[new_idx]

    def auto_generate(self) -> None:
        """ステータスを自動生成する（2段階変化）"""
        total_points = random.randint(CONFIG["STAT_TOTAL_MIN"], CONFIG["STAT_TOTAL_MAX"])
        stats = {stat: RANKS.index("C") for stat in STATS}
        base_sum = sum(stats.values())
        target_sum = total_points

        while sum(stats.values()) < target_sum:
            stat = random.choice(STATS)
            if stats[stat] <= RANKS.index("SS") - 2:
                stats[stat] += 2
        while sum(stats.values()) > target_sum:
            stat = random.choice(STATS)
            if stats[stat] >= RANKS.index("F") + 2:
                stats[stat] -= 2

        self.stats = {stat: RANKS[val] for stat, val in stats.items()}

        if all(RANKS.index(v) >= RANKS.index(CONFIG["WEAK_STAT_THRESHOLD"]) for v in self.stats.values()):
            weak_stat = random.choice(STATS)
            weak_idx = max(0, RANKS.index(self.stats[weak_stat]) - 2)
            self.stats[weak_stat] = RANKS[weak_idx]

        self.apply_job_bonus()

    def change_job(self, new_job: str) -> None:
        """職業を変更し、ボーナスを再適用する"""
        self.job = new_job
        self.stats = {stat: "C" for stat in STATS}
        self.apply_job_bonus()