from tkinter import *
from tkinter import ttk, font
from tkinter.messagebox import showerror, showwarning, showinfo
import re

class WindowCreateObject: # Коллега и посредник в паттерне Mediator,
    def __init__(self, mediator):
        self.__mediator = mediator

    def changed(self):
        args = \
        [
            self.entry_airfield_name.get(),
            self.entry_structures_name.get(),
            self.entry_cipher.get(),
            self.combobox_types_of_repairs.get(),
            self.entry_price.get(),
            self.entry_contractor_name.get(),
            self.entry_repair_period.get(),
            self.entry_structures_photo.get()
        ]
        self.__mediator.object_changed(self, args=args)

    def check_fields(self):
        children = self.__frame.winfo_children()

        flag = True

        for child in children:
            if child.winfo_class() == 'TEntry':
                if len(child.get()) == 0:
                    flag = False

            if child.winfo_class() == 'TCombobox':
                if child.current() == -1:
                    flag = False

        if flag:
            self.button_create['state'] = [ACTIVE]
        else:
            self.button_create['state'] = [DISABLED]

    def object_changed(self, obj):
        if obj.winfo_class() == 'TEntry':
            self.check_fields()
        if obj.winfo_class() == 'TCombobox':
            self.check_fields()
        if obj.winfo_name() == 'button_create':
            self.changed()
            self.dismiss(self.window)
            showinfo(title="Оповещение", message="Объект успешно создан.")

    def ttk_object_changed(self, event, obj):
        self.object_changed(obj)

    def dismiss(self, window):
        window.grab_release()
        window.destroy()

    def is_valid_num(self, newval):
        return re.match("\d*$", newval) is not None

    def request(self, command):
        return self.__mediator.request(command)


    def show_create_obj_window(self):
        self.window = window = Toplevel()
        window.title("Создание объекта")
        window_x = (window.winfo_screenwidth() -550)/2
        window_y = (window.winfo_screenheight()-540)/2
        window.geometry(f'550x380+{int(window_x)}+{int(window_y)}')
        window.minsize(550,520)
        window.protocol("WM_DELETE_WINDOW", lambda: self.dismiss(window))


        self.__frame = frame = ttk.Frame(master=window, padding=[8, 10])

        frame.columnconfigure(index = 0, weight = 1)
        frame.columnconfigure(index = 1, weight = 40)
        frame.columnconfigure(index = 2, weight = 2)

        check_entry_num = (frame.register(self.is_valid_num), "%P")

        font_label_header = "TkTextFont" #font.Font(family="Arial", size=14, weight="normal", slant="roman")
        font_other_label  = "TkTextFont" #font.Font(family="Arial", size=11, weight="normal", slant="roman")

        label_header = ttk.Label(master=frame, text='Заполните поля объекта', font=font_label_header)
        label_header.grid(row=0, column=0, columnspan=3,sticky=N, padx=40, pady=20)

        label_airfield_name = ttk.Label(master=frame, text='Название аэропорта:', font=font_other_label)
        self.entry_airfield_name = ttk.Entry(master=frame, name='entry_airfield_name')
        self.entry_airfield_name.bind('<KeyRelease>', lambda event, obj = self.entry_airfield_name: self.ttk_object_changed(event, obj))
        self.entry_airfield_name.focus()

        label_airfield_name.grid(row=1, column=0, sticky=NSEW, padx=[40,0], pady=10)
        self.entry_airfield_name.grid(row=1, column=1, columnspan=2, sticky=NSEW, padx=[10,40], pady=10, ipadx=10, ipady=4)

        label_structures_name = ttk.Label(master=frame, text='Название объекта:', font=font_other_label)
        self.entry_structures_name = ttk.Entry(master=frame, name='entry_structures_name')
        self.entry_structures_name.bind('<KeyRelease>', lambda event, obj = self.entry_structures_name: self.ttk_object_changed(event, obj))

        label_structures_name.grid(row=2, column=0, sticky=NSEW, padx=[40,0], pady=10)
        self.entry_structures_name.grid(row=2, column=1, columnspan=2, sticky=NSEW, padx=[10,40], pady=10, ipadx=10, ipady=4)

        label_cipher = ttk.Label(master=frame, text='Шифр:', font=font_other_label)
        self.entry_cipher = ttk.Entry(master=frame, validate='key', validatecommand=check_entry_num, name='entry_cipher')
        self.entry_cipher.bind('<KeyRelease>', lambda event, obj = self.entry_cipher: self.ttk_object_changed(event, obj))

        label_cipher.grid(row=3, column=0, sticky=NSEW, padx=[40,0], pady=10)
        self.entry_cipher.grid(row=3, column=1, columnspan=2, sticky=NSEW, padx=[10,40], pady=10, ipadx=10, ipady=4)

        label_types_of_repairs = ttk.Label(master=frame, text='Тип ремонта:', font=font_other_label)
        types_of_repairs_list  = list(self.request('get_types_of_repairs_name_from_int').values())

        self.combobox_types_of_repairs = ttk.Combobox(master=frame, values=types_of_repairs_list, state="readonly", name='combobox_types_of_repairs')
        self.combobox_types_of_repairs.bind('<<ComboboxSelected>>', lambda event, obj = self.combobox_types_of_repairs: self.ttk_object_changed(event, obj))

        label_types_of_repairs.grid(row=4, column=0, sticky=NSEW, padx=[40,0], pady=10)
        self.combobox_types_of_repairs.grid(row=4, column=1, columnspan=2, sticky=NSEW, padx=[10,40], pady=10, ipadx=10, ipady=4)

        label_price = ttk.Label(master=frame, text='Цена:', font=font_other_label)
        self.entry_price = ttk.Entry(master=frame, validate='key', validatecommand=check_entry_num, name='entry_price')
        self.entry_price.bind('<KeyRelease>', lambda event, obj = self.entry_price: self.ttk_object_changed(event, obj))

        label_price.grid(row=5, column=0, sticky=NSEW, padx=[40,0], pady=10)
        self.entry_price.grid(row=5, column=1, columnspan=2, sticky=NSEW, padx=[10,40], pady=10, ipadx=10, ipady=4)

        label_contractor_name = ttk.Label(master=frame, text='Имя подрядчика:', font=font_other_label)
        self.entry_contractor_name = ttk.Entry(master=frame, name='entry_contractor_name')
        self.entry_contractor_name.bind('<KeyRelease>', lambda event, obj = self.entry_contractor_name: self.ttk_object_changed(event, obj))

        label_contractor_name.grid(row=6, column=0, sticky=NSEW, padx=[40,0], pady=10)
        self.entry_contractor_name.grid(row=6, column=1, columnspan=2, sticky=NSEW, padx=[10,40], pady=10, ipadx=10, ipady=4)

        label_repair_period = ttk.Label(master=frame, text='Срок работы:', font=font_other_label)
        self.entry_repair_period = ttk.Entry(master=frame, validate='key', validatecommand=check_entry_num, name='entry_repair_period')
        self.entry_repair_period.bind('<KeyRelease>', lambda event, obj = self.entry_repair_period: self.ttk_object_changed(event, obj))

        label_repair_period.grid(row=7, column=0, sticky=NSEW, padx=[40,0], pady=10)
        self.entry_repair_period.grid(row=7, column=1, columnspan=2, sticky=NSEW, padx=[10,40], pady=10, ipadx=10, ipady=4)

        label_structures_photo = ttk.Label(master=frame, text='Фото объекта:', font=font_other_label)
        self.entry_structures_photo = ttk.Entry(master=frame, name='entry_structures_photo')
        self.entry_structures_photo.bind('<KeyRelease>', lambda event, obj = self.entry_structures_photo: self.ttk_object_changed(event, obj))

        label_structures_photo.grid(row=8, column=0, sticky=NSEW, padx=[40,0], pady=10)
        self.entry_structures_photo.grid(row=8, column=1, columnspan=2, sticky=NSEW, padx=[10,40], pady=10, ipadx=10, ipady=4)

        self.button_create = ttk.Button(master=frame, text="Создать объект", state=[DISABLED], name='button_create')
        self.button_create['command'] = lambda: self.object_changed(self.button_create)
        self.button_create.grid(row=9, column=2, sticky=NSEW, padx=40, pady=5)

        frame.pack(fill=BOTH)

        window.grab_set()       # захватываем пользовательский ввод