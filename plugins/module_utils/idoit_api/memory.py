from .consts import C__CATG__MEMORY
from .category import IDoitCategory


class IDoitMemory(IDoitCategory):

    def __init__(self, cfg):
        super().__init__(cfg, C__CATG__MEMORY)

    def convert_field_with_name_capacity(self, data):
        return float(data['capacity']['title'])
