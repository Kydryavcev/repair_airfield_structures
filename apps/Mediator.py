from GUI_Frame.GUI import GUI
from model.ModelCompanyRepairAirfieldStructures import ModelCompanyRepairAirfieldStructures

class Mediator: # класс, реализующий паттеры поведения  Mediator
    def __init__(self):
        self.__model = ModelCompanyRepairAirfieldStructures(self)

    def request(self, command, args=[]):
        if command == 'get_objects':
            return self.__model.get_objects()
        elif command == 'get_objects_database':
            return self.__model.get_all_objects_from_database()
        elif command == 'get_fields_object':
            return self.__model.get_fields_object()
        elif command == 'get_fields_object_reverse':
            return self.__model.get_fields_object_reverse()
        elif command == 'get_fields_types_object_reverse':
            return self.__model.get_fields_types_object_reverse()
        elif command == 'delete_objects':
            for object in args:
                self.__model.delete_object_from_database(object)
        elif command == 'insert_objects':
            for object in args:
                self.__model.add_object_in_database(object)
        elif command == 'seach_objects':
            return self.__model.get_find_objects_in_database(args[0], args[1])
        elif command == 'contains_object':
            return self.__model.contains(args=args)

        return self.__model.request(command)

    def object_changed(self, object, command = None, args = []):
        if object == self.__root:
            if command == 'create_object':
                self.__model.create_object(args)
            elif command == 'sort':
                self.__model.sort_database(args[0])
        elif object == self.__model:
            if command == 'create_object':
                self.__root.insert_object_in_table(args=args)
            elif command == 'sorted_database':
                self.__root.update_database()
            elif command == 'objects_added':
                self.__root.update_database()
            elif command == 'database_changed':
                objects = self.__model.get_objects()

                self.__root.database_changed(objects[1:])


    def create_window(self):
        self.__root = GUI(self)
        self.__root.create_window()

Mediator().create_window()