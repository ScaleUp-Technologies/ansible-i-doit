from .consts import C__CATG__CONNECTOR
from .category import IDoitCategory
from pprint import pprint


class IDoitConnector(IDoitCategory):
    def __init__(self, cfg):
        super().__init__(cfg, C__CATG__CONNECTOR)

    def convert_field_with_name_assigned_category(self, data):
        return data['assigned_category']['const']

    def convert_field_with_name_assigned_connector(self, data):
        return self.conv_array_field('assigned_connector', data, 'ref_id')

    def convert_field_with_name_cable_connection(self, data):
        return self.conv_array_field('cable_connection', data, 'id')

    def convert_field_with_name_relation_direction(self, data):
        return int(data['relation_direction']['id'])

    def convert_field_with_name_connector_sibling(self, data):
        return int(data['connector_sibling']['id'])

    def save_category_if_changed(self, objId, data):
        raise Exception(
            'Funktioniert nur wenn es nur eine Kategorie gibt, ' +
            'muss mit ID spezifiziert werden')
