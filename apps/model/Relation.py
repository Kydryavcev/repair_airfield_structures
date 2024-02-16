from typing import *
import csv, os.path, re

class Relation:
    def __init__(self, relation_name: str, type_objects: str, attribute_types: Dict):
        self.type_objects       = type_objects
        self.attribute_types    = attribute_types
        self.relation_name      = relation_name
        self.relation_path_name = 'Data\\' + relation_name + '.csv'

        if not os.path.isfile(self.relation_path_name):
            with open(self.relation_path_name, 'w') as file:
                header = list(attribute_types.keys())
                header_csv_str = ''

                for attribute in header:
                    header_csv_str += attribute + ','

                header_csv_str = header_csv_str[0:-1] + '\n'

                file.write(header_csv_str)

    def SELECT(self, attributes = [], WHERE = None):
        objs = []
        with open(self.relation_path_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            headers = next(reader)

            if len(attributes) == 0:
                objs.append(headers)
            else:
                objs.append(attributes)

            for row in reader:
                if WHERE == None:
                    objs.append(row)
                elif re.fullmatch(r'\w+ == .+', WHERE):
                    tokens = WHERE.split(' ')

                    tokens[2] = ' '.join(tokens[2:])

                    tokens = tokens[0:3]

                    if not (tokens[0] in headers):
                        raise Exception('В отношении (таблице) нет атрибута с именем' + tokens[0])

                    index = headers.index(tokens[0])

                    if str(type(self.attribute_types[tokens[0]])) == "<class 'int'>":
                        if int(row[index]) == int(tokens[2]):
                            if len(attributes) == 0:
                                objs.append(row)
                            else:
                                row_mod = []
                                for attribute in attributes:
                                    index = headers.index(attribute)
                                    row_mod.append(row[index])
                                objs.append(row_mod)
                    else:
                        if re.fullmatch(r'".+"', tokens[2]):
                            if row[index] == tokens[2][1:-1]:
                                if len(attributes) == 0:
                                    objs.append(row)
                                else:
                                    row_mod = []
                                    for attribute in attributes:
                                        index = headers.index(attribute)
                                        row_mod.append(row[index])
                                    objs.append(row_mod)
                        else:
                            if row[index].find(tokens[2]) != -1:
                                if len(attributes) == 0:
                                    objs.append(row)
                                else:
                                    row_mod = []
                                    for attribute in attributes:
                                        index = headers.index(attribute)
                                        row_mod.append(row[index])
                                    objs.append(row_mod)
                elif re.fullmatch(r'\w+ > \d+', WHERE):
                    tokens = WHERE.split(' ')

                    if not (tokens[0] in headers):
                        raise Exception('В отношении (таблице) нет атрибута с именем' + tokens[0])

                    index = headers.index(tokens[0])

                    if int(row[index]) > int(tokens[2]):
                        if len(attributes) == 0:
                            objs.append(row)
                        else:
                            row_mod = []
                            for attribute in attributes:
                                index = headers.index(attribute)
                                row_mod.append(row[index])
                            objs.append(row_mod)
                elif re.fullmatch(r'\w+ < \d+', WHERE):
                    tokens = WHERE.split(' ')

                    if not (tokens[0] in headers):
                        raise Exception('В отношении (таблице) нет атрибута с именем' + tokens[0])

                    index = headers.index(tokens[0])

                    if int(row[index]) < int(tokens[2]):
                        if len(attributes) == 0:
                            objs.append(row)
                        else:
                            row_mod = []
                            for attribute in attributes:
                                index = headers.index(attribute)
                                row_mod.append(row[index])
                            objs.append(row_mod)
                elif re.fullmatch(r'\w+ >= \d+', WHERE):
                    tokens = WHERE.split(' ')

                    if not (tokens[0] in headers):
                        raise Exception('В отношении (таблице) нет атрибута с именем' + tokens[0])

                    index = headers.index(tokens[0])

                    if int(row[index]) >= int(tokens[2]):
                        if len(attributes) == 0:
                            objs.append(row)
                        else:
                            row_mod = []
                            for attribute in attributes:
                                index = headers.index(attribute)
                                row_mod.append(row[index])
                            objs.append(row_mod)
                elif re.fullmatch(r'\w+ <= \d+', WHERE):
                    tokens = WHERE.split(' ')

                    if not (tokens[0] in headers):
                        raise Exception('В отношении (таблице) нет атрибута с именем' + tokens[0])

                    index = headers.index(tokens[0])

                    if int(row[index]) <= int(tokens[2]):
                        if len(attributes) == 0:
                            objs.append(row)
                        else:
                            row_mod = []
                            for attribute in attributes:
                                index = headers.index(attribute)
                                row_mod.append(row[index])
                            objs.append(row_mod)
                else:
                    raise Exception('Неопределенное выражение WHERE: ' + WHERE)
        return objs

    def INSERT(self, obj):
        if str(type(obj)) != self.type_objects:
            raise Exception("Передан некоректнный объект типа" + str(type(obj)))

        if self.contains(obj):
            print("Кортедж с такой записью уже существует. Вставка невозможна.")
            return self

        VALUES = obj.to_list_str()

        with open(self.relation_path_name, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(VALUES)

        return self

    def DELETE(self,obj = None, WHERE = None):
        if obj != None:
            if str(type(obj)) != self.type_objects:
                raise Exception("Передан некоректнный объект типа" + str(type(obj)))

            with open(self.relation_path_name, 'r+', encoding='utf-8') as file:
                file.readline()  # Пропускаем заголовки, чтобы никто не напакастил

                flag = False # Удалён ли элемент
                shift = 0 # Сдвиг
                previous_position = file.tell()

                line = file.readline()

                while line != '':
                    current_position = file.tell()

                    if flag:
                        file.seek(previous_position - shift)
                        file.write(line)
                        file.seek(current_position)

                    if line[0:-1] == obj.to_csv_str():
                        shift = current_position - previous_position

                        flag = True


                    line = file.readline()

                    previous_position = current_position

                file.truncate(current_position - shift)
            return

        if re.fullmatch(r'\w+ == .+', WHERE):
            tokens = WHERE.split(' ')

            headers = list(self.attribute_types.keys())

            if not (tokens[0] in headers):
                raise Exception('В отношении (таблице) нет атрибута с именем' + tokens[0])

            index = headers.index(tokens[0])

            with open(self.relation_path_name, 'r+', encoding='utf-8') as file:
                file.readline()  # Пропускаем заголовки, чтобы никто не напакастил

                shift = 0 # Сдвиг
                previous_position = file.tell()

                line = file.readline()

                while line != '':
                    current_position = file.tell()

                    obj_as_list = line[0:-1].split(',')

                    if str(type(self.attribute_types[tokens[0]])) == "<class 'int'>":
                        if int(obj_as_list[index]) == int(tokens[2]):
                            shift += current_position - previous_position
                        else:
                            file.seek(previous_position - shift)
                            file.write(line)
                            file.seek(current_position)
                    else:
                        if obj_as_list[index] == tokens[2]:
                            shift += current_position - previous_position
                        else:
                            file.seek(previous_position - shift)
                            file.write(line)
                            file.seek(current_position)


                    line = file.readline()

                    previous_position = current_position

                file.truncate(current_position - shift)
        elif re.fullmatch(r'\w+ > \d+', WHERE):
            tokens = WHERE.split(' ')

            headers = list(self.attribute_types.keys())

            if not (tokens[0] in headers):
                raise Exception('В отношении (таблице) нет атрибута с именем' + tokens[0])

            index = headers.index(tokens[0])

            with open(self.relation_path_name, 'r+', encoding='utf-8') as file:
                file.readline()  # Пропускаем заголовки, чтобы никто не напакастил

                shift = 0 # Сдвиг
                previous_position = file.tell()

                line = file.readline()

                while line != '':
                    current_position = file.tell()

                    obj_as_list = line[0:-1].split(',')

                    if int(obj_as_list[index]) > int(tokens[2]):
                        shift += current_position - previous_position
                    else:
                        file.seek(previous_position - shift)
                        file.write(line)
                        file.seek(current_position)

                    line = file.readline()

                    previous_position = current_position

                file.truncate(current_position - shift)
        elif re.fullmatch(r'\w+ < \d+', WHERE):
            tokens = WHERE.split(' ')

            headers = list(self.attribute_types.keys())

            if not (tokens[0] in headers):
                raise Exception('В отношении (таблице) нет атрибута с именем' + tokens[0])

            index = headers.index(tokens[0])

            with open(self.relation_path_name, 'r+', encoding='utf-8') as file:
                file.readline()  # Пропускаем заголовки, чтобы никто не напакастил

                shift = 0  # Сдвиг
                previous_position = file.tell()

                line = file.readline()

                while line != '':
                    current_position = file.tell()

                    obj_as_list = line[0:-1].split(',')

                    if int(obj_as_list[index]) < int(tokens[2]):
                        shift += current_position - previous_position
                    else:
                        file.seek(previous_position - shift)
                        file.write(line)
                        file.seek(current_position)

                    line = file.readline()

                    previous_position = current_position

                file.truncate(current_position - shift)
        elif re.fullmatch(r'\w+ >= \d+', WHERE):
            tokens = WHERE.split(' ')

            headers = list(self.attribute_types.keys())

            if not (tokens[0] in headers):
                raise Exception('В отношении (таблице) нет атрибута с именем' + tokens[0])

            index = headers.index(tokens[0])

            with open(self.relation_path_name, 'r+', encoding='utf-8') as file:
                file.readline()  # Пропускаем заголовки, чтобы никто не напакастил

                shift = 0  # Сдвиг
                previous_position = file.tell()

                line = file.readline()

                while line != '':
                    current_position = file.tell()

                    obj_as_list = line[0:-1].split(',')

                    if int(obj_as_list[index]) >= int(tokens[2]):
                        shift += current_position - previous_position
                    else:
                        file.seek(previous_position - shift)
                        file.write(line)
                        file.seek(current_position)

                    line = file.readline()

                    previous_position = current_position

                file.truncate(current_position - shift)
        elif re.fullmatch(r'\w+ <= \d+', WHERE):
            tokens = WHERE.split(' ')

            headers = list(self.attribute_types.keys())

            if not (tokens[0] in headers):
                raise Exception('В отношении (таблице) нет атрибута с именем' + tokens[0])

            index = headers.index(tokens[0])

            with open(self.relation_path_name, 'r+', encoding='utf-8') as file:
                file.readline()  # Пропускаем заголовки, чтобы никто не напакастил

                shift = 0  # Сдвиг
                previous_position = file.tell()

                line = file.readline()

                while line != '':
                    current_position = file.tell()

                    obj_as_list = line[0:-1].split(',')

                    if int(obj_as_list[index]) <= int(tokens[2]):
                        shift += current_position - previous_position
                    else:
                        file.seek(previous_position - shift)
                        file.write(line)
                        file.seek(current_position)

                    line = file.readline()

                    previous_position = current_position

                file.truncate(current_position - shift)
        else:
            raise Exception('Неопределенное выражение WHERE: ' + WHERE)

    def UPDATE(self, SET, WHERE):
        pass

    def ORDER(self, attribute):
        with open(self.relation_path_name, 'r+', encoding='utf-8') as file:
            relation_headers = file.readline() # Пропускаем заголовки

            index_attribute = relation_headers.split(',').index(attribute) # Получаем индекс аттрибута в отношении

            start_position = file.tell()

            back_line_position = start_position
            back_line  = file.readline()

            front_line_position = file.tell()
            front_line = file.readline()

            qentity_unsorted_line_counter = 2 # Несчитая, строку с атрибутами

            while front_line != '':
                flag = False

                obj_as_list_from_back_line = back_line.split(',')
                obj_attribute_from_back_line = obj_as_list_from_back_line[index_attribute]

                obj_as_list_from_front_line = front_line.split(',')
                obj_attribute_from_front_line = obj_as_list_from_front_line[index_attribute]

                if str(type(self.attribute_types[attribute])) == "<class 'int'>":
                    if int(obj_attribute_from_front_line) < int(obj_attribute_from_back_line):
                        file.seek(back_line_position)
                        file.write(front_line)
                        file.write(back_line)

                        flag = True
                else:
                    if obj_attribute_from_front_line < obj_attribute_from_back_line:
                        file.seek(back_line_position)
                        file.write(front_line)
                        file.write(back_line)

                        flag = True

                if flag:
                    end_front_line_position = file.tell() - 8

                    back_line_position = end_front_line_position - (front_line_position-back_line_position) + 8

                    front_line_position = file.tell()
                    front_line = file.readline()
                else:
                    back_line_position = front_line_position
                    back_line = front_line

                    front_line_position = file.tell()
                    front_line = file.readline()

                qentity_unsorted_line_counter += 1

            qentity_unsorted_line_counter -= 1

            while qentity_unsorted_line_counter > 0:
                file.seek(start_position)

                back_line_position = start_position
                back_line = file.readline()

                front_line_position = file.tell()
                front_line = file.readline()

                current_line_counter = 2

                while current_line_counter < qentity_unsorted_line_counter:
                    flag = False

                    obj_as_list_from_back_line = back_line.split(',')
                    obj_attribute_from_back_line = obj_as_list_from_back_line[index_attribute]

                    obj_as_list_from_front_line = front_line.split(',')
                    obj_attribute_from_front_line = obj_as_list_from_front_line[index_attribute]

                    if str(type(self.attribute_types[attribute])) == "<class 'int'>":
                        if int(obj_attribute_from_front_line) < int(obj_attribute_from_back_line):
                            file.seek(back_line_position)
                            file.write(front_line)
                            file.write(back_line)

                            flag = True
                    else:
                        if obj_attribute_from_front_line < obj_attribute_from_back_line:
                            file.seek(back_line_position)
                            file.write(front_line)
                            file.write(back_line)

                            flag = True

                    if flag:
                        end_front_line_position = file.tell() - 8

                        back_line_position = end_front_line_position - (front_line_position - back_line_position) + 8

                        front_line_position = file.tell()
                        front_line = file.readline()
                    else:
                        back_line_position = front_line_position
                        back_line = front_line

                        front_line_position = file.tell()
                        front_line = file.readline()

                    current_line_counter += 1
                qentity_unsorted_line_counter -= 1


    def ORDER_FAST(self, attribute):
        '''Внешняя сортировка.'''
        # Оооох, зря ты сюда полез...
        headers = list(self.attribute_types.keys())

        if not (attribute in headers):
            raise Exception("Аттрибута с именем '" + attribute + "' нет в отношении.")

        with open(self.relation_path_name, 'r', encoding='utf-8') as sortable_file:
            self.__sortable_file_headers = sortable_file.readline() # Сохраняем заголовки, чтобы в будующем не мучаться

        self.__length_series = 1

        quantity_series = -1

        while quantity_series != 1:
            self.__distribution()
            quantity_series = self.__merger(attribute)
            self.__length_series *= 2

        os.remove('Data\\' + 'temp1_' + self.relation_name + '.csv')
        os.remove('Data\\' + 'temp2_' + self.relation_name + '.csv')

        delattr(self, '_Relation__sortable_file_headers')
        delattr(self, '_Relation__length_series')
        delattr(self, '_Relation__file_temp1_weight')
        delattr(self, '_Relation__file_temp2_weight')

    def __distribution(self):
        '''Этап распределения внешней сортировки.'''

        with (open(self.relation_path_name, 'r', encoding='utf-8')                     as sortable_file,
        open('Data\\' + 'temp1_' + self.relation_name + '.csv', 'w', encoding='utf-8') as file_temp1,
        open('Data\\' + 'temp2_' + self.relation_name + '.csv', 'w', encoding='utf-8') as file_temp2):

            sortable_file.readline()  # Пропускаем аттрибуты (заголовки)

            file_num = 0
            series_num  = 0
            line_num = 0
            # ДУБЛИРУЮТСЯ ЭЛЕМЕНТЫ ИЗ-ЗА ТОГО ЧТО НЕСКОЛЬКО РАЗ ЗАИСЫВАЕТСЯ СТРОКА


            for line in sortable_file: # Распределение
                if series_num % 2 == 0:
                    file_temp1.write(line)
                else:
                    file_temp2.write(line)

                line_num += 1

                if line_num == self.__length_series:
                    line_num = 0
                    series_num += 1


            self.__file_temp1_weight = file_temp1.tell() # То же самое что и размер в байтах
            self.__file_temp2_weight = file_temp2.tell()

    def __merger(self, attribute):
        '''Этап слияния внешней сортировки.'''
        # Боже, храни того человека, кто будет разбираться в этом.
        with (open(self.relation_path_name, 'w', encoding='utf-8')                     as sortable_file,
        open('Data\\' + 'temp1_' + self.relation_name + '.csv', 'r', encoding='utf-8') as file_temp1,
        open('Data\\' + 'temp2_' + self.relation_name + '.csv', 'r', encoding='utf-8') as file_temp2):

            sortable_file.write(self.__sortable_file_headers) # Запишем аттрибуты в файл

            relation_headers = self.__sortable_file_headers[0:-1].split(',') # Получаем список аттрибутов

            index_attribute = relation_headers.index(attribute) # Получаем индекс аттрибута в отношении

            file_temp1_end = False
            file_temp2_end = False

            obj_as_str_from_file_temp1 = file_temp1.readline()
            obj_as_list_from_file_temp1 = obj_as_str_from_file_temp1.split(',')
            obj_attribute_from_file_temp1 = obj_as_list_from_file_temp1[index_attribute]

            obj_as_str_from_file_temp2 = file_temp2.readline()
            obj_as_list_from_file_temp2 = obj_as_str_from_file_temp2.split(',')
            obj_attribute_from_file_temp2 = obj_as_list_from_file_temp2[index_attribute]

            quantity_series = 0

            while True:
                number_of_obj_in_series_read_file_temp1 = 0
                number_of_obj_in_series_read_file_temp2 = 0
                file_temp1_series_end = False
                file_temp2_series_end = False
                if (file_temp1_end and file_temp2_end):
                    return quantity_series

                for i in range(0, self.__length_series*2):
                    if (file_temp1_end and file_temp2_end):
                        break

                    if (file_temp1_series_end or file_temp1_end):
                        sortable_file.write(obj_as_str_from_file_temp2)

                        if file_temp2.tell() >= self.__file_temp2_weight:
                            file_temp2_end = True

                            continue

                        obj_as_str_from_file_temp2 =  file_temp2.readline()
                        obj_as_list_from_file_temp2 = obj_as_str_from_file_temp2.split(',')
                        obj_attribute_from_file_temp2 = obj_as_list_from_file_temp2[index_attribute]

                        continue

                    if (file_temp2_series_end or file_temp2_end):
                        sortable_file.write(obj_as_str_from_file_temp1)

                        if file_temp1.tell() >= self.__file_temp1_weight:
                            file_temp1_end = True

                            continue

                        obj_as_str_from_file_temp1 = file_temp1.readline()
                        obj_as_list_from_file_temp1 = obj_as_str_from_file_temp1.split(',')
                        obj_attribute_from_file_temp1 = obj_as_list_from_file_temp1[index_attribute]

                        continue

                    if str(type(self.attribute_types[attribute])) == "<class 'int'>":
                        if int(obj_attribute_from_file_temp1) < int(obj_attribute_from_file_temp2):
                            sortable_file.write(obj_as_str_from_file_temp1)

                            number_of_obj_in_series_read_file_temp1 += 1

                            if number_of_obj_in_series_read_file_temp1 >= self.__length_series:
                                file_temp1_series_end  = True

                            if file_temp1.tell() >= self.__file_temp1_weight:
                                file_temp1_end = True

                                continue

                            obj_as_str_from_file_temp1 = file_temp1.readline()
                            obj_as_list_from_file_temp1 = obj_as_str_from_file_temp1.split(',')
                            obj_attribute_from_file_temp1 = obj_as_list_from_file_temp1[index_attribute]
                        else:
                            sortable_file.write(obj_as_str_from_file_temp2)

                            number_of_obj_in_series_read_file_temp2 += 1

                            if number_of_obj_in_series_read_file_temp2 >= self.__length_series:
                                file_temp2_series_end = True

                            if file_temp2.tell() >= self.__file_temp2_weight:
                                file_temp2_end = True

                                continue

                            obj_as_str_from_file_temp2 = file_temp2.readline()
                            obj_as_list_from_file_temp2 = obj_as_str_from_file_temp2.split(',')
                            obj_attribute_from_file_temp2 = obj_as_list_from_file_temp2[index_attribute]
                    else:
                        if obj_attribute_from_file_temp1 < obj_attribute_from_file_temp2:
                            sortable_file.write(obj_as_str_from_file_temp1)

                            number_of_obj_in_series_read_file_temp1 += 1

                            if number_of_obj_in_series_read_file_temp1 >= self.__length_series:
                                file_temp1_series_end  = True

                            if file_temp1.tell() >= self.__file_temp1_weight:
                                file_temp1_end = True

                                continue

                            obj_as_str_from_file_temp1 = file_temp1.readline()
                            obj_as_list_from_file_temp1 = obj_as_str_from_file_temp1.split(',')
                            obj_attribute_from_file_temp1 = obj_as_list_from_file_temp1[index_attribute]
                        else:
                            sortable_file.write(obj_as_str_from_file_temp2)

                            number_of_obj_in_series_read_file_temp2 += 1

                            if number_of_obj_in_series_read_file_temp2 >= self.__length_series:
                                file_temp2_series_end = True

                            if file_temp2.tell() >= self.__file_temp2_weight:
                                file_temp2_end = True

                                continue

                            obj_as_str_from_file_temp2 = file_temp2.readline()
                            obj_as_list_from_file_temp2 = obj_as_str_from_file_temp2.split(',')
                            obj_attribute_from_file_temp2 = obj_as_list_from_file_temp2[index_attribute]

                quantity_series += 1


    def contains(self, obj):
        if str(type(obj)) != self.type_objects:
            raise Exception("Передан некоректнный объект типа" + str(type(obj)))

        values = obj.to_list_str()

        with open(self.relation_path_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            headers = next(reader)
            for row in reader:
                if values == row:
                    return True
        return False

    def __iter__(self):
        self.__iter_file   = open(self.relation_path_name, 'r', encoding='utf-8')
        self.__iter_reader = csv.reader(self.__iter_file)
        self.__headers     = next(self.__iter_reader) # Пропускаем заголовки
        return self

    def __next__(self):
        try:
            result = next(self.__iter_reader)
        except StopIteration:
            self.__iter_file.close()

            delattr(self, '_Relation__iter_file')
            delattr(self, '_Relation__iter_reader')
            delattr(self, '_Relation__headers')
            raise StopIteration
        return dict(zip(self.__headers, result))
