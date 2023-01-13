from .consts import C__CATG__NETWORK_PORT
from .category import IDoitCategory

class IDoitNetworkPort(IDoitCategory):

    def __init__(self,cfg):
        super().__init__(cfg, C__CATG__NETWORK_PORT )

    def convert_field_with_name_active(self, data):
        return int(data['active']['value'])

    def convert_field_with_name_interface(self, data):
        if data['interface']==[]:
            return None
        # else:
        raise Exception('unknown conversion ',data)

    def convert_field_with_name_speed(self, data):
        return float(data['speed']['title'])

    def convert_field_with_name_cable(self, data):
        return self.conv_array_field('cable', data, 'id')

    def convert_field_with_name_addresses(self, data):
        if data['addresses']==[]:
            return None
        #else:
        raise Exception('unknown conversion ', data)

    def convert_field_with_name_layer2_assignment(self, data):
        if data['layer2_assignment']==[]:
            return None
        #else:
        raise Exception('unknown conversion ', data)

    def convert_field_with_name_assigned_connector(self, data):
        return self.conv_array_field('assigned_connector',data,'ref_id')

    def convert_field_with_name_relation_direction(self, data):
        return int(data['relation_direction']['id'])

    def save_category_if_changed(self, objId, data):
        raise Exception('Funktioniert nur wenn es nur eine Kategorie gibt, muss mit ID spezifiziert werden')