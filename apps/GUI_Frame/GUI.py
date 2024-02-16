from tkinter import *
from tkinter import ttk
from GUI_Frame.CreatedObjects import CreatedObjects
from GUI_Frame.DatabaseObjectsExtended import DatabaseObjects

class GUI:
    def __init__(self, mediator):
        self.__mediator = mediator

    def create_window(self):
        self.root = Tk()

        self.root.title('Ремонт сооружений аэропорта')
        self.root.geometry('500x300')
        self.root.state('zoomed')

        icon = PhotoImage(file="Data\\images\\icon_plane.png")

        self.root.iconphoto(False, icon)

        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH)

        self.created_objects          = CreatedObjects(self)
        self.object_from_database     = DatabaseObjects(self)

        self.created_object_frame = self.created_objects.get_created_objects_frame(self.notebook)
        self.created_object_frame.pack()

        self.object_from_database_frame = self.object_from_database.get_database_objects_frame(self.notebook)
        self.object_from_database_frame.pack(fill=BOTH)

        self.notebook.add(self.created_object_frame, text='Созданные элементы')
        self.notebook.add(self.object_from_database_frame, text='База данных')

        self.root.mainloop()

    def request(self, command, args=[]):
        return self.__mediator.request(command, args=args)

    def changed(self, command, args = []):
        self.__mediator.object_changed(self, command=command, args=args)

    def insert_object_in_table(self, args):
        self.created_objects.insert_object(args=args)

    def update_database(self):
        self.object_from_database.update_database()

    def database_changed(self, objects):
        self.created_objects.update_table(objects)

    def object_changed(self, object, command = None, args = []):
        if object == self.created_objects:
            if command == 'create_object':
                self.changed(command, args=args)
        elif object == self.object_from_database:
            if command == 'sort':
                self.changed(command=command,args=args)