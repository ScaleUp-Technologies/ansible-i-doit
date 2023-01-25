from .consts import C__CATG__CPU
from .category import IDoitCategory


class IDoitCpu(IDoitCategory):

    def __init__(self, cfg):
        super().__init__(cfg, C__CATG__CPU)

    def convert_field_with_name_frequency(self, data):
        return float(data['frequency']['title'])
