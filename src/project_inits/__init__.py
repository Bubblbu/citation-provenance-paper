from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

data_dir = Path("../data")
als_dir = data_dir / "ALS_data"
