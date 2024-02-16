import json
from typing import *
from enum import IntEnum

class TypesOfRepairs(IntEnum):
    TECHNICAL_INSPECTION = 0 # Технический осмотр
    REDECORATING         = 1 # Косметический ремонт
    RENEWAL              = 2 # Капитальный ремонт
    REDEVELOPMENT        = 3 # Разработка проекта/перепланеровка

    @staticmethod
    def get_types_of_repairs_name_from_int():
        names_dict = \
        {
            0: 'Технический осмотр',
            1: 'Косметический ремонт',
            2: 'Капитальный ремонт',
            3: 'Разработка проекта/перепланеровка'
        }

        correct_names_dict = dict()

        for index, name in names_dict.items():
            if (index in list(TypesOfRepairs._value2member_map_.keys())):
                correct_names_dict[index] = name

        return correct_names_dict

    @staticmethod
    def get_types_of_repairs_int_from_name():
        names_dict = \
        {
            'Технический осмотр': 0,
            'Косметический ремонт': 1,
            'Капитальный ремонт': 2,
            'Разработка проекта/перепланеровка': 3
        }

        correct_names_dict = dict()

        for name, index  in names_dict.items():
            if (index in list(TypesOfRepairs._value2member_map_.keys())):
                correct_names_dict[name] = index

        return correct_names_dict

    def __str__(self):
        types_of_repairs_name = TypesOfRepairs.get_types_of_repairs_name_from_int()
        return types_of_repairs_name[int(self._value_)]

    @staticmethod
    def from_str(str):
        types_of_repairs_name = TypesOfRepairs.get_types_of_repairs_int_from_name()

        num = types_of_repairs_name[str]

        return TypesOfRepairs(num)



class RepairAirfieldStructures:
    ATTRIBUTE_TYPES = {
        'airfield_name' : 'строка',
        'structures_name': 'строка',
        'cipher':   1234,
        'types_of_repairs': 'строка', # Было бы хорошо реализовать указание множества возможных значений в виде списка
        'price': 777,
        'contractor_name': 'строка',
        'repair_period': 1,
        'structures_photo': 'строка'
    }

    ATTRIBUTE_NAME_FOR_PEPLE = {
        'airfield_name' : 'Название аэропорта',
        'structures_name': 'Название объекта',
        'cipher':   'Шифр',
        'types_of_repairs': 'Тип ремонта',
        'price': 'Цена',
        'contractor_name': 'Имя подрядчика',
        'repair_period': 'Срок работы',
        'structures_photo': 'Фото объекта'
    }

    ATTRIBUTE_NAME_FOR_PROGRAM = {
        'Название аэропорта': 'airfield_name',
        'Название объекта': 'structures_name',
        'Шифр': 'cipher',
        'Тип ремонта': 'types_of_repairs',
        'Цена': 'price',
        'Имя подрядчика': 'contractor_name',
        'Срок работы': 'repair_period',
        'Фото объекта': 'structures_photo'
    }

    def __init__(self, airfield_name: str = 'default_airfield_name', structures_name: str = 'default_structures_name', cipher: int = 1234, types_of_repairs: TypesOfRepairs = 1, price: int = 777, contractor_name: str = 'OOO StroyMah', repair_period: int = 1, structures_photo: str = "Data\\images\\devault_phote.png"):
        self.airfield_name    = str(airfield_name).strip()
        self.airfield_name    = str(airfield_name).strip()
        self.structures_name  = str(structures_name).strip()
        self.cipher           = int(cipher)
        self.types_of_repairs = TypesOfRepairs(types_of_repairs)
        self.price            = int(price)
        self.contractor_name  = str(contractor_name).strip()
        self.repair_period    = int(repair_period)
        self.structures_photo = str(structures_photo).strip()

    def __eq__(self, other):
        if str(type(other)) != str(type(self)):
            return False

        result = (
        self.airfield_name    == other.airfield_name    and
        self.airfield_name    == other.airfield_name    and
        self.structures_name  == other.structures_name  and
        self.cipher           == other.cipher           and
        self.types_of_repairs == other.types_of_repairs and
        self.price            == other.price            and
        self.contractor_name  == other.contractor_name  and
        self.repair_period    == other.repair_period    and
        self.structures_photo == other.structures_photo)

        return result

    def clone(self):
        return RepairAirfieldStructures(self.airfield_name, self.structures_name, self.cipher, self.types_of_repairs, self.price, self.сontractor_name, self.repair_period, self.structures_photo)

    @staticmethod
    def from_dict(dict_obj):
        airfield_name    = dict_obj['airfield_name']
        structures_name  = dict_obj['structures_name']
        cipher           = int(dict_obj['cipher'])
        types_of_repairs = TypesOfRepairs(int(dict_obj['types_of_repairs']))
        price            = int(dict_obj['price'])
        contractor_name  = dict_obj['contractor_name']
        repair_period    = int(dict_obj['repair_period'])
        structures_photo = dict_obj['structures_photo']

        return RepairAirfieldStructures(airfield_name, structures_name, cipher, types_of_repairs, price, contractor_name, repair_period, structures_photo)

    @staticmethod
    def from_list(arr: List):
        if len(arr) != 2:
            raise Exception('Создание объекта из списка невозможно.')
        if len(arr[0]) != len(RepairAirfieldStructures.ATTRIBUTE_TYPES):
            raise Exception('Описать объекта из списка невозможно, не все поля определены.')

        headers = arr[0]
        attr    = list(RepairAirfieldStructures.ATTRIBUTE_TYPES.keys())
        attr_position = []

        for i in range(0, len(attr)):
            attr_position.append(headers.index(attr[i]))

        airfield_name    = arr[1][attr_position[0]]
        structures_name  = arr[1][attr_position[1]]
        cipher           = int(arr[1][attr_position[2]])
        types_of_repairs = TypesOfRepairs.from_str(arr[1][attr_position[3]])
        price            = int(arr[1][attr_position[4]])
        contractor_name  = arr[1][attr_position[5]]
        repair_period    = int(arr[1][attr_position[6]])
        structures_photo = arr[1][attr_position[7]]

        return RepairAirfieldStructures(airfield_name, structures_name, cipher, types_of_repairs, price, contractor_name, repair_period, structures_photo)

    @staticmethod
    def from_lists(lists):
        if len(lists[0]) != len(RepairAirfieldStructures.ATTRIBUTE_TYPES):
            raise Exception('Описать объекта из списка невозможно, не все поля определены.')

        objs = []

        headers = lists[0]

        for i in range(1, len(lists)):
            obj = RepairAirfieldStructures.from_list([headers, lists[i]])
            objs.append(obj)

        return objs

    def to_list_str(self):
        return [
            str(self.airfield_name),
            str(self.structures_name),
            str(self.cipher),
            str(self.types_of_repairs),
            str(self.price),
            str(self.contractor_name),
            str(self.repair_period),
            str(self.structures_photo)
        ]

    def to_csv_str(self):
        return (str(self.airfield_name)   + ',' +
                str(self.structures_name)  + ',' +
                str(self.cipher)           + ',' +
                str(self.types_of_repairs) + ',' +
                str(self.price)             + ',' +
                str(self.contractor_name)   + ',' +
                str(self.repair_period)     + ',' +
                str(self.structures_photo))