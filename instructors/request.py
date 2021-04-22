import sqlite3
import json
from models import Instructor

def get_all_instructors():
    with sqlite3.connect("./dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            i.id,
            i.first_name
        FROM Instructors i
        """)

        instructors = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            instructor = Instructor(row['id'], row['first_name'])

            instructors.append(instructor.__dict__)

    return json.dumps(instructors)

# Function with a single parameter
def get_single_instructor(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            i.id,
            i.first_name
        FROM Instructors i
        WHERE i.id = ?
        """, ( id, ))
        
        data = db_cursor.fetchone()

        instructor = Instructor(data['id'], data['first_name'])

        return json.dumps(instructor.__dict__)

def create_instructor(new_instructor):
   with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Instructors
            ( first_name, )
        VALUES
            ( ?, );
        """, (new_instructor['first_name',],  ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_instructor['id'] = id


        return json.dumps(new_instructor)

def delete_instructor(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Instructors
        WHERE id = ?
        """, (id, ))

def update_instructor(id, new_instructor):
  with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Instructors
            SET
                first_name = ?
        WHERE id = ?
        """, (new_instructor['first_name'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

  if rows_affected == 0:
        # Forces 404 response by main module
      return False
  else:
        # Forces 204 response by main module
      return True
