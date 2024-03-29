#!/usr/bin/python
import os
import yaml
import argparse
from jinja2 import Environment, FileSystemLoader

def render_cat(base_spec, template, outdir):
    idoit_doc_options = {}
    for fieldname in base_spec['fields'].keys():
        ansible_name = fieldname
        field = base_spec['fields'][fieldname]
        if 'ansible_name' in field.keys():
            ansible_name = field['ansible_name']

        idoit_doc_options[ansible_name] = {
            'description': field['description'],
            'type': 'str'
        }
        if field['type'] == 'dialog':
            ansible_id_name = "%s_id" % ansible_name
            idoit_doc_options[ansible_id_name] = {
                'description': field['description_id'],
                'type': 'int'
            }
        elif field['type'] == 'float':
            idoit_doc_options[ansible_name]['type'] = 'float'
        elif field['type'] == 'bool':
            idoit_doc_options[ansible_name]['type'] = 'bool'
        elif field['type'] == 'int':
            idoit_doc_options[ansible_name]['type'] = 'int'
        elif field['type'] == 'list':
            idoit_doc_options[ansible_name]['type'] = 'list'
            idoit_doc_options[ansible_name]['elements'] = field['element_type']
        elif field['type'] in [ 'datetime', 'date_hhmm'] :
            idoit_doc_options[ansible_name]['type'] = 'str'
        elif field['type'] not in ['str', 'html']:
            raise Exception('Unsupported type %s in %s.yml' %
                            (field['type'], base_spec['basename']))

    idoit_doc = {
        'module': ('idoit_cat_%s' % base_spec['basename']),
        'short_description': (
          'Create or update a %s category to an object' %
          base_spec['basename']),
        'description':  (
          'Adds %s category to an object if not there or update values' %
          base_spec['category']),
        'options': idoit_doc_options,
        'author': [
            'Sven Anders (during work by ScaleUp Technologies) (@tabacha)'
        ],
        'extends_documentation_fragment': [
            'scaleuptechnologies.idoit.idoit_option',
            'scaleuptechnologies.idoit.category_options']
    }
    if base_spec['single_value_cat']:
        idoit_doc['extends_documentation_fragment'].append(
            'scaleuptechnologies.idoit.single_category_options')
    else:
        idoit_doc['extends_documentation_fragment'].append(
            'scaleuptechnologies.idoit.multi_category_options')

    idoit_examples = base_spec['doc_examples']
    idoit_return = {
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
        'id': {
            'description': 'Category Id of the saved category',
            'type': 'int'
        },
        'return': {
            'description': 'I-Doit API Result',
            'type': 'complex'
        }
    }

    idoit_spec = {
        'category': base_spec['category'],
        'single_value_cat': base_spec['single_value_cat'],
        'fields': base_spec['fields'],
    }

    out_filename = '%s/modules/idoit_cat_%s.py' % (outdir,base_spec['basename'])
    write_py_file(out_filename, template, idoit_doc,
                  idoit_examples, idoit_return, idoit_spec,
                  'IdoitCategoryModule')


def render_cat_info(base_spec, template, outdir):
    idoit_doc_options = {}
    idoit_doc = {
        'module': ('idoit_cat_%s_info' % base_spec['basename']),
        'short_description': (
            'Get values from a %s category to an object' %
            base_spec['basename']),
        'description':  ('Gets %s category  values' % base_spec['category']),
        'options': idoit_doc_options,
        'author': ['Scaleup Technologies', 'Sven Anders (@tabacha)'],
        'extends_documentation_fragment': [
            'scaleuptechnologies.idoit.idoit_option',
            'scaleuptechnologies.idoit.category_options']
    }
    module_fqn = 'scaleuptechnologies.idoit.idoit_cat_%s_info' % base_spec['basename']
    idoit_examples = {
        "name": "Search for a category for object 1320",
        module_fqn: {
            "idoit": "{{ idoit_access }}",
            "obj_id": 1320
        }
    }
    idoit_return = {
        'changed': {
            'description': 'Are there changes?',
            'type': 'bool',
            'returned': 'always'
        },
        'data': {
            'description': 'Data of the category',
            'returned': 'always',
            'type': 'complex',
        }
    }
    idoit_spec = {
        'category': base_spec['category'],
        'single_value_cat': base_spec['single_value_cat'],
        'fields': base_spec['fields'],
    }

    out_filename = '%s/modules/idoit_cat_%s_info.py' % (outdir,base_spec['basename'])
    write_py_file(out_filename, template, idoit_doc, idoit_examples,
                  idoit_return, idoit_spec, 'IdoitCategoryInfoModule')


def write_py_file(filename, template, idoit_doc, idoit_examples,
                  idoit_return, idoit_spec, idoit_class):
    content = template.render(
        idoit_doc=yaml.dump(idoit_doc, width=70),
        idoit_examples=yaml.dump(idoit_examples, width=70),
        idoit_return=yaml.dump(idoit_return, width=70),
        idoit_spec=yaml.dump(idoit_spec, width=70),
        idoit_class=idoit_class)
    with open(filename, 'w') as outfile:
        outfile.write(content)


def processYaml(filename, template, outdir):
    print(filename)

    with open(filename, "r") as stream:
        try:
            base_spec = yaml.safe_load(stream)
            render_cat(base_spec, template, outdir)
            render_cat_info(base_spec, template, outdir)
        except yaml.YAMLError as exc:
            print(exc)


def main():
    aparser = argparse.ArgumentParser(description='Build Idoit Collection')
    aparser.add_argument('-s','--src', type=str, help="src dircectory", default='src/idoit')
    aparser.add_argument('-d','--dest', type=str, help="dest dircectory", default='plugins')
    args = aparser.parse_args()
    directory = f"{args.src}/category/"
    environment = Environment(loader=FileSystemLoader(f"{args.src}/templates/"))
    template = environment.get_template("category.py.j2")
    for file in os.listdir(directory):
        processYaml(os.path.join(directory, file), template, args.dest)

main()
