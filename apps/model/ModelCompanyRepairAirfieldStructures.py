from model.Relation import Relation
from model.RepairAirfieldStructures import RepairAirfieldStructures, TypesOfRepairs

class ModelCompanyRepairAirfieldStructures:
    def __init__(self, mediator):
        self.__mediator =  mediator

        self.__relation = Relation("RepairAirfieldStructures", str(type(RepairAirfieldStructures())), RepairAirfieldStructures.ATTRIBUTE_TYPES)

        self.__objs =  []

    def request(self, command):
        if command == 'get_types_of_repairs_name_from_int':
            return TypesOfRepairs.get_types_of_repairs_name_from_int()
        elif command == 'get_types_of_repairs_int_from_name':
            return TypesOfRepairs.get_types_of_repairs_int_from_name()

    def changed(self, command='', args = []):
        self.__mediator.object_changed(self, command=command,args=args)

    def create_object(self, args):
        [airfield_name, structures_name, cipher, types_of_repairs, price, contractor_name, repair_period, structures_photo] = args

        types_of_repairs_name = self.request('get_types_of_repairs_int_from_name')

        types_of_repairs = types_of_repairs_name[types_of_repairs]

        new_obj = RepairAirfieldStructures(airfield_name, structures_name,cipher, types_of_repairs, price, contractor_name, repair_period, structures_photo)

        self.__objs.append(new_obj)

        self.changed(command='create_object', args=args)

    def get_objects(self):
        objs_as_list = []

        objs_as_list.append(RepairAirfieldStructures.ATTRIBUTE_NAME_FOR_PEPLE)

        for obj in self.__objs:
            objs_as_list.append(obj.to_list_str())

        return objs_as_list

    def get_fields_object(self):
        return RepairAirfieldStructures.ATTRIBUTE_NAME_FOR_PEPLE

    def get_fields_object_reverse(self):
        return RepairAirfieldStructures.ATTRIBUTE_NAME_FOR_PROGRAM

    def get_fields_types_object_reverse(self):
        return RepairAirfieldStructures.ATTRIBUTE_TYPES

    # def add_objects_in_database(self):
    #     for obj in self.__objs:
    #         self.__relation.INSERT(obj)
    #
    #     self.__objs = []

    def add_object_in_database(self, args):
        [airfield_name, structures_name, cipher, types_of_repairs, price, contractor_name, repair_period,
         structures_photo] = args

        types_of_repairs_name = self.request('get_types_of_repairs_int_from_name')

        types_of_repairs = types_of_repairs_name[types_of_repairs]

        new_obj = RepairAirfieldStructures(airfield_name, structures_name, cipher, types_of_repairs, price, contractor_name, repair_period, structures_photo)

        new_obj_index = -1
        for index, obj in enumerate(self.__objs):
            if obj == new_obj:
                new_obj_index = index

        if new_obj_index == -1:
            return

        self.__relation.INSERT(new_obj)

        self.__objs.pop(new_obj_index)

        self.changed(command='objects_added')


    def get_all_objects_from_database(self):
        result = self.__relation.SELECT()

        result[0] = RepairAirfieldStructures.ATTRIBUTE_NAME_FOR_PEPLE

        return result

    def get_find_objects_in_database(self, attribute, value):
        if not (attribute in list(RepairAirfieldStructures.ATTRIBUTE_TYPES.keys())):
            raise Exception(f'У объекта нет атрибута с названием {attribute}.')

        if str(type(value)) != str(type(RepairAirfieldStructures.ATTRIBUTE_TYPES[attribute])):
            raise ValueError(f"'{value}' имеет тип данных отличный от {type(RepairAirfieldStructures.ATTRIBUTE_TYPES[attribute])}.")

        return self.__relation.SELECT(WHERE=f'{attribute} == {value}')

    def sort_database(self, attribute):
        self.__relation.ORDER_FAST(attribute)

        self.changed(command='sorted_database')

    def contains(self, args):
        [airfield_name, structures_name, cipher, types_of_repairs, price, contractor_name, repair_period, structures_photo] = args

        types_of_repairs_name = self.request('get_types_of_repairs_int_from_name')

        types_of_repairs = types_of_repairs_name[types_of_repairs]

        obj = RepairAirfieldStructures(airfield_name, structures_name,cipher, types_of_repairs, price, contractor_name, repair_period, structures_photo)

        return self.__relation.contains(obj)

    def delete_object_from_database(self, args):
        [airfield_name, structures_name, cipher, types_of_repairs, price, contractor_name, repair_period, structures_photo] = args

        types_of_repairs_name = self.request('get_types_of_repairs_int_from_name')

        types_of_repairs = types_of_repairs_name[types_of_repairs]

        obj = RepairAirfieldStructures(airfield_name, structures_name, cipher, types_of_repairs, price, contractor_name, repair_period, structures_photo)

        self.__relation.DELETE(obj)

        self.changed('database_changed')