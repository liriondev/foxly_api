import os
from .foxlite import DataBase

db = DataBase("session")
if not os.path.exists(f'databases/session.db'):
    db.create(
        'session',
        (
            db.Column('token'),
            db.Column('key_hash')
        )
    )

class User:
    def __init__(self) -> None:
        self.token: str
    
    def save_session(self, data):
        db.insert("session", "token,key_hash", f'"{data.token}","{data.key_hash}"')
    
    def get_session(self):
        return db.select("session", "*")