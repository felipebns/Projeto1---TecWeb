import sqlite3

from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

class Database:
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self.conn = sqlite3.connect(f"Docs/data/{self.nome}.db")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS note ( id INTEGER PRIMARY KEY,
                                            title STRING,
                                            content TEXT NOT NULL );
        """)

    def add(self, note: Note) -> None:
        self.conn.execute(f"""
            INSERT INTO note (title, content) VALUES ('{note.title}', '{note.content}');
        """)
        self.conn.commit()

    def get_all(self) -> list:
        cursor = self.conn.execute("SELECT id, title, content FROM note")
        notes = []
        for linha in cursor:
            id_ = linha[0]
            title = linha[1]
            content = linha[2]
            note = Note(id=id_, title=title, content=content)
            notes.append(note)
        return notes
    
    def update(self, entry: Note) -> None:
        self.conn.execute(f"""
            UPDATE note SET title = '{entry.title}' ,content = '{entry.content}' WHERE id = {entry.id}
        """)
        self.conn.commit()

    def delete(self, note_id: int) -> None:
        self.conn.execute(f"""
            DELETE FROM note WHERE id = {note_id}
        """)
        self.conn.commit()

    def get_by_id(self, id) -> Note:
        elementos = self.get_all()
        for elemento in elementos:
            if elemento.id == int(id):
                return elemento

