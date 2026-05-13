import os
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Config:
    openrouter_api_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    gumroad_access_token: str = field(default_factory=lambda: os.getenv("GUMROAD_ACCESS_TOKEN", ""))
    pinterest_access_token: str = field(default_factory=lambda: os.getenv("PINTEREST_ACCESS_TOKEN", ""))
    pinterest_board_id: str = field(default_factory=lambda: os.getenv("PINTEREST_BOARD_ID", ""))
    deepseek_model: str = "deepseek/deepseek-v4-flash"
    data_dir: Path = Path(__file__).parent / "templates"
    db_path: Path = Path(__file__).parent / "state.db"

    def validate(self):
        missing = [k for k, v in {
            "OPENROUTER_API_KEY": self.openrouter_api_key,
            "GUMROAD_ACCESS_TOKEN": self.gumroad_access_token,
            "PINTEREST_ACCESS_TOKEN": self.pinterest_access_token,
            "PINTEREST_BOARD_ID": self.pinterest_board_id,
        }.items() if not v]
        if missing:
            raise ValueError(f"Missing env vars: {', '.join(missing)}")

config = Config()
