# config.py
query = "brazil"
subject = "Any"
months = 1
import os
from pathlib import Path
path = Path(os.getenv('ROBOT_ARTIFACTS', 'output'))