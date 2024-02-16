from tkinter import *
from tkinter import ttk
from GUI_Frame.WindowCreateObject import WindowCreateObject

class CreatedObjects:
    def request(self, command, args=[]):
        return self.__mediator.request(command, args=args)

    def changed(self, command = None, args=[]):
        self.__mediator.object_changed(self, command=command, args=args)

    def object_changed(self, object, command = None, args = []):
        if object == self.window_create_object:
            self.changed(command='create_object', args=args)

    def __init__(self, mediator):
        self.__mediator = mediator

    def insert_object(self, args):
        item = self.table.insert('', END, values=args)

        contains = self.request('contains_object', args)

        if contains:
            self.table.item(item, tag='contains')

    def update_table(self, objects):
        for item in self.table.get_children(''):
            self.table.delete(item)

        for object in objects:
            self.insert_object(object)

    def insert_objects_database(self):
        objects = []

        for item in self.table.selection():
            values = self.table.item(item)['values']
            objects.append(values)

        self.request('insert_objects', objects)

        for item in self.table.selection():
            self.table.delete(item)


    def object_select_table(self, event):
        if len(self.table.selection()) > 0:
            self.button_add_object_database['state'] = [ACTIVE]
        else:
            self.button_add_object_database['state'] = [DISABLED]

    def selection_remove(self, event):
        items = self.table.selection()

        for item in items:
            self.table.selection_remove(item)

    def get_created_objects_frame(self, master):
        frame = ttk.Frame(master=master, padding=[8, 10])

        self.window_create_object = WindowCreateObject(self)

        button_create_obj = ttk.Button(master=frame, text='Создать объект', padding=[10,5], command=self.window_create_object.show_create_obj_window)

        button_create_obj.pack(anchor=NW, pady=[0,10])

        data = self.request('get_objects')

        headers_as_dict = data[0]

        self.table = ttk.Treeview(master=frame, columns=list(headers_as_dict.keys()), show='headings')
        self.table.tag_configure('contains', background='#7BB767')

        column_width = (frame.winfo_screenwidth() - 30) / len(headers_as_dict)

        for header in list(headers_as_dict.keys()):
            self.table.column(header, width=int(column_width))
            self.table.heading(header, text=headers_as_dict[header])


        self.table.bind('<<TreeviewSelect>>',  self.object_select_table)
        self.table.bind('<Escape>', self.selection_remove)
        self.table.pack(fill=BOTH, expand=True)

        self.button_add_object_database = ttk.Button(master=frame, text='Добавить в базу данных', padding=[10,5], state=[DISABLED], command=self.insert_objects_database)
        self.button_add_object_database.pack(anchor=SE, pady=[10,0])

        return frame