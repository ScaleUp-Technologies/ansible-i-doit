from .consts import C__CATG__STORAGE_DEVICE
from .category import IDoitCategory


class IDoitStorageDevice(IDoitCategory):

    def __init__(self, cfg):

        super().__init__(cfg, C__CATG__STORAGE_DEVICE)

    def convert_field_with_name_capacity(self, data):
        return float(data['capacity']['title'])

    def convert_field_with_name_hotspare(self, data):
        return int(data['hotspare']['value'])
