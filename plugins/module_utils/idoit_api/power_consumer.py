from .consts import C__CATG__POWER_CONUMER
from .category import IDoitCategory


class IDoitPowerConsumer(IDoitCategory):

    def __init__(self, cfg):
        super().__init__(cfg, C__CATG__POWER_CONUMER)

    def convert_field_with_name_active(self, data):
        return int(data['active']['value'])
