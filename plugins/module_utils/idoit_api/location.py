from .consts import C__CATG__LOCATION
from .category import IDoitCategory
from pprint import pprint
from copy import deepcopy


class IDoitLocation(IDoitCategory):

    def __init__(self, cfg):
        super().__init__(cfg, C__CATG__LOCATION)

    def convert_field_with_name_pos(self, data):
        return int(data['pos']['visually_from'])

    def convert_field_with_name_latitude(self, data):
        if data['latitude'] == '':
            return None
        return float(data['latitude'])

    def convert_field_with_name_longitude(self, data):
        if data['longitude'] == '':
            return None
        return float(data['longitude'])

    def fix_empty_position(self, data):
        for pos_key in ['latitude', 'longitude']:
            if not (pos_key in data):
                data[pos_key] = None
            elif data[pos_key] == '':
                data[pos_key] = None

    def save_category(self, objId, data):
        cdata = deepcopy(data)
        self.fix_empty_position(cdata)
        super().save_category(objId, cdata)

    def update_category(self, objId, data):
        cdata = deepcopy(data)
        self.fix_empty_position(cdata)
        super().update_category(objId, cdata)
