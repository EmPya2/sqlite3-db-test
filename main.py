from kivymd.app import MDApp
import sqlite3
import sys
from kivy.lang import Builder
from kivymd.utils.set_bars_colors import set_bars_colors
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.uix.card import MDCard
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
import datetime
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import MDLabel
from plyer import notification

from kivymd.uix.taptargetview import MDTapTargetView

from sqlite3 import Error

from kivymd.uix.tab import MDTabsBase


kv = """

# card to contain note data

<Note>:
	size_hint: 1, None
	style:"outlined"
	ripple_behavior: True
	line_color: app.theme_cls.primary_color
	padding:"10dp"
	line_width: 3
	radius: 20
	title:""
	date:""
	name:"" 
	note:""
	
	on_release:
		
		app.take_info(self.title, self.date, self.note)
		
	MDBoxLayout:
		orientation:"vertical"
		#size_hint: .5, 1
		
		MDLabel:
			text: root.title[0:35] 
			font_style:"Button"
			markup: True
			font_size:"18dp"
			bold: True
			color:app.theme_cls.primary_color
					
		#MDLabel:
			#text:"Status"
			#font_style:"Caption"
			
		MDLabel:
			text: root.date
			markup: True
	
	MDBoxLayout:
		adaptive_width: True

		orientation:"vertical"
		#size_hint_x:.1
		size_hint_y: None
		pos_hint: {"center_y":.5, "center_x":.8}
		

		MDIconButton:
			icon:"delete-outline"
			pos_hint: {"center_y":.5}
			on_press:
				app.remove_data_from_db(root.name)
				
			on_release:
				app.refill_note()

#card to contain task data		
			
<Task>:
	size_hint: 1, None
	#md_bg_color:"e7e7e7"
	#size: 0, "100dp"
	style:"outlined"
	line_color: app.theme_cls.primary_color
	line_width:3 
	radius: 20
	id:""
	title:""
	details:""
	status:""
	date:""
	
	
	MDIconButton:
		icon:"circle-outline"
		pos_hint: {"center_y":.5}
		theme_icon_color:"Custom"
		icon_color:app.theme_cls.primary_color
		
		on_release:
			self.icon = "check-circle-outline"   if self.icon == "circle-outline" else "circle-outline"
			
			root.status = "Done" if root.status == "Not Accomplished" else "Not Accomplished"
		
	MDBoxLayout:
		orientation:"vertical"
		size_hint: .5, 1
		
		MDLabel:
			text: str(root.title) 
			font_style:"Button"
			markup: True
			font_size:"18dp"
			bold: True
			color:app.theme_cls.primary_color
			
		MDLabel:
			text: str(root.status)
			font_style:"Caption"
			bold: True
			
		MDLabel:
			text: str(root.date)
			markup: True 
			bold: True
	
	MDBoxLayout:

		orientation:"vertical"
		size_hint_x:.1
		size_hint_y: None
		pos_hint: {"center_y":.5}
		

		MDIconButton:
			icon:"delete-outline"
			pos_hint: {"center_y":.5}
			on_press:
				app.remove_data_from_db_(root.id)
				
			on_release:
				app.refill_task()
				
<Alert>:
	font_style:"H6"
	halign:"center"
	pos_hint:{"center_x":.5, "center_y":.5}
	bold: True 
	theme_text_color:"Custom"
		
ScreenManager:
	id:sm	

	Screen:
		name:"a"
		
		MDBoxLayout:
			orientation:"vertical"
			
			MDBoxLayout:
				orientation:"vertical"
				adaptive_height: True
	
				# title bar
			
				MDTopAppBar:
					title:"Notebook and Tasks"
					
					right_action_items: [["cog", lambda x: app.open_settings()], ["theme-light-dark", lambda x : app.exit()]]
					
			# tabs
		
			MDTabs:
				id: tab_control
				tab_hint_x: True
				tab_indicator_color:"white"
				underline_color:"white"
				indicator_color:"red"
				
				Tab:
					title:"[b]Notes[b]"
					icon:"notebook"
	
					
					orientation:"vertical"
					
					RecycleView:
						id: notes_viewer
						key_viewclass: "viewclass"
						key_size: "height"
			
											
						RecycleBoxLayout:
							orientation:"vertical"
							size_hint_y: None 
							height: self.minimum_height 
							default_size_hint: 1, None
							padding: "10dp"
							default_size: None, dp(80)
							spacing:"10dp"
														
					
				Tab:
					#title:"[b]Add Notes[b]"
					icon:"notebook-plus"
					
					
					orientation:"vertical"
					
					padding:"10dp"
					spacing: "50dp"
					
					MDGridLayout:
						cols: 1
						#size_hint_y: None
						spacing:"20dp"
						
						MDGridLayout:
							#orientation:"vertical"
							cols:1
							adaptive_height: True
						
					
							MDTextField:
								id: note_title
								mode: "fill"
								adaptive_height: True
								hint_text: "Title"
						
								
						MDGridLayout:
						#	orientation:"vertical"
							cols:1
			
						
							MDTextField:
								id: notes
								mode:"fill"
								multiline: True
								hint_text: "Write Note Here"
								size_hint: 1, .5
			
								
						MDBoxLayout:
							orientation:"vertical"
							#adaptive_height: True
							
	
						
							MDFloatingActionButton:
								icon: "plus"
								id:sv
								pos_hint: {"center_x":.5}
								#icon_color: app.theme_cls.primary_color 
								theme_text_color: "Custom"
								on_release:
									app.save_note()
									app.refill_note()
				
						
				Tab:
					title:"[b]Tasks[/b]"
					icon: "clipboard-list"
					
					RecycleView:
						key_viewclass: "viewclass"
						key_size:"height"
						id: task_viewer
						
						RecycleBoxLayout:
							spacing:"20dp"
							
							padding: "10dp"
							orientation:"vertical"
							height: self.minimum_height
							size_hint: 1, None 
							default_size_hint: 1, None 
							default_size: 0, dp(120)
							
				
					
				Tab:
					#title: "Add Tasks"
					icon:"clipboard-plus"
					
					orientation:"vertical"
					
					MDGridLayout:
						size_hint_y: .5
						cols: 1
						padding:"10dp"
						
						spacing:"10dp"
						
						MDTextField:
							mode:"fill"
							
							hint_text:"Title"
							id: task_title
							
						MDTextField:
							adaptive_height: True
							mode: "fill"
							hint_text:"Task details"
							size_hint: 1, .1
							id: task_details
							
					MDGridLayout:
						cols:1
						#md_bg_color:"blue"
						padding:"10dp"
						spacing:"30dp"
						size_hint_y:.4
						
						MDBoxLayout
							adaptive_height: True 
		
						
							MDRoundFlatIconButton:
								text:"Choose Date To Do Task"
								icon:"calendar"	
								halign:"center"
								pos_hint:{"center_x":.5}
								on_press:
									app.show_date()
							
							MDLabel:
								adaptive_height: True
								text:""
								bold: True
								id: picked_date
								adaptive_height: True
								halign:"center"
					
						MDBoxLayout:
					
							adaptive_height: True
						
							MDRoundFlatIconButton:
								text:"Choose Time To Do Task"
								icon:"clock"	
								halign:"center"
								pos_hint:{"center_x":.5}
								on_press:
									app.show_time()
							
							MDLabel:
								adaptive_height: True
								text:""
								bold: True
								id: picked_time
								adaptive_height: True
								halign:"center"		
					
							
					MDBoxLayout:
						orientation:"vertical"
						size_hint_y: .1
						
						MDFloatingActionButton:
							icon:"plus"
							pos_hint: {"center_x":.5, "center_y":.9}
							elevation:0
							on_press:
								app.save_task(task_title, task_details, picked_date, picked_time)
								
							on_release:
								app.refill_task()
						
					
					
	Screen:
		name:"b"
		
		MDBoxLayout:
			orientation:"vertical"
			
			padding:"10dp"
			
			MDCard:
				orientation:"vertical"
				elevation: 3
				radius: "25dp"
				
				MDBoxLayout:
					padding:"10dp"
					spacing:"30dp"
					orientation:"vertical"
					adaptive_height: True

			
					MDLabel:
						text:"Title"
						id:sec_title
						halign:"center"
						adaptive_height: True
						font_style: "H5"
						
						
					MDLabel:
						text:"Date"
						id: sec_date
						adaptive_height: True
						halign:"center"
						
				MDSeparator:
				
		
					
				ScrollView:
					
					
					MDBoxLayout:
						orientation:"vertical"
						size_hint_y: None
						height:self.minimum_height 
						default_size_hint: 1, 1
						padding:"20dp"
						
						MDLabel:
							adaptive_height: True
							text:"Note"
							id: sec_note
							halign:"center"
							
				MDBoxLayout:
					orientation:"vertical"
					adaptive_height: True
					padding:"10dp"
					
					MDRoundFlatIconButton:
						text:"Back"
						icon:"arrow-left"
						pos_hint: {"center_x":.5, "center_y":.9}
						halign:"center"
						on_release: sm.current = "a"
						
					
	Screen:
		name:"settings"
		
		MDBoxLayout:
			orientation:"vertical"
			
			spacing:"20dp"
			
			MDBoxLayout:
				orientation:"vertical"
				adaptive_height: True
				
				MDTopAppBar:
					title:"Settings"
					right_action_items:[["back", lambda x: app.exit()], ["book", lambda x: app.to_a()]]
					
			MDGridLayout:
				cols: 1
				
				padding:"20dp"
				
				MDCard:
					radius:"20dp"
					size_hint: 1, None 
					height:"100dp"
					elevation: 3
					padding:"10dp"
					
					MDBoxLayout:
						padding:[20, 0, 0, 0]
						size_hint_x: .75
						MDLabel:
							text:"Dark Theme"
							bold: True
							
					MDBoxLayout:
						size_hint_x: .25
						
						MDCheckbox:
							id: dt
							active: True

							on_active:
								app.change_theme()
					
					
				

"""

# Database class to easily control databases

class Database():
	def __init__(self, name):
		self.name = name 
		self.conn = None

		self.connect_()
		
	def connect_(self):
		try:
		
			self.conn = sqlite3.connect(str(self.name))
			self.cursor = self.conn.cursor()
			print("Connection successful")
			
		except Error as e:
			print("connect failed to %s failed, %s" %(self.name, e))
	
	def create_table(self, name, columns): 
		try:
		
			self.command = """CREATE TABLE IF NOT EXISTS
	{} (Id INTEGER PRIMARY KEY AUTOINCREMENT,
		
		{} char(50),
		
		{} char(30),
		
		{} char(100)
		)""".format(name, columns[0], columns[1], columns[2])
		
			print(self.command)
			
			self.cursor.execute(self.command)
			print("create notes Table successful")
			
			self.conn.commit()
			
		except Error as e:
			print("Create notes table failed", e)
				
	def create_table_(self, name, columns): 
	
		try:
	
		
			self.command_= """CREATE TABLE IF NOT EXISTS
	{} (Id INTEGER PRIMARY KEY AUTOINCREMENT,
		
		{} char(50),
		
		{} char(30),
		
		{} char(100),
		
		{} char(100)
		)""".format(name, columns[0], columns[1], columns[2], columns[3])
		
			print(self.command_)
			
			self.cursor.execute(self.command_)
			
			print("create tasks table successful")
			self.conn.commit()
			
		except Error as e:
			print("Add to task failed", e)
			
	
		
	def insert_into_table(self, title, date, note):
		
		try:
			self.conn = sqlite3.connect(str(self.name))
			self.cursor = self.conn.cursor()
			self.cursor = self.conn.cursor()
			
			
			self.cursor.execute("""
			INSERT INTO Notes(Title, Date, Note ) VALUES(?, ?, ?)""", (title, date, note))	
			
			self.conn.commit()
			
			command = """ SELECT * FROM Notes"""
			
			self.cursor.execute(command)
			
			fetch = self.cursor.fetchall()
			
			
			print(fetch)
			print("Added title, date and note")
			
			
			
		except Error as e:
			print("Add to notes failed", e)
			
	def insert_into_table_(self, title, task, status, date):
		
		try:
			self.conn = sqlite3.connect(str(self.name))
			self.cursor = self.conn.cursor()
			
			self.cursor.execute(""" INSERT INTO Tasks(Title,Task, Status, Date) VALUES(?, ?, ?, ?) """, (title, task, status, date))
			self.conn.commit()
			
			self.cursor.execute("""
			SELECT * FROM Tasks
			
			""")
			
			self.conn.commit()
			
			fetch = self.cursor.fetchall()
			
			
			print(fetch)
			print("Added title, status and date")
			
			
			
		except Error as e:
			print("Add to notes failed", e)
			
# Note class inherit from MDCard class

class Note(MDCard):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		
	def delete(self):
		print(dir(self.parent.remove_widget(self)))
		notification. notify(title="Note Deleted successfully", message="your note has been removed")
		

# Task card inherit from mMDCard class	
class Task(MDCard):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		pass

class Tab(MDTabsBase, MDBoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
	def on_tab_switch(self, a, b, c):
		print(a, b, c)
		
class Alert(MDLabel):
	pass

notes_db = Database("notes.db")
task_db = Database("tasks.db")

# Main app class
class App(MDApp):
	
	def build(self):	
		
		
		# settings theme and colore
		self.theme_cls.primary_palette = "Red"
		self.theme_cls.primary_hue = "600"
		self.theme_cls.theme_style = "Light"
		self.theme_cls.material_style = "M2"
		
		# return kv file
		return Builder.load_string(kv)
		
	def on_start(self):	
		
		# add task

		# creating databases
		
		
		#creating tables
		notes_db.create_table("Notes", ["Title", "Date", "Note"])
		task_db.create_table_("Tasks", ["Title", "Task", "Status", "Date"])
		
		set_bars_colors(self.theme_cls.primary_color, "000000",
		#self.theme_cls.primary_color,
		 "Light")
		 
		 # creating note items 
		 
		self.refill_note()
		self.refill_task()
		
	def change_theme(self):
		if self.theme_cls.theme_style == "Light":
			self.theme_cls.theme_style = "Dark"
			
		else:
			self.theme_cls.theme_style = "Light"
			
	
			
	def exit(self):
		sys.exit()
		
	def save_note(self):
		IDS = self.root.ids
		
		try:
			
			if not(IDS.note_title.text == "" or IDS.note_title.text == None) :
		
				
				
				current_date = datetime.datetime.now()
				
				current_date = current_date.strftime("%d %b, %Y      %H:%M")
				
				print(str(IDS.note_title.text))
				
				notes_db.insert_into_table(str(IDS.note_title.text), str(current_date) , str(IDS.notes.text))
				
				notification. notify(title="Note added successfully", message="your note has been saved")
				
			else: 
				stat = Snackbar(text="A title is required")
				stat.open()
			
		except Error as e:
			print(e)
			raise e

		finally:
			IDS.note_title.text, IDS.notes.text = "", ""
			print(dir(self.root.ids.tab_control))
			
			tab_1 = list(self.root.ids.tab_control.get_tab_list())[0]
			
			self.root.ids.tab_control.switch_tab(tab_1)
			
			
		
	def refill_note(self):
		
		
		# creating note items 
		 
		notes_db.cursor.execute("""
		 SELECT * FROM Notes
		 
		 """)
		 
		notes_db.conn.commit()
		 
		all_notes = notes_db.cursor.fetchall()
		 
		print("all_notes ::", all_notes)
		
		self.root.ids.notes_viewer.data = []
		
		#self.root.ids.notes_viewer.clear_widgets()
		
		for a_note in all_notes:
		 
			self.root.ids.notes_viewer.data.append(
		{"viewclass": "Note", 
		"title": a_note[1],
		"date":a_note[2], 
		"name": str(a_note[0]), 
		"note": str(a_note[3])	}
		)
		
		if self.root.ids.notes_viewer.data== []:
			self.root.ids.notes_viewer.data.append(
			{
			"viewclass": "Alert",
			"text": "No Notes"}
			)
			
		else:
			pass
			
	def remove_data_from_db(self, data_id):
		
		try:
			
			SQL = """
			
			DELETE FROM Notes WHERE Id = {}
			
			""".format(str(data_id))
			
		
			notes_db.cursor.execute(SQL)
			
			notes_db.conn.commit()
			notification. notify(title=" Note Deleted successfully", message="your note has been deleted")
			
		except Error as e:
			
			print("op failed", e)
			
	def take_info(self, a, b, c):
		self.root.current = "b"
		self.root.ids.sec_title.text = str(a.upper())
		self.root.ids.sec_date.text = str(b)
		self.root.ids.sec_note.text = str(c)

	def save_date(self, instance, value, date_range):
	    print("okkk") 
	    date_sel= value 
	    new_sel = date_sel.strftime("%d %b, %Y") 
	    self.root.ids.picked_date.text = "%s "%(new_sel)
	    
	def save_time(self, instance, value):
	    print(instance, value)
	    
	    self.root.ids.picked_time.text = str(value.strftime("%H:%M"))
	    
	    
	def show_date(self):
		self.dp = MDDatePicker(title="select date to do task", min_date=datetime.date.today())
		
		self.dp = MDDatePicker(title="select date to do task", min_date=datetime.date.today())
		
		self.dp.bind(on_save=self.save_date)
		print(dir(self.dp))
		
		self.dp.open()
		
	def show_time(self):
		self.tp = MDTimePicker(title="select time to do task")
		print(dir(self.tp))
		
		self.tp.bind(on_save=self.save_time)
		self.tp.open()
		
	def save_task(self, task_title, task_details, picked_time, picked_date):
		
		try:
			
			if task_title.text == "" or task_title.text == None:
				stats = Snackbar(text="Task or name of task is required")
				stats.open()
				
			else:
		
				date_time_text = str(picked_date.text + "  "+picked_time.text)
				
				title_text = str(task_title.text) 
				
				details_text = str(task_details.text)
				
				task_db.insert_into_table_(title_text, details_text, "Not Accomplished", date_time_text)
				
				print("Added data to Tasks")
				notification. notify(title=" Task added successfully", message="your task has been saved")
			
		except Error as e:
			print("Add to Tasks failed", e)
			notification. notify(title="Operation Failed", message="Task was not saved")
			
		finally:
			
			task_title.text, task_details.text, picked_time.text, picked_date.text = "", "", "", ""
			
			self.root.ids.tab_control.switch_tab(list(self.root.ids.tab_control.get_tab_list())[2])
			
	def refill_task(self):
		
		# creating note items 
		 
		task_db.cursor.execute("""
		 SELECT * FROM Tasks
		 
		 """)
		 
		task_db.conn.commit()
		 
		all_task = task_db.cursor.fetchall()
		 
		print("all_tasks ::", all_task)
		
		self.root.ids.task_viewer.data = []
		
		#self.root.ids.notes_viewer.clear_widgets()
		
		for a_task in all_task:
		 
			self.root.ids.task_viewer.data.append(
		{"viewclass": "Task", 
		"id":str(a_task[0]),
		"title": str(a_task[1]),
		"status":str(a_task[3]), 
		"date": str(a_task[4]), 
		"details": str(a_task[2])	}
		)
		
		if self.root.ids.task_viewer.data == []:
			self.root.ids.task_viewer.data.append(
			{
			"viewclass": "Alert",
			"text": "No Tasks"}
			)
			
		else:
			pass
		
	def remove_data_from_db_(self, id):
		try:
			
			del_cmd = """ 
			DELETE FROM Tasks WHERE Id = {}
			""".format(id)
			
			task_db.cursor.execute(del_cmd)
			task_db.conn.commit()
			
			print("data %s deleted" %id) 
			notification. notify(title="Data Deleted", message="you have successfully deleted a task")
			
		except Error as e:
			print("remove data failed", e)
			
	def open_settings(self):
		self.root.current = "settings"	
		
	def to_a(self):
		self.root.current = "a"
		
		
		
if __name__ == "__main__":
	App().run()