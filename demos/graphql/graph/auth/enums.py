from enum import Enum, unique


@unique
class UserGender(Enum):
    women = 'women'
    male = 'male'
    none = 'none'
