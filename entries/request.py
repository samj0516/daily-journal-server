import sqlite3
import json
from models import Entries
from models import Mood
from models import Instructor


def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            e.instructor_id,
            m.label,
            i.first_name
        FROM entries e
        JOIN Mood m
            ON m.id = e.mood_id
        JOIN Instructors i
            ON i.id = e.instructor_id
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            entry = Entries(row['id'], row['date'], row['concept'], row['entry'], row['mood_id'], row['instructor_id'])

            mood = Mood(row['mood_id'], row['label'])

            instructor = Instructor(row['instructor_id'], row['first_name'])
            
            entry.mood = mood.__dict__

            entry.instructor = instructor.__dict__
            
            entries.append(entry.__dict__)

    return json.dumps(entries)

# Function with a single parameter
def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            e.instructor_id,
            m.label,
            i.first_name
        FROM entries e
        JOIN Mood m
            ON m.id = e.mood_id
        JOIN Instructors i
            ON i.id = e.instructor_id
        WHERE e.id = ?
        """, ( id, ))
        
        data = db_cursor.fetchone()

        entry = Entries(data['id'], data['date'], data['concept'], data['entry'], data['mood_id'], data['instructor_id'])
        mood = Mood(data['mood_id'], data['label'])

        instructor = Instructor(data['instructor_id'], data['first_name'])
            
        entry.mood = mood.__dict__

        entry.instructor = instructor.__dict__

        return json.dumps(entry.__dict__)

def get_entry_by_search(search_term):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            e.instructor_id
        FROM entries e
        WHERE e.concept LIKE ?
        """, ( f"%{search_term}%", ))
        
        
        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            entry = Entries(row['id'], row['date'], row['concept'], row['entry'], row['mood_id'], row['instructor_id'])

            entries.append(entry.__dict__)

    return json.dumps(entries)


def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entries
            ( date, concept, entry, mood_id, instructor_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_entry['date'], new_entry['concept'],
              new_entry['entry'], new_entry['mood_id'],
              new_entry['instructor_id'], ))
       
        id = db_cursor.lastrowid
       
        new_entry['id'] = id


    return json.dumps(new_entry)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))


def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            UPDATE Entries
                SET
                    id = ?,
                    date = ?,
                    concept = ?,
                    entry = ?,
                    mood_id = ?,
                    instructor_id = ?
            WHERE id = ?
        """, (new_entry['id'], new_entry['date'], new_entry['concept'],
              new_entry['entry'], new_entry['mood_id'],
              new_entry['instructor_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True