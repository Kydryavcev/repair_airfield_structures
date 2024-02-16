from tkinter import *
from tkinter import ttk
import re

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

    def update_table(self, objects):
        for k in self.table.get_children(""):
            self.table.delete(k)

        for object in objects:
            self.table.insert('', END, values=object)

    def seach_objects(self):
        value_field = self.combobox_fields.get()

        fields = self.request('get_fields_object_reverse')
        fields_types = self.request('get_fields_types_object_reverse')

        field = fields[value_field]

        value = self.entry_value_field.get()

        if value == '':
            objects = self.request('get_objects_database')

            for k in self.table.get_children(""):
                self.table.delete(k)

            for object in objects[1:]:
                self.table.insert('', END, values=object)

            return


        if str(type(fields_types[field])) == "<class 'int'>":
            value = int(value)

        result = self.request('seach_objects', args=[field, value])

        self.update_table(result[1:])

    def selected(self, event):
        self.entry_value_field.delete(0, END)

    def is_valid(self, newval):
        value = self.combobox_fields.get()

        fields = self.request('get_fields_object_reverse')
        fields_types = self.request('get_fields_types_object_reverse')

        field = fields[value]

        if str(type(fields_types[field])) == "<class 'int'>":
            return re.match("\d*$", newval) is not None
        else:
            return re.match(".*$", newval) is not None

    def __init__(self, mediator):
        self.__mediator = mediator

    def get_database_objects_frame(self, master):
        frame = ttk.Frame(master=master, padding=[8, 10])

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=40)

        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=30)

        fields = self.request('get_fields_object')

        self.combobox_fields = ttk.Combobox(master=frame, values=list(fields.values()), state='readonly')
        self.combobox_fields.current(0)
        self.combobox_fields.bind("<<ComboboxSelected>>", self.selected)
        self.combobox_fields.grid(row=0, column=0, padx=[0,10], sticky=W, ipadx=10, ipady=4)

        check_entry = (frame.register(self.is_valid), "%P")

        self.entry_value_field = ttk.Entry(master=frame, validate='key', validatecommand=check_entry)
        self.entry_value_field.bind('<KeyRelease>', lambda event: self.seach_objects())
        self.entry_value_field.grid(row=0, column=1, padx=[10,10], ipadx=10, ipady=4, sticky=W)

        # self.button_seach = ttk.Button(master=frame, text='Найти', command=self.seach_objects, padding=[10,5])
        # self.button_seach.grid(row=0,column=2, padx=[10,10], sticky=W)

        objects = self.request('get_objects_database')

        headers_as_dict = objects[0]

        self.table = ttk.Treeview(master=frame, columns=list(headers_as_dict.keys()), show='headings')

        column_width = (frame.winfo_screenwidth() - 30) / len(headers_as_dict)

        for header in list(headers_as_dict.keys()):
            self.table.column(header, width=int(column_width))
            self.table.heading(header, command=lambda arg = str(header): self.object_changed(self.table, command='sort', args=[arg]), text=headers_as_dict[header])

        for object in objects[1:]:
            self.table.insert('', END, values=object)

        self.table.bind('<Delete>', self.delete_objects_database)
        self.table.bind('<Escape>', self.selection_remove)

        self.table.grid(row=1, column=0, columnspan=4, pady=[10, 0], sticky=NS)

        return frame