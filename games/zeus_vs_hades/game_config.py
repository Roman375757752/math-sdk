"""Zeus vs Hades – Gods of War (6x5 Scatter-Pays Tumbling Game)"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.config import BetMode  # ← Внимание: это BetMode, а не config.BetMode


class GameConfig(Config):
    """Zeus vs Hades configuration for Stake Engine"""

    def __init__(self):
        super().__init__()

        # === ОСНОВНЫЕ ПАРАМЕТРЫ ===
        self.game_id = "zeus_vs_hades"
        self.provider_numer = 0
        self.working_name = "Zeus vs Hades - Gods of War"
        self.wincap = 10000.0
        self.win_type = "scatter"
        self.rtp = 0.9607  # 96.07%
        self.construct_paths()

        # === СЕТКА ===
        self.num_reels = 6
        self.num_rows = [5] * self.num_reels  # 6x5

        # === PAYTABLE (как в Zeus vs Hades) ===
        t1, t2, t3, t4 = (8, 8), (9, 10), (11, 12), (13, 36)
        pay_group = {
            # H1 = Zeus
            (t1, "H1"): 10.0,
            (t2, "H1"): 25.0,
            (t3, "H1"): 50.0,
            (t4, "H1"): 100.0,

            # H2 = Hades
            (t1, "H2"): 5.0,
            (t2, "H2"): 10.0,
            (t3, "H2"): 25.0,
            (t4, "H2"): 50.0,

            # H3 = Pegasus
            (t1, "H3"): 2.5,
            (t2, "H3"): 5.0,
            (t3, "H3"): 10.0,
            (t4, "H3"): 25.0,

            # H4 = Shield
            (t1, "H4"): 2.0,
            (t2, "H4"): 4.0,
            (t3, "H4"): 7.5,
            (t4, "H4"): 15.0,

            # L1 = Temple
            (t1, "L1"): 1.0,
            (t2, "L1"): 2.0,
            (t3, "L1"): 3.0,
            (t4, "L1"): 10.0,

            # L2 = Helmet
            (t1, "L2"): 0.8,
            (t2, "L2"): 1.5,
            (t3, "L2"): 2.5,
            (t4, "L2"): 8.0,

            # L3 = Ring
            (t1, "L3"): 0.5,
            (t2, "L3"): 1.0,
            (t3, "L3"): 2.0,
            (t4, "L3"): 5.0,

            # L4 = Cup
            (t1, "L4"): 0.4,
            (t2, "L4"): 0.8,
            (t3, "L4"): 1.5,
            (t4, "L4"): 4.0,
        }
        self.paytable = self.convert_range_table(pay_group)

        # === СПЕЦИАЛЬНЫЕ СИМВОЛЫ ===
        self.include_padding = True
        self.special_symbols = {
            "wild": ["W"],        # Wild
            "scatter": ["S"],     # Scatter (Coin)
            "multiplier": ["M"]   # Multiplier (2x–500x)
        }

        # === ТРИГГЕРЫ ФРИСПИНОВ (2 FS за каждый скаттер) ===
        self.freespin_triggers = {
            self.basegame_type: {
                3: 6,   # 3 скаттера = 6 FS
                4: 8,
                5: 10,
                6: 12,
                7: 14,
                8: 16,
                9: 18,
                10: 20,
            },
            self.freegame_type: {
                1: 2,   # 1 скаттер = +2 FS
                2: 4,
                3: 6,
                4: 8,
                5: 10,
                6: 12,
                7: 14,
                8: 16,
                9: 18,
                10: 20,
            },
        }

        self.anticipation_triggers = {
            self.basegame_type: 2,   # Антисипация с 2 скаттеров
            self.freegame_type: 1,   # В бонусе — с 1
        }

        # === РИЛСТРИПЫ ===
        reels = {
            "BR0": "BR0.csv",  # Basegame
            "FR0": "FR0.csv",  # Freegame
            "WCAP": "WCAP.csv" # Wincap (опционально)
        }
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]

        # === BET MODES ===
        self.bet_modes = [
            # === ОСНОВНАЯ ИГРА ===
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    # Wincap
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1, "WCAP": 5},
                            },
                            "scatter_triggers": {6: 1},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    # Freegame Entry
                    Distribution(
                        criteria="freegame",
                        quota=0.1,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {4: 5, 5: 1},
                            "force_freegame": True,
                        },
                    ),
                    # Zero Win
                    Distribution(
                        criteria="0",
                        quota=0.4,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_freegame": False,
                        },
                    ),
                    # Basegame Win
                    Distribution(
                        criteria="basegame",
                        quota=0.5,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_freegame": False,
                        },
                    ),
                ],
            ),

            # === BUY BONUS (100x) ===
            BetMode(
                name="bonus",
                cost=100.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {self.freegame_type: {"FR0": 1, "WCAP": 5}},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.999,
                        conditions={
                            "reel_weights": {self.freegame_type: {"FR0": 1}},
                            "scatter_triggers": {5: 10, 6: 5, 7: 1},
                            "force_freegame": True,
                        },
                    ),
                ],
            ),
        ]
