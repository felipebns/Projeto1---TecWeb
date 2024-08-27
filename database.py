import sqlite3

from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

@dataclass
class Popup:
    id: int = None
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
        self.prepare_popup()

    def prepare_popup(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS popup (id INTEGER DEFAULT 1,
                          content STRING);
        """)        
        self.conn.execute(f"""
            INSERT INTO popup (id, content) VALUES ('1', '');
        """)
        self.conn.commit()

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
            
    def get_popup(self):
        cursor = self.conn.execute("SELECT content, id FROM popup")
        for row in cursor:
            content = row[0]
        return content
    
    def update_popup(self, pop: Popup):
        self.conn.execute(f"""
            UPDATE popup SET content = '{pop.content}' WHERE id = 1
        """)
        self.conn.commit()

