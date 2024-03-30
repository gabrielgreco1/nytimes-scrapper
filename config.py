# config.py
query = "brazil"
subject = "Sports"
months = 3
import os
from pathlib import Path
path = Path(os.getenv('ROBOT_ARTIFACTS', 'output'))