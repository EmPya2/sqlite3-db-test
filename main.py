from kivymd.app import MDApp
from kivy.lang import Builder
import sqlite3
from kivymd.toast import toast
from sqlite3 import Error
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
			
			
if __name__ == "__main__":
	App().run()