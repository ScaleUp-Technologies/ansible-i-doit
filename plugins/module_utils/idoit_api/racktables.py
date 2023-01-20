from .consts import C__CATG__CUSTOM_FIELDS_RACKTABLES
from pprint import pprint
from .category import IDoitCategory


class Racktables(IDoitCategory):

    def __init__(self, cfg):
        super().__init__(cfg, C__CATG__CUSTOM_FIELDS_RACKTABLES)
        self.rt_link = ''
        self.rt_id = ''
        self.rt_type = ''
        self.rt_content = ''
        for field in self.fields:
            title = self.fields[field]['title']
            if title == 'Racktables URL':
                self.rt_link = field
            if title == 'Racktables ID':
                self.rt_id = field
            if title == 'Racktables Object Type':
                self.rt_type = field
            if title == 'Racktables Inhalt':
                self.rt_content = field
        if ((self.rt_link == '') or
           (self.rt_id == '') or
           (self.rt_type == '') or
           (self.rt_content == '')):
            raise Exception('Object nicht deifinert')

    def save_category(self, objId, data):
        mydata = {}
        if 'id' in data.keys():
            mydata[self.rt_id] = data['id']
        if 'link' in data.keys():
            mydata[self.rt_link] = data['link']
        if 'type' in data.keys():
            mydata[self.rt_type] = data['type']
        if 'content' in data.keys():
            mydata[self.rt_content] = data['content']
        if 'description' in data.keys():
            mydata['description'] = data['description']
        return super().save_category(objId, mydata)

    def convert_incomming_category(self, data):
        rtn = {}
        if self.rt_id in data.keys():
            rtn['id'] = data[self.rt_id]

        if self.rt_link in data.keys():
            rtn['link'] = data[self.rt_link]

        if self.rt_type in data.keys():
            rtn['type'] = data[self.rt_type]

        if self.rt_content in data.keys():
            rtn['content'] = data[self.rt_content]

        if 'description' in data.keys():
            rtn['description'] = data['description']

        rtn['_data'] = data
        return rtn
