from tkinter import *
from tkinter import ttk

class DatabaseObjects:
    def request(self, command, args=[]):
        return self.__mediator.request(command, args=args)

    def changed(self, command = None, args=[]):
        self.__mediator.object_changed(self, command, args)

    def object_changed(self, object, command = None, args = []):
        if object == self.table:
            if command == 'sort':
                self.changed(command, args)

    def update_database(self):
        data = self.request('get_objects_database')

        for k in self.table.get_children(""):
            self.table.delete(k)

        for object in data[1:]:
            self.table.insert('', END, values=object)

    def delete_objects_database(self, event):
        objects = []

        for item in self.table.selection():
            values = self.table.item(item)['values']
            objects.append(values)

        self.request('delete_objects', objects)

        for item in self.table.selection():
            self.table.delete(item)

    def selection_remove(self, event):
        items = self.table.selection()

        for item in items:
            self.table.selection_remove(item)

    def __init__(self, mediator):
        self.__mediator = mediator

    def get_database_objects_frame(self, master):
        frame = ttk.Frame(master=master, padding=[8, 10])

        data = self.request('get_objects_database')

        headers_as_dict = data[0]

        self.table = ttk.Treeview(master=frame, columns=list(headers_as_dict.keys()), show='headings')

        column_width = (frame.winfo_screenwidth() - 30) / len(headers_as_dict)

        for header in list(headers_as_dict.keys()):
            self.table.column(header, width=int(column_width))
            self.table.heading(header, command=lambda arg = str(header): self.object_changed(self.table, command='sort', args=[arg]), text=headers_as_dict[header])

        for object in data[1:]:
            self.table.insert('', END, values=object)

        self.table.bind('<Delete>', self.delete_objects_database)
        self.table.bind('<Escape>', self.selection_remove)

        self.table.pack(anchor=S,fill=BOTH, expand=True)

        return frame