#!/usr/bin/python
import os
import yaml
from jinja2 import Environment, FileSystemLoader

def render_cat(base_spec,template):
    idoit_doc_options={}
    for fieldname in base_spec['fields'].keys():
        ansible_name=fieldname
        field=base_spec['fields'][fieldname]
        if 'ansible_name' in field.keys():
            ansible_name=field['ansible_name']

        idoit_doc_options[ansible_name]={
            'description': field['description'],
            'type': 'str'
        }
        if field['type']=='dialog':
            ansible_id_name="%s_id" % ansible_name
            idoit_doc_options[ansible_id_name]={
                'description': field['description_id'],
                'type': 'int'
            }
    idoit_doc= {
        'module': ('idoit_cat_%s' % base_spec['basename']),
        'short_description': ('Create or update a %s category to an object' % base_spec['basename']),
        'description':  ('Adds %s category to an object if not there or update values' % base_spec['category']),
        'options': idoit_doc_options,
        'author': ['Scaleup Technologies', 'Sven Anders (@tabacha)'],
        'extends_documentation_fragment': [
            'scaleuptechnologies.idoit.idoit_option',
            'scaleuptechnologies.idoit.category_options']
    }
    idoit_examples=base_spec['doc_examples']
    idoit_return={
        'changed': {
            'description': 'Are there changes?',
            'type': 'bool',
            'returned': 'always'
        },
        'data': {
            'description': 'New data',
            'type': 'complex',
            'sample': {
                "description": "",
                "firmware": "",
                "manufacturer_id": 5,
                 "model_id": 22,
                 "product_id": "",
                 "serial": "Test 42",
                 "service_tag": "CZJ037040C"
            }
        },
        'return': {
            'description': 'I-Doit API Result',
            'type': 'complex'
        }
    }

    idoit_spec={
        'category': base_spec['category'],
        'single_value_cat': base_spec['single_value_cat'],
        'fields': base_spec['fields'],
    }

    idoit_class='IdoitCategoryModule'

    content=template.render(
        idoit_doc=yaml.dump(idoit_doc),
        idoit_examples=yaml.dump(idoit_examples),
        idoit_return=yaml.dump(idoit_return),
        idoit_spec=yaml.dump(idoit_spec),
        idoit_class=idoit_class)
    out_filename='plugins/modules/idoit_cat_%s.py' % base_spec['basename']
    with open(out_filename,'w') as outfile:
        outfile.write(content)

def render_cat_info(base_spec,template):

def processYaml(filename, template):
    print(filename)

    with open(filename, "r") as stream:
        try:
            base_spec=yaml.safe_load(stream)
            render_cat(base_spec,template)
        except yaml.YAMLError as exc:
            print(exc)

def main():
    directory = "src/idoit/category/"
    environment = Environment(loader=FileSystemLoader("src/idoit/templates/"))
    template = environment.get_template("category.py.j2")
    for file in os.listdir(directory):
        processYaml(os.path.join(directory,file), template)

main()