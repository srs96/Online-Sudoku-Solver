import sys
import os
import pandas as pd
root_path = os.path.dirname(os.path.abspath(os.path.basename(__file__)))
sys.path.append(root_path)
from app import db
from app.models import Puzzles
full_path = root_path + '/puzzles/puzzles.csv'
puzzles_file = pd.read_csv(full_path)


for index, row in puzzles_file.iterrows():
    current_puzzle = row[0]
    current_diff = row[1]
    current_puzzle = Puzzles(puzzle=current_puzzle, difficulty=current_diff)
    db.session.add(current_puzzle)
db.session.commit()
