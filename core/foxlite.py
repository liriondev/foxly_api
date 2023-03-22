import sqlite3, os, json

class DataStruct:
    def __init__(self, data: dict):
        self.__dict__ = json.loads(json.dumps(data))

class DataBase:
	def __init__(self, db_name:str) -> None:
		if not os.path.exists('databases/'): os.mkdir('databases/')
		self.db_name:str=f"databases/{db_name}.db"
		
	def create(self, table_name:str, columns):
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(str(x) for x in columns)})')
		conn.commit()
		cursor.close()
	
	def insert(self, table_name:str, column_name:str, column_value:str) -> None:
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'INSERT INTO {table_name} ({column_name}) VALUES ({column_value})')
		conn.commit()
		cursor.close()
	
	def update(self, table_name:str, values:str, where:str='') -> None:
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'UPDATE {table_name} SET {values} {"" if not len(where) else "WHERE "+where}')
		conn.commit()
		cursor.close()

	def delete(self, table_name:str, where:str='') -> None:
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'DELETE FROM {table_name} {"" if not len(where) else "WHERE "+where}')
		conn.commit()
		cursor.close()
	
	def select(self, table_name:str, column:str, where:str='') -> DataStruct:
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(f'SELECT {column} FROM {table_name} {"" if not len(where) else "WHERE "+where}')
		coln=[i[0] for i in cursor.description]
		data=cursor.fetchall()
		res={}
		for i in range(len(data)):
			res[i]=dict.fromkeys(coln)
			for y in range(len(coln)):
				res[i][coln[y]]=data[i][y]
		try: return DataStruct(res[0])
		except: return False
	
	def execute(self, raw: str):
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		cursor.execute(raw)
		conn.commit()
		cursor.close()
		
	def Column(self, column_name:str, column_value_type:str='INTEGER', primary_key:bool=False, default:str=None) -> str:
		return f'{column_name} {column_value_type} {"PRIMARY KEY" if primary_key else ""} {"DEFAULT "+str(default) if default is not None else ""}'
		
	def Where(self, column_name:str, column_value:str) -> str:
		return f'{column_name}="{column_value}"'
