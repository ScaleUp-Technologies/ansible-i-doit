from .consts import C__CATG__ACCESS
from .category import IDoitCategory


class IDoitAccess(IDoitCategory):

    def __init__(self, cfg):
        super().__init__(cfg, C__CATG__ACCESS)

    def convert_field_with_name_primary(self, data):
        return int(data['primary']['value'])
