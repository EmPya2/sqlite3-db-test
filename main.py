from kivymd.app import MDApp
from kivy.lang import Builder
import sqlite3
from kivymd.toast import toast
from sqlite3 import Error
import random


kv = """

<Btn@MDRaisedButton>
	pos_hint: {"center_x":.5, "center_y":.5}
	
MDGridLayout: 
	cols: 1

	MDGridLayout: 
		cols: 1
		
		AnchorLayout:
		
			Btn: 
				text:"Create Database"
				on_release: 
					app.create_db()
				
		AnchorLayout:
		
			Btn: 
				text:"Create Cursor"
				on_release: 
					app.create_cursor()
					
		AnchorLayout:
		
			Btn: 
				text:"Create db table"
				on_release: 
					app.create_table()
					
		AnchorLayout:
		
			Btn: 
				text:"select all from db"
				on_release: 
					app.sel()
					
		AnchorLayout:
		
			Btn: 
				text:"Add to db"
				on_release: 
					app.add()				
		
		
	
"""

class App(MDApp): 
	def build(self): 
		return Builder.load_string(kv)
		
	def on_start(self): 
		try: 
			from android.permissions import Permission, request_permissions 
			request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
			
		except: 
			toast("couldnt request permission")
			
		try:
			self.conn = sqlite3.connect("mydb.db")
			toast("db created")
			
		except Error as e: 
			toast(f"create db failed: {e}")
		

	def create_db(self): 
		try:  
			self.conn = sqlite3.connect("mydb.db") 
			toast("db created")
			
		except Error as e:  
			toast(f"create db failed: {e}")
			
	def create_cursor(self): 
		try: 
			self.curs = self.conn.cursor()
			toast("cursor created")
			
		except Error as e: 
			toast(f"create cursor failed {e}")
			
	def sel(self): 
		try:
			sql = """
				SELECT * FROM Note
			"""
			
			self.curs.execute(sql)
			self.conn.commit()
			
			p = self.curs.fetchall()
			
			toast(f"""{p}""")
			
		except: 
			toast("add to db failed")
		
	def add(self): 
		z = random.randint(0, 100000000)
		
		try:
			sql = f"""
			INSERT INTO Note VALUES ({z}, "bingo")
		"""
			self.curs.execute(sql)
			toast("data added")
			
		except: 
			toast("add to db failed")		
		
		
	def create_table(self): 
		try:
			sql = """
				CREATE TABLE IF NOT EXISTS
				Note(
				id INTEGER,
				Name CHAR(50)
				)
			"""
			self.curs.execute(sql)
			self.conn.commit()
			toast("Created table")
			
		except Error as e: 
			toast(f"Create table Failed {e}")
		
			
			
if __name__ == "__main__":
	App().run()