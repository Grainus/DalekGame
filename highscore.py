import sqlite3 as sql
from typing import Optional

from controller import Keyboard
from game import Game
from models import Difficulty

class HighScore:
   @staticmethod
   def connect() -> sql.Connection:
      return sql.connect('file:highscores.db?mode=rw', uri=True)
   
   @staticmethod
   def create_db() -> sql.Connection:
      con = sql.connect("highscores.bd")
      cur = con.cursor()

      for diff in Difficulty:
         cur.execute(f"""
               CREATE TABLE IF NOT EXISTS HighScores_{diff.name} (
                  UserName TEXT PRIMARY KEY,
                  Score INTEGER,
                  Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )"""
         )

      return con

   @staticmethod
   def push_score(game: Game):
      try:
         con = HighScore.connect()
      except sql.OperationalError:
         con = HighScore.create_db()
      cur = con.cursor()
      
      diff = game.difficulty.name
      name = Keyboard.get_text()
      
      cur.execute(f"""
         INSERT INTO HighScores_{diff} (UserName, Score)
            VALUES (?, ?)
            ON CONFLICT (UserName) DO UPDATE SET
               Score = excluded.Score
               Date = CURRENT_TIMESTAMP
            WHERE excluded.Score > HighScore_EASY.Score   
         """, (name, game.score)
      )
      
   @staticmethod
   def get_scores(
            difficulty: Optional[tuple[Difficulty, ...]] = None
         ) -> Optional[list[tuple]]:
      try:
         con = HighScore.connect()
      except sql.OperationalError:
         return None
     
      cur = con.cursor()
      
      template = (
         "SELECT '{}' AS Difficulty, * FROM HighScores_{}\n"
      )
      
      command = "UNION ALL\n".join(
            template.format(*(diff.name,) * 2)
            for diff in Difficulty
               if difficulty is None
               or diff in difficulty
      ) + "ORDER BY Score DESC"
      
      result = cur.execute(command)
      return result.fetchall()