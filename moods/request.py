import sqlite3
import json
from models import Mood


def get_all_moods():
    with sqlite3.connect("./dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM mood m
        """)

        moods = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            mood = Mood(row['id'], row['label'])

            moods.append(mood.__dict__)

    return json.dumps(moods)

# Function with a single parameter
def get_single_mood(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM mood m
        WHERE m.id = ?
        """, ( id, ))
        
        data = db_cursor.fetchone()

        mood = Mood(data['id'], data['label'])

        return json.dumps(mood.__dict__)

def create_mood(new_mood):
   with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Mood
            ( label, )
        VALUES
            ( ?, );
        """, (new_mood['label'],  ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_mood['id'] = id


        return json.dumps(new_mood)

def delete_mood(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM moods
        WHERE id = ?
        """, (id, ))

def update_mood(id, new_mood):
  with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Mood
            SET
                label = ?
        WHERE id = ?
        """, (new_mood['label'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

  if rows_affected == 0:
        # Forces 404 response by main module
      return False
  else:
        # Forces 204 response by main module
      return True
